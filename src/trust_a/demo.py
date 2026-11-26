"""Run fixed proposals against two fresh, in-memory draft queues."""

from collections.abc import Callable
from pathlib import Path

from .controls import dispatch
from .documents import Document, load


def example_dir() -> Path:
    return Path(__file__).parent / "example"


def demo() -> Document:
    directory = example_dir()
    contract, policy = (load(directory / name) for name in ("contract.json", "policy.json"))
    scenarios = []
    for case in (
        "valid",
        "outside-scope",
        "approval-missing",
        "data-unverified",
        "proof-missing",
    ):
        observed = load(directory / "before.json")
        action = "draft.publish" if case == "outside-scope" else "draft.save"
        observed["action"] = action
        if case == "approval-missing":
            observed["approval"] = {"status": "NOT_OBSERVED"}
        if case == "data-unverified":
            observed["sources"]["catalog"] = {"status": "UNVERIFIED"}
        if case == "proof-missing":
            del observed["sources"]["catalog"]["evidence_ref"]
        # Same fixed proposal and adapter behavior in both arms. Each queue starts empty.
        declared: list[str] = []
        guarded: list[str] = []

        def handlers(queue: list[str]) -> dict[str, Callable[[], None]]:
            return {
                "draft.save": lambda: queue.append("saved"),
                "draft.publish": lambda: queue.append("published"),
            }

        handlers(declared)[action]()
        decision = dispatch(
            contract,
            policy,
            observed["run_id"],
            action,
            observed,
            directory / "evidence",
            handlers(guarded),
        )
        scenarios.append(
            {
                "scenario": case,
                "proposal": action,
                "declaration_queue": declared,
                "guarded_queue": guarded,
                "decision": decision,
            }
        )
    return {"stage": "demo", "scenarios": scenarios}
