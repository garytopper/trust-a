import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator
from trust_a.audit import audit
from trust_a.controls import dispatch
from trust_a.demo import demo, example_dir
from trust_a.documents import InvalidDocument, SCHEMAS, load, validate, validator


class ToolkitTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.directory = Path(temp.name) / "evidence"
        shutil.copytree(example_dir() / "evidence", self.directory)
        self.contract, self.policy, self.before, self.after, self.receipt = (
            load(example_dir() / f"{name}.json")
            for name in ["contract", "policy", "before", "after", "receipt"]
        )
        self.calls = []

    def dispatch(self):
        action = self.before["action"]
        result = dispatch(
            self.contract,
            self.policy,
            "sample-1",
            action,
            self.before,
            self.directory,
            {action: lambda: self.calls.append(action)},
        )
        self.assertEqual(result["invoked"], bool(self.calls))
        return result

    def audit(self):
        return audit(self.contract, self.policy, self.receipt, self.after, self.directory)

    def assertFinding(self, result, code):
        self.assertIn(code, [f["code"] for f in result["findings"]], result)
        self.assertNotEqual(result["status"], "PASS")

    def test_packaged_schemas_are_valid(self):
        for kind in SCHEMAS:
            Draft202012Validator.check_schema(validator(kind).schema)

    def test_valid_scenario_calls_adapter_once(self):
        self.assertEqual(self.dispatch()["status"], "PASS")
        self.assertEqual(self.calls, ["draft.save"])
        self.assertEqual(self.audit()["status"], "PASS")

    def test_handler_failure_propagates(self):
        def fail():
            raise RuntimeError("adapter failed")

        with self.assertRaisesRegex(RuntimeError, "adapter failed"):
            dispatch(
                self.contract,
                self.policy,
                "sample-1",
                "draft.save",
                self.before,
                self.directory,
                {"draft.save": fail},
            )

    def test_outside_scope_blocks_registered_tool(self):
        self.before["action"] = "draft.publish"
        self.assertFinding(self.dispatch(), "scope.forbidden")
        self.assertEqual(self.calls, [])

    def test_missing_binding(self):
        result = dispatch(
            self.contract,
            self.policy,
            "sample-1",
            "draft.save",
            self.before,
            self.directory,
            {},
        )
        self.assertFinding(result, "scope.unbound")

    def test_approval_states(self):
        for state in ["PENDING", "NOT_OBSERVED", "REJECTED", "NOT_REQUIRED"]:
            with self.subTest(state=state):
                self.before["approval"] = {"status": state}
                self.assertNotEqual(self.dispatch()["status"], "PASS")
                self.assertEqual(self.calls, [])

    def test_approval_event_scope_and_authority(self):
        self.policy["approval_authorities"] = []
        self.assertFinding(self.dispatch(), "approval.authority")
        self.contract["actions"]["another"] = self.contract["actions"]["draft.save"]
        self.before["action"] = "another"
        self.assertFinding(self.dispatch(), "approval.scope")
        self.assertEqual(self.calls, [])

    def test_run_and_contract_binding(self):
        self.before["run_id"] = "other"
        self.before["contract_version"] = "other"
        self.before["policy_version"] = "other"
        result = self.dispatch()
        for code in [
            "identity.run_id",
            "identity.contract_version",
            "identity.observation.policy_version",
        ]:
            self.assertFinding(result, code)
        self.assertEqual(self.calls, [])

    def test_unverified_sources_block(self):
        for state in ["UNKNOWN", "UNVERIFIED", "UNAVAILABLE", "CONFLICT", "STALE"]:
            self.before["sources"]["catalog"] = {"status": state}
            self.assertFinding(self.dispatch(), "truth.source")
        self.before["sources"] = {}
        self.assertFinding(self.dispatch(), "truth.source")
        self.assertEqual(self.calls, [])

    def test_missing_and_modified_blob(self):
        ref = self.before["sources"]["catalog"]["evidence_ref"]
        path = self.directory / ref.split(":")[-1]
        path.write_bytes(b"changed")
        self.assertFinding(self.dispatch(), "evidence.digest")
        path.unlink()
        self.assertFinding(self.dispatch(), "evidence.unavailable")
        self.assertFinding(self.audit(), "evidence.unavailable")
        self.assertEqual(self.calls, [])

    def test_autonomy_and_risk(self):
        for level in ["READ_ONLY", "RECOMMEND"]:
            self.contract["autonomy"] = level
            self.assertFinding(self.dispatch(), "autonomy.write")
        self.contract["risk_ceiling"] = "R0"
        self.assertFinding(self.dispatch(), "risk.ceiling")
        self.contract["actions"]["draft.save"]["risk"] = "R0"
        self.assertFinding(self.dispatch(), "risk.mutation")
        self.assertEqual(self.calls, [])

    def test_low_risk_read_can_run_without_approval(self):
        self.contract["autonomy"] = "READ_ONLY"
        self.contract["actions"]["catalog.read"] = {
            "effect": "READ",
            "risk": "R0",
            "required_sources": [],
        }
        self.before.update(action="catalog.read", approval={"status": "NOT_REQUIRED"})
        self.assertEqual(self.dispatch()["status"], "PASS")

    def test_existing_execution_blocks_dispatch(self):
        self.before = self.after
        self.assertFinding(self.dispatch(), "execution.recorded")
        self.assertEqual(self.calls, [])

    def test_missing_observations_and_receipt_lists(self):
        self.after = None
        del self.receipt["material_actions"]
        result = self.audit()
        self.assertFinding(result, "observations.missing")
        self.assertFinding(result, "actions.unobserved")

    def test_failed_unlisted_and_unobserved_check(self):
        self.after["checks"][0]["status"] = "FAIL"
        self.assertFinding(self.audit(), "verification.result")
        self.receipt["evidence"].clear()
        self.assertFinding(self.audit(), "evidence.unlisted")
        self.after["checks"].clear()
        self.assertFinding(self.audit(), "verification.missing")

    def test_independence_required_for_specific_check(self):
        self.policy["by_risk"]["R1"]["verification"] = "INDEPENDENT"
        self.assertFinding(self.audit(), "verification.independence")
        self.after["checks"][0]["class"] = "INDEPENDENT"
        self.assertFinding(self.audit(), "receipt.verification.class")
        self.receipt["verification"]["class"] = "INDEPENDENT"
        self.assertEqual(self.audit()["status"], "PASS")

    def test_schema_invalid_format_and_unknown_fields(self):
        for key, value in [
            ("completed_at", "yesterday"),
            ("risk", "R9"),
            ("extra", True),
        ]:
            with self.subTest(field=key), self.assertRaises(InvalidDocument):
                validate("receipt", {**self.receipt, key: value})
        self.receipt["evidence"][0]["uri"] = "not a URI"
        with self.assertRaises(InvalidDocument):
            validate("receipt", self.receipt)

    def test_unsupported_uri_is_unknown_without_fetching(self):
        self.receipt["evidence"][0]["uri"] = "https://example.invalid/source"
        self.assertFinding(self.audit(), "evidence.unobserved")

    def test_receipt_cannot_hide_action_or_disagreement(self):
        self.receipt["material_actions"] = []
        self.receipt["approval"]["required"] = False
        self.receipt["risk"] = "R0"
        result = self.audit()
        for code in [
            "receipt.material_actions",
            "receipt.approval.required",
            "receipt.risk",
        ]:
            self.assertFinding(result, code)

    def test_proven_stop_vs_missing_execution(self):
        self.after["approval"] = {"status": "PENDING"}
        self.receipt["approval"] = {"required": True, "status": "PENDING"}
        self.after["checks"] = []
        self.receipt["verification"] = {
            "required": False,
            "class": "NOT_REQUIRED",
            "checks": [],
        }
        self.receipt.update(outcome="AWAITING_APPROVAL", material_actions=[])
        data = b"Fixture adapter: pending approval; handler not invoked."
        key = hashlib.sha256(data).hexdigest()
        (self.directory / key).write_bytes(data)
        uri = "urn:sha256:" + key
        self.after["execution"] = {"status": "NOT_INVOKED", "evidence_ref": uri}
        self.receipt["evidence"] = [{"label": "stop", "uri": uri}]
        self.assertEqual(self.audit()["status"], "PASS")
        del self.after["execution"]
        self.assertFinding(self.audit(), "execution.unknown")

    def test_duplicate_keys_rejected(self):
        path = self.directory / "ambiguous.json"
        path.write_text('{"run_id":"one","run_id":"two"}')
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            load(path)

    def test_controlled_comparison_observes_distinct_effects(self):
        first = demo()
        self.assertEqual(first, demo())
        self.assertEqual(len(first["scenarios"]), 5)
        for case in first["scenarios"]:
            self.assertEqual(len(case["declaration_queue"]), 1)
            self.assertEqual(len(case["guarded_queue"]), int(case["scenario"] == "valid"))
        self.assertIn("scope.forbidden", json.dumps(first))
