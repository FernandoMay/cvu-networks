import numpy as np
import random
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from core.coalition import UserNode, CoalitionEngine

@dataclass
class SimulationConfig:
    lambda_rate: float = 0.90
    tau_lag: float = 50.0
    num_edge_nodes: int = 4
    edge_capacity: int = 30
    edge_latency_base: float = 10.0
    cloud_latency_base: float = 30.0
    cloud_propagation_delay: float = 50.0
    simulation_time: int = 100000
    warmup_period: int = 35000

class EdgeNode:
    def __init__(self, node_id: int, capacity: int, latency: float):
        self.node_id = node_id
        self.capacity = capacity
        self.latency = latency
        self.queue = 0

    def is_full(self) -> bool:
        return self.queue >= self.capacity

    def process_task(self) -> float:
        if self.queue > 0:
            self.queue -= 1
            return self.latency
        return 0.0

class CloudNode:
    def __init__(self, latency: float, prop_delay: float):
        self.latency = latency
        self.prop_delay = prop_delay
        self.queue = 0

    def process_task(self) -> float:
        if self.queue > 0:
            self.queue -= 1
            return self.latency + self.prop_delay
        return 0.0

class CVUEnvironment:
    def __init__(self, config: SimulationConfig):
        self.config = config
        self.edge_nodes = [EdgeNode(i, config.edge_capacity, config.edge_latency_base) for i in range(config.num_edge_nodes)]
        self.cloud_node = CloudNode(config.cloud_latency_base, config.cloud_propagation_delay)
        self.current_time = 0
        self.tasks_processed = 0
        self.total_latency = 0.0
        self.dropped_tasks = 0

    def route_task(self, user: UserNode, policy: str = " UAER\) -> Tuple[str, Optional[int]]:
 if policy == \UAER\:
 if user.state.temporal_urgency >= 0.7:
 available_edge = [n for n in self.edge_nodes if not n.is_full()]
 if available_edge:
 node = random.choice(available_edge)
 node.queue += 1
 return \edge\, node.node_id

 available_edge = [n for n in self.edge_nodes if not n.is_full()]
 if available_edge:
 node = random.choice(available_edge)
 node.queue += 1
 return \edge\, node.node_id

 self.cloud_node.queue += 1
 return \cloud\, None

 def step(self) -> float:
 self.current_time += 1
 step_latency = 0.0
 for node in self.edge_nodes:
 lat = node.process_task()
 if lat > 0:
 step_latency += lat
 self.tasks_processed += 1
 cloud_lat = self.cloud_node.process_task()
 if cloud_lat > 0:
 step_latency += cloud_lat
 self.tasks_processed += 1
 self.total_latency += step_latency
 return step_latency / (self.tasks_processed if self.tasks_processed > 0 else 1)
