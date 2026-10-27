# CVU Networking PhD Repository

This repository implements a reproducible simulation framework for low-latency cognitive virtual universe (CVU) operations in edge-cloud network environments. The code models coalition formation among user nodes, urgency-aware task routing, and latency-driven orchestration under a cognitive network setting.

## Research focus

The project targets the problem of efficient task placement and coalition-aware coordination in cognitive network systems where user states evolve over time and edge infrastructure must handle bursts of localized demand. The implementation emphasizes:

- cognitive-state modeling for each user or node,
- coalition formation based on distance and state similarity,
- urgency-aware edge routing,
- fallback behavior to cloud infrastructure when edge resources are saturated,
- analysis and plotting for publication-style reporting.

## Repository structure

- `core/coalition.py`: coalition formation logic and cognitive state representation
- `simulator/environment.py`: edge/cloud environment and task routing model
- `experiments/run_simulation.py`: end-to-end simulation runner
- `results/`: generated metrics, figures, and traces
- `docs/`: project documentation and research notes

## Reproduction

1. Create and activate a Python environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the simulation:

   ```bash
   python experiments/run_simulation.py
   ```

4. Generate the summary figure:

   ```bash
   python results/plotting.py
   ```

5. Generate a compact metrics summary:

   ```bash
   python results/metrics_summary.py
   ```

6. Generate a comparative scenario matrix for publication-facing analysis:

   ```bash
   python results/plot_scenario_matrix.py
   ```

## Current validated result

The repository currently produces the following output from the simulation:

- Average latency: 0.00016199515581773036 ms
- Tasks processed: 90,071
- Dropped tasks: 0

The project also includes a comparative scenario grid stored in `results/scenario_comparison.json`, with a summary plot generated at `results/scenario_matrix.png`.

## Notes

This project is structured for research reproducibility and extension. The current version includes a validated baseline plus a comparative multi-scenario evaluation intended to support the paper narrative and publication-style analysis.
