from dataclasses import dataclass
from enum import Enum
from typing import List


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.value}, l={self.left}, r={self.right})"


class Graph:
    root: Node = None
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
        if node.value == 'AAA':
            print(node)
            self.root = node


def calculate_steps(graph, target, directions: str) -> List[Node]:
    steps = []
    current_node = graph.root
    for direction in directions * 1000:
        if current_node.value == target:
            return steps
        if direction == "L":
            current_node = graph[current_node.left]
        elif direction == "R":
            current_node = graph[current_node.right]
        else:
            raise ValueError(f"Invalid direction: {direction}")
        steps.append(current_node)

    return steps


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
        steps = calculate_steps(nodes, 'ZZZ', directions)
        print(len(steps))


if __name__ == "__main__":
    main()
