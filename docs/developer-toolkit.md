# Integrate the Developer Toolkit

The 1.0 release candidate runs locally with Python 3.11+ and pip. It makes a small part of an Agent Contract executable. The six dimensions, design questions and risk classification remain engineering decisions. Start with the [Agent Contract](../templates/AGENT-CONTRACT.md) and the [Risk & Autonomy Policy](../templates/RISK-AUTONOMY-POLICY.md).

## See the first result

From the repository checkout on Linux or macOS:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -c requirements-dev.lock .
trust-a demo
```

On Windows activate the environment with `.venv\Scripts\Activate.ps1`. The comparison sends five fixed proposals to two fresh in-memory queues. In the declarative arm the simulator invokes its handler directly. In the guarded arm the same handler runs through `dispatch`. Inspect the resulting queue for each case. The valid save appears in both. A publish proposal, missing approval, unverified catalog and missing proof leave the guarded queue empty. No model, production tool or network service participates. These results measure control behavior on those proposals.

## Run an independent consumer

From the checkout, with the environment still active:

```sh
mkdir ../draft-consumer
cp -R examples/draft examples/run_workflow.py ../draft-consumer/
cd ../draft-consumer
trust-a validate contract draft/contract.json
trust-a validate policy draft/policy.json
trust-a check draft/contract.json draft/policy.json draft/before.json \
  --action draft.save --run-id sample-1 --evidence-dir draft/evidence
python run_workflow.py draft allowed
trust-a validate receipt allowed/receipt.json
trust-a audit draft/contract.json draft/policy.json allowed/receipt.json \
  --observations allowed/after.json --evidence-dir allowed/evidence --json
```

The example creates an evidence directory, a dispatch decision, host observations and a receipt. It derives the material action and the `SELF` check from the queue it inspected. Each run writes to a new output directory.

```sh
python run_workflow.py draft blocked --unverified
trust-a audit draft/contract.json draft/policy.json blocked/receipt.json \
  --observations blocked/after.json --evidence-dir blocked/evidence
```

The second queue stays empty. The receipt outcome is `ABORTED`, and the audit can pass because the host recorded the stop. To see a structural failure, run `trust-a validate receipt draft/contract.json --json`. To see an evidence gap, omit `--observations` from an audit. Every subcommand accepts `--json`. Exit 0 means the requested check passed or the demo completed, 1 means a failed or unknown control, and 2 means invalid input or invocation. Gate on both audit status and receipt outcome if the job also requires successful work.

## Configure the trust boundary

| Document or boundary | Owner and meaning |
| --- | --- |
| [Contract](../examples/draft/contract.json) | The operator assigns stable agent identity, contract/policy versions, objective, autonomy and ceiling. Each allowed capability declares a fixed effect, risk and required sources. Omission denies a capability. |
| [Policy](../examples/draft/policy.json) | The operator names approval authorities and sets approval and named verification requirements for every risk class. `ACT_WITH_APPROVAL` also requires approval for every write. `READ_ONLY` and `RECOMMEND` exclude writes. R0 represents observation. |
| [Pre-action observations](../examples/draft/before.json) | The host binds trusted adapter data to one run, action and authority version. The proposal supplies only a capability ID. Host adapters assess source provenance, freshness and conflicts, then record a status and supporting bytes. |
| Host dispatch | A host-owned mapping binds each capability to a zero-argument handler with a fixed target and payload. Only dispatch has access to that handler. Invalid structure raises `InvalidDocument` before invocation. A failed or unknown precondition returns `invoked: false`. |
| [Post-action observations](../examples/draft/after.json) | The host records application, proven non-invocation or lack of observation. Named checks specify their result and verifier class. The policy may require an independent verifier for each named check. |
| [Run Receipt](../schemas/run-receipt.schema.json) | The portable v1 schema remains unchanged. The toolkit audit profile expects a contract version, an explicit material action list and a local manifest of evidence references. A schema pass alone establishes document shape. |

Configure an actual dispatch boundary in the host:

```python
from trust_a.controls import dispatch

result = dispatch(
    contract, policy, run_id, proposed_capability, host_observations,
    evidence_directory, {"draft.save": save_this_validated_draft},
)
if not result["invoked"]:
    record_stop(result["findings"])
```

The concrete adapter and complete runnable example are in [run_workflow.py](../examples/run_workflow.py). Keep the contract, policy, observations, evidence store and binding registry outside the proposal author's write authority. Bind parameters and destination before approval. Use a fresh run ID for each invocation. The fixture reuses one synthetic ID in isolated directories so the comparison is reproducible.

## Evidence and limitations

- **Integrity.** Store blob bytes under their lowercase SHA-256 hex filename. Reference them with `urn:sha256:<digest>`. The toolkit checks each digest locally. Other well-formed receipt URIs remain valid under the canonical schema and yield an unknown in this local audit profile.
- **Approval.** The fixture approval blob is a JSON event with `agent_id`, `contract_version`, `policy_version`, `run_id`, `action`, `approver` and `decision`. Dispatch compares its scope and approver to the host configuration. The host must authenticate the emitter, enforce expiry, revocation and single use, and ensure the fixed inputs remain current through the action.
- **Verification.** The host must establish verifier identity and independence. The audit reconciles claimed and observed checks by name, checks evidence and enforces the configured minimum class. A `SELF` check cannot satisfy an `INDEPENDENT` requirement. A checksum establishes byte integrity. It provides no assurance about who produced the bytes.
- **Unknowns.** Missing observations, evidence or required checks yield explicit findings. Pending and rejected approvals stop dispatch. Runtime/model metadata in a receipt grants no additional authority.
- **Boundary.** This release profiles one fixed, bounded action per run. The host owns concurrency, parameter validation, transactionality, retry safety and recovery. A handler exception propagates because a failed handler may already have changed state. Tools that bypass dispatch are outside its control. The audit covers the observed records and cannot discover omitted actions in another system.

## CI and local builds

From a clean checkout, create a virtual environment and run:

```sh
python -m pip install -r requirements-dev.lock
bash scripts/check.sh
```

The same command runs in the existing PR check. It checks skill sync, compiles and lints Python, checks types and formatting, builds the source distribution and wheel, installs the wheel, then runs tests and the consumer exercise outside the checkout. The RC files are available in `dist/`. To install the wheel in a separate environment, use `python -m pip install -c requirements-dev.lock dist/trust_a_toolkit-1.0.0rc1-py3-none-any.whl`. No package publication step is configured.

Maintainers can refresh the dependency pins with `uv pip compile pyproject.toml requirements-dev.in --universal --python-version 3.11 --no-annotate --no-header -o requirements-dev.lock`. Treat a dependency refresh as a reviewed change and run the full gate.
