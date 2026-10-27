import numpy as np
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass, field
import uuid

@dataclass(frozen=True)
class CognitiveState:
    explicit_intent: float
    attention_span: float
    decision_confidence: float
    temporal_urgency: float
    cognitive_workload: float

    def to_array(self) -> np.ndarray:
        return np.array([self.explicit_intent, self.attention_span, self.decision_confidence,
        self.temporal_urgency, self.cognitive_workload])

@dataclass(frozen=True)
class UserNode:
    user_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    position: np.ndarray = field(default_factory=lambda: np.random.rand(3) * 100)
    state: CognitiveState = None

    def __post_init__(self):
        if self.state is None:
            self.state = CognitiveState(np.random.rand(), np.random.rand(), np.random.rand(), np.random.rand(),
            np.random.rand())

class CoalitionEngine:
    def __init__(self, beta: float = 0.6):
        self.beta = beta

    def calculate_cognitive_distance(self, user_i: UserNode, user_j: UserNode) -> float:
        phys_dist = np.linalg.norm(user_i.position - user_j.position)
        norm_phys_dist = min(phys_dist / 100.0, 1.0)
        neural_dist = np.linalg.norm(user_i.state.to_array() - user_j.state.to_array())
        norm_neural_dist = min(neural_dist / np.sqrt(5), 1.0)
        return (1 - self.beta) * norm_phys_dist + self.beta * norm_neural_dist

    def calculate_utility(self, coalition: Set[UserNode]) -> float:
        if not coalition: return 0.0
        if len(coalition) == 1: return 1.0
        total_dist = 0
        count = 0
        nodes = list(coalition)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                total_dist += self.calculate_cognitive_distance(nodes[i], nodes[j])
                count += 1
        avg_dist = total_dist / count if count > 0 else 1.0
        return 10.0 / (1.0 + avg_dist)

    def merge_and_split(self, users: List[UserNode]) -> List[Set[UserNode]]:
        partitions = [{u} for u in users]
        stable = False
        iterations = 0
        max_iter = 1000
        while not stable and iterations < max_iter:
            iterations += 1
            stable = True
            for i in range(len(partitions)):
                for j in range(i + 1, len(partitions)):
                    c1, c2 = partitions[i], partitions[j]
                    if self.calculate_utility(c1 | c2) > self.calculate_utility(c1) + self.calculate_utility(c2):
                        partitions[i] = c1 | c2
                        partitions.pop(j)
                        stable = False
                        break
                if not stable: break
            if not stable: continue
            for i in range(len(partitions)):
                coalition = partitions[i]
                if len(coalition) < 2: continue
                nodes = list(coalition)
                for split_idx in range(1, len(nodes)):
                    s1 = set(nodes[:split_idx])
                    s2 = set(nodes[split_idx:])
                    if self.calculate_utility(s1) + self.calculate_utility(s2) > self.calculate_utility(coalition):
                        partitions[i] = s1
                        partitions.append(s2)
                        stable = False
                        break
                if not stable: break
        return partitions

