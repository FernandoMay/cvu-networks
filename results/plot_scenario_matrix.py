import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
RESULT_PATH = ROOT / "results" / "scenario_comparison.json"
OUTPUT_PATH = ROOT / "results" / "scenario_matrix.png"


def load_data(path: Path = RESULT_PATH) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def plot_matrix(data: list[dict], output_path: Path = OUTPUT_PATH) -> Path:
    betas = sorted({entry["beta"] for entry in data})
    user_counts = sorted({entry["num_users"] for entry in data})

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    for beta in betas:
        series = [
            next(entry["avg_latency"] for entry in data if entry["num_users"] == users and entry["beta"] == beta)
            for users in user_counts
        ]
        axes[0].plot(user_counts, series, marker="o", linewidth=2, label=f"beta={beta}")

    axes[0].set_title("Average latency vs user density")
    axes[0].set_xlabel("Users")
    axes[0].set_ylabel("Average latency")
    axes[0].grid(alpha=0.3)
    axes[0].legend(loc="best")

    beta_series = []
    for beta in betas:
        beta_series.append(
            sum(entry["p95_latency"] for entry in data if entry["beta"] == beta) / len([1 for entry in data if entry["beta"] == beta])
        )
    axes[1].bar([str(beta) for beta in betas], beta_series, color="#4C78A8")
    axes[1].set_title("Average p95 latency by beta")
    axes[1].set_xlabel("Beta")
    axes[1].set_ylabel("p95 latency")
    axes[1].grid(axis="y", alpha=0.3)

    fig.suptitle("CVU scenario comparison matrix", fontsize=14, weight="bold")
    fig.tight_layout()
    fig.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return output_path


if __name__ == "__main__":
    data = load_data()
    output = plot_matrix(data)
    print(f"Saved scenario matrix plot to {output}")
