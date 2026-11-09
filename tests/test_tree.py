"""Unit tests for agent-scratchpad-branching-tree."""
import unittest
from agent_scratchpad_branching_tree.tree import ScratchpadTree


class TestScratchpadTree(unittest.TestCase):
    def setUp(self):
        self.tree = ScratchpadTree("Root task")

    def test_branching_and_trajectory(self):
        b1 = self.tree.branch("root", "Branch 1", 0.4)
        b2 = self.tree.branch("root", "Branch 2", 0.9)

        traj = self.tree.get_best_trajectory()
        self.assertEqual(len(traj), 2)
        self.assertEqual(traj[-1].node_id, b2.node_id)

    def test_pruned_leaves_skipped(self):
        b1 = self.tree.branch("root", "Branch 1", 0.4)
        b2 = self.tree.branch("root", "Branch 2", 0.9)
        self.tree.prune_branch(b2.node_id)

        traj = self.tree.get_best_trajectory()
        # b2 is pruned, so b1 becomes best active
        self.assertEqual(traj[-1].node_id, b1.node_id)
