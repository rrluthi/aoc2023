import math
from typing import List


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.value}, l={self.left}, r={self.right})"


class Graph:
    roots: List[Node] = []
    nodes: dict = {}

    def __init__(self, root: Node = None):
        self.root = root

    def __repr__(self):
        return f"Graph({self.nodes})"

    def __getitem__(self, key):
        if key in self.nodes:
            return self.nodes[key]
        raise KeyError(f"Node {key} not found")

    def insert_node(self, node: Node):
        if node.value in self.nodes:
            raise ValueError(f"Node {node.value} already exists")
        self.nodes[node.value] = node
        if node.value.endswith('A'):
            self.roots.append(node)


def calculate_steps(graph, directions: str, counter=0) -> int:
    step_counter = counter
    group = graph.roots
    counters = []
    for direction in directions * 100:
        step_counter += 1
        for i, current_node in enumerate(group):
            if direction == "L":
                group[i] = graph[current_node.left]
            elif direction == "R":
                group[i] = graph[current_node.right]
            else:
                raise ValueError(f"Invalid direction: {direction}")
            if group[i].value.endswith('Z'):
                counters.append(step_counter)

        if len(counters) == len(group):
            print(f"Found all ends with Z: {group}")
            break

    total = math.lcm(*counters)
    return total


def parse_input(f) -> (Node, str):
    nodes = []
    directions = f.readline().strip()
    for line in f:
        line = line.strip()
        if not line:
            continue
        if "=" in line:
            key, value = line.split(" = ")
            left, right = value.strip("()").split(", ")
            nodes.append(Node(value=key, left=left, right=right))

    graph = Graph()
    for node in nodes:
        graph.insert_node(node)
    return graph, directions


def main():
    with open('input8.txt') as f:
        nodes, directions = parse_input(f)
        steps = calculate_steps(nodes, directions)
        print(steps)


if __name__ == "__main__":
    main()
