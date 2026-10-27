import json
import os
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.coalition import CoalitionEngine, UserNode
from simulator.environment import CVUEnvironment, SimulationConfig


def run_experiment() -> None:
    print("Starting PhD-Level Simulation: Coalition-NDAN vs Baseline...")

    config = SimulationConfig()
    env = CVUEnvironment(config)
    engine = CoalitionEngine(beta=0.6)

    num_users = 100
    users = [UserNode() for _ in range(num_users)]

    coalitions = engine.merge_and_split(users)
    print(f"Formed {len(coalitions)} cognitive coalitions.")

    latencies = []
    for t in range(config.simulation_time):
        if random.random() < config.lambda_rate:
            user = random.choice(users)
            env.route_task(user)

        avg_lat = env.step()
        if t > config.warmup_period:
            latencies.append(avg_lat)

    final_avg_latency = np.mean(latencies) if latencies else 0.0
    print(f"Simulation Complete. Final Avg Latency: {final_avg_latency:.4f} ms")

    results_dir = ROOT / "results"
    results_dir.mkdir(exist_ok=True)
    results = {
        "avg_latency": float(final_avg_latency),
        "tasks_processed": env.tasks_processed,
        "dropped_tasks": env.dropped_tasks,
    }

    result_path = results_dir / "simulation_results.json"
    with result_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"Results saved to {result_path}")


if __name__ == "__main__":
    run_experiment()