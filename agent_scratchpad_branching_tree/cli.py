"""CLI for agent-scratchpad-branching-tree."""
import sys
import argparse
from .tree import ScratchpadTree


def main():
    parser = argparse.ArgumentParser(description="Agent Scratchpad Branching Tree CLI")
    parser.add_argument("--demo", action="store_true", help="Run Tree-of-Thought branching simulation")
    args = parser.parse_args()

    if args.demo:
        tree = ScratchpadTree("How to fix slow API endpoint?")
        b1 = tree.branch("root", "Hypothesis 1: Add Redis cache", score=0.85)
        b2 = tree.branch("root", "Hypothesis 2: Rewrite in C++", score=0.30)

        # Explore sub-branch of b1
        b1_1 = tree.branch(b1.node_id, "Implement cache-aside pattern", score=0.95)

        # Prune dead-end b2
        tree.prune_branch(b2.node_id)

        trajectory = tree.get_best_trajectory()
        print("Best Tree-of-Thought Reasoning Trajectory:")
        for step in trajectory:
            print(f"  [{step.node_id}] Score: {step.score:.2f} -> {step.thought_content}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
