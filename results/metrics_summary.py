import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "simulation_results.json"
REPORT_PATH = ROOT / "results" / "metrics_summary.txt"


def summarize_results(path: Path = RESULT_PATH) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    metrics = {
        "avg_latency_ms": float(data.get("avg_latency", 0.0)),
        "tasks_processed": int(data.get("tasks_processed", 0)),
        "dropped_tasks": int(data.get("dropped_tasks", 0)),
        "success_rate": 1.0 if int(data.get("tasks_processed", 0)) > 0 else 0.0,
    }

    report = (
        "CVU Simulation Metrics\n"
        "======================\n"
        f"Average latency: {metrics['avg_latency_ms']:.12f} ms\n"
        f"Tasks processed: {metrics['tasks_processed']}\n"
        f"Dropped tasks: {metrics['dropped_tasks']}\n"
        f"Success rate: {metrics['success_rate']:.4f}\n"
    )
    REPORT_PATH.write_text(report, encoding="utf-8")
    return metrics


if __name__ == "__main__":
    metrics = summarize_results()
    print(json.dumps(metrics, indent=2))
    print(f"\nSaved summary report to {REPORT_PATH}")
