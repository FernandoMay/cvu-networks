import json
import random
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.coalition import CoalitionEngine, UserNode
from simulator.environment import CVUEnvironment, SimulationConfig

OUTPUT_PATH = ROOT / "results" / "scenario_comparison.json"


def run_single_scenario(num_users: int, beta: float, simulation_time: int = 20000, warmup_period: int = 4000) -> dict:
    config = SimulationConfig(
        lambda_rate=0.9,
        simulation_time=simulation_time,
        warmup_period=warmup_period,
    )
    env = CVUEnvironment(config)
    engine = CoalitionEngine(beta=beta)
    users = [UserNode() for _ in range(num_users)]

    coalitions = engine.merge_and_split(users)
    latencies = []
    for t in range(config.simulation_time):
        if random.random() < config.lambda_rate:
            user = random.choice(users)
            env.route_task(user)
        avg_lat = env.step()
        if t > config.warmup_period:
            latencies.append(avg_lat)

    p95_latency = float(np.percentile(latencies, 95)) if latencies else 0.0
    spectral_efficiency_proxy = float((env.tasks_processed + 1.0) / max(1.0, num_users * (p95_latency + 1e-6)))

    return {
        "num_users": num_users,
        "beta": beta,
        "coalitions": len(coalitions),
        "avg_latency": float(np.mean(latencies)) if latencies else 0.0,
        "p95_latency": p95_latency,
        "spectral_efficiency_proxy": spectral_efficiency_proxy,
        "tasks_processed": int(env.tasks_processed),
        "dropped_tasks": int(env.dropped_tasks),
    }


def run_matrix() -> list[dict]:
    scenarios = []
    for users in [20, 50, 100, 200]:
        for beta in [0.0, 0.4, 0.6, 0.8, 1.0]:
            scenarios.append(run_single_scenario(num_users=users, beta=beta))
    return scenarios


def main() -> None:
    results = run_matrix()
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, indent=2)
    print(json.dumps(results, indent=2))
    print(f"\nSaved scenario comparison to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
