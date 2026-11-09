"""Core Agent Scratchpad Branching Tree implementation."""
from typing import Dict, List, Optional, Tuple, Any


class TreeNode:
    def __init__(self, node_id: str, parent_id: Optional[str], thought_content: str, score: float = 0.0):
        self.node_id = node_id
        self.parent_id = parent_id
        self.thought_content = thought_content
        self.score = score
        self.children: List[str] = []
        self.is_pruned = False


class ScratchpadTree:
    def __init__(self, root_problem: str):
        self.nodes: Dict[str, TreeNode] = {}
        root_node = TreeNode("root", None, root_problem, 1.0)
        self.nodes["root"] = root_node
        self._next_id = 1

    def branch(self, parent_id: str, thought_content: str, score: float = 0.5) -> TreeNode:
        if parent_id not in self.nodes:
            raise KeyError(f"Parent node '{parent_id}' does not exist")

        node_id = f"node_{self._next_id}"
        self._next_id += 1
        node = TreeNode(node_id, parent_id, thought_content, score)
        self.nodes[node_id] = node
        self.nodes[parent_id].children.append(node_id)
        return node

    def prune_branch(self, node_id: str):
        if node_id in self.nodes:
            self.nodes[node_id].is_pruned = True
            for child_id in self.nodes[node_id].children:
                self.prune_branch(child_id)

    def get_best_trajectory(self) -> List[TreeNode]:
        # Find active (non-pruned) leaf node with highest cumulative score
        leaves = [n for n in self.nodes.values() if not n.children and not n.is_pruned]
        if not leaves:
            return [self.nodes["root"]]

        best_leaf = max(leaves, key=lambda n: n.score)
        trajectory = []
        curr = best_leaf
        while curr:
            trajectory.append(curr)
            curr = self.nodes.get(curr.parent_id) if curr.parent_id else None

        trajectory.reverse()
        return trajectory
