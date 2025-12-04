# lattice.py
import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name, state=0.0):
        self.name = name
        self.state = state
        self.children = []

    def add_child(self, node):
        self.children.append(node)

    def update_state(self, influence):
        # Simple triadic coherence: average of child influence + own state
        if self.children:
            child_avg = np.mean([c.state for c in self.children])
            self.state = (self.state + child_avg + influence) / 3
        else:
            self.state = (self.state + influence) / 2

class TriadicLattice:
    def __init__(self, depth=3, branching=2):
        self.root = Node("Observer")
        self.depth = depth
        self.branching = branching
        self.nodes = [self.root]
        self.build_lattice(self.root, depth)

    def build_lattice(self, parent, depth):
        if depth <= 0:
            return
        for i in range(self.branching):
            child = Node(f"{parent.name}-{i}")
            parent.add_child(child)
            self.nodes.append(child)
            self.build_lattice(child, depth-1)

    def propagate(self, influence=1.0, iterations=5):
        for _ in range(iterations):
            for node in reversed(self.nodes):
                node.update_state(influence)

    def visualize(self):
        states = [node.state for node in self.nodes]
        plt.figure(figsize=(10,4))
        plt.bar(range(len(states)), states)
        plt.xlabel("Nodes")
        plt.ylabel("State Value")
        plt.title("Triadic Recursive Lattice States")
        plt.show()


# Example usage
if __name__ == "__main__":
    lattice = TriadicLattice(depth=3, branching=3)
    lattice.propagate(influence=1.0, iterations=5)
    lattice.visualize()