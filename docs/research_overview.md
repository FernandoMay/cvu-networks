# Research overview

## Problem statement

The simulation models a multi-user cognitive networking scenario in which edge and cloud infrastructure coordinate to process latency-sensitive tasks. The objective is to minimize response latency while preserving service stability under demand bursts and heterogeneous user states.

## Core modeling assumptions

- User nodes are represented by a cognitive state with explicit intent, attention span, confidence, urgency, and workload.
- Cognitive similarity drives coalition formation.
- Spatial distance and state similarity jointly define the cost of coalition merging.
- Edge infrastructure provides lower-latency service, while cloud access acts as a fallback when edge nodes saturate.
- A urgency-aware routing policy prioritizes highly time-sensitive tasks to edge resources.

## Expected behavior

The experiment is designed to show that coalition-aware routing reduces the effective cost of service delivery by exploiting local structure and demand clustering. The simulation outcome summarises throughput, latency, and task drop count under a representative workload profile.

## Reproducibility checklist

- Install dependencies from `requirements.txt`.
- Run `python experiments/run_simulation.py`.
- Inspect `results/simulation_results.json`.
- Generate plots with `python results/plotting.py`.
- Confirm the summary report from `python results/metrics_summary.py`.
