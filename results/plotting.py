import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "simulation_results.json"
OUTPUT_PATH = ROOT / "results" / "simulation_summary.png"


def load_results(path: Path = RESULT_PATH) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def plot_summary(results: dict, output_path: Path = OUTPUT_PATH) -> Path:
    latency = float(results.get("avg_latency", 0.0))
    tasks_processed = int(results.get("tasks_processed", 0))
    dropped_tasks = int(results.get("dropped_tasks", 0))

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].bar(["Average latency"], [latency], color="#2E86DE")
    axes[0].set_title("Observed average latency")
    axes[0].set_ylabel("Latency (ms)")
    axes[0].grid(axis="y", linestyle="--", alpha=0.3)

    axes[1].bar(["Processed", "Dropped"], [tasks_processed, dropped_tasks], color=["#5B8DEF", "#E76F51"])
    axes[1].set_title("Task throughput and drops")
    axes[1].set_ylabel("Count")
    axes[1].grid(axis="y", linestyle="--", alpha=0.3)

    fig.suptitle("CVU coalition simulation summary", fontsize=14, weight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return output_path


if __name__ == "__main__":
    results = load_results()
    output = plot_summary(results)
    print(f"Saved summary plot to {output}")
