"""Exercise the installed wheel from a new directory with no repository imports."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory() as name:
        project = Path(name)
        shutil.copytree(ROOT / "examples" / "draft", project / "spec")
        shutil.copy(ROOT / "examples" / "run_workflow.py", project)
        cli = str(Path(sys.executable).with_name("trust-a"))

        def run(*args, expected=0):
            result = subprocess.run(args, cwd=project, capture_output=True, text=True)
            if result.returncode != expected:
                raise RuntimeError(f"{args}: {result.returncode}\n{result.stdout}\n{result.stderr}")
            return json.loads(result.stdout)

        for kind, file in [
            ("contract", "contract"),
            ("policy", "policy"),
            ("receipt", "receipt"),
            ("observations", "before"),
            ("observations", "after"),
        ]:
            assert run(cli, "validate", kind, f"spec/{file}.json", "--json")["status"] == "PASS"
        for scenario, args in [("allowed", []), ("blocked", ["--unverified"])]:
            result = run(sys.executable, "-I", "run_workflow.py", "spec", scenario, *args)
            assert result["queue"] == (["draft"] if scenario == "allowed" else [])
            audit = run(
                cli,
                "audit",
                "spec/contract.json",
                "spec/policy.json",
                f"{scenario}/receipt.json",
                "--observations",
                f"{scenario}/after.json",
                "--evidence-dir",
                f"{scenario}/evidence",
                "--json",
            )
            assert audit["status"] == "PASS"
            assert audit["outcome"] == ("PASS" if scenario == "allowed" else "ABORTED")
        check = [
            cli,
            "check",
            "spec/contract.json",
            "spec/policy.json",
            "spec/before.json",
            "--run-id",
            "sample-1",
            "--evidence-dir",
            "spec/evidence",
            "--json",
            "--action",
        ]
        assert run(*check, "draft.save")["status"] == "PASS"
        assert run(*check, "other", expected=1)["status"] == "FAIL"
        (project / "invalid.json").write_text('{"schema_version":null}')
        assert run(cli, "validate", "receipt", "invalid.json", "--json", expected=2)["stage"] == "input"
        demo = run(cli, "demo", "--json")
        assert sum(bool(row["guarded_queue"]) for row in demo["scenarios"]) == 1
        print("Clean consumer: schema, preflight, adapter, audit, demo and exit codes passed.")


if __name__ == "__main__":
    main()
