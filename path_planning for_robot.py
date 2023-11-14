# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 19:00:44 2023

@author: Muntadher
"""

import heapq
import matplotlib.pyplot as plt
import numpy as np

class Node:
    def __init__(self, position, cost=0, parent=None):
        self.position = position
        self.cost = cost
        self.parent = parent

    def __lt__(self, other):
        return self.cost < other.cost

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    open_set = []
    closed_set = set()

    heapq.heappush(open_set, Node(start, 0))

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.position == goal:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        if current_node.position in closed_set:
            continue

        closed_set.add(current_node.position)

        for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (current_node.position[0] + neighbor[0], current_node.position[1] + neighbor[1])

            if (
                0 <= new_position[0] < len(grid)
                and 0 <= new_position[1] < len(grid[0])
                and grid[new_position[0]][new_position[1]] == 0
            ):
                new_cost = current_node.cost + 1
                heapq.heappush(open_set, Node(new_position, new_cost, current_node))

    return None

def plot_paths(grids, paths, probabilities):
    fig, axs = plt.subplots(1, len(grids) + 1, figsize=(12, 4))

    for k, (grid, path, probability) in enumerate(zip(grids, paths, probabilities)):
        cmap = plt.cm.get_cmap('tab10', len(paths))
        axs[k].imshow(grid, cmap='Greys', origin='upper')

        for i, (p, prob) in enumerate(zip(path, probability)):
            color = cmap(i)
            for j, position in enumerate(p):
                alpha = (j + 1) / len(p)  # Adjust alpha based on position in the path
                axs[k].text(position[1], position[0], 'X', ha='center', va='center', color=color, alpha=alpha)

            # Display probability information
            axs[k].text(p[-1][1] + 1, p[-1][0], f'P={prob:.2f}', ha='left', va='center', color=color)

        axs[k].set_title(f'Grid {k + 1}')

    plt.title('Path Planning Visualization with Probabilities')
    plt.xlabel('Column Index')
    plt.ylabel('Row Index')
    plt.show()

# Example usage
grid1 = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

grid2 = [
    [0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

grid3 = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)

# Generate multiple random paths and associated probabilities for demonstration purposes
num_paths = 3
all_paths1, all_probabilities1, all_paths2, all_probabilities2, all_paths3, all_probabilities3 = [], [], [], [], [], []

for _ in range(num_paths):
    path1 = astar(np.copy(grid1), start, goal)
    if path1:
        probability1 = np.random.uniform(0.1, 1.0)  # Random probability for demonstration
        all_paths1.append(path1)
        all_probabilities1.append(probability1)

    path2 = astar(np.copy(grid2), start, goal)
    if path2:
        probability2 = np.random.uniform(0.1, 1.0)  # Random probability for demonstration
        all_paths2.append(path2)
        all_probabilities2.append(probability2)

    path3 = astar(np.copy(grid3), start, goal)
    if path3:
        probability3 = np.random.uniform(0.1, 1.0)  # Random probability for demonstration
        all_paths3.append(path3)
        all_probabilities3.append(probability3)

if all_paths1 and all_paths2 and all_paths3:
    print(f"{len(all_paths1)} Paths found for Grid 1:")
    for i, (path, probability) in enumerate(zip(all_paths1, all_probabilities1)):
        print(f"Path {i + 1}: {path}, Probability: {probability:.2f}")

    print(f"\n{len(all_paths2)} Paths found for Grid 2:")
    for i, (path, probability) in enumerate(zip(all_paths2, all_probabilities2)):
        print(f"Path {i + 1}: {path}, Probability: {probability:.2f}")

    print(f"\n{len(all_paths3)} Paths found for Grid 3:")
    for i, (path, probability) in enumerate(zip(all_paths3, all_probabilities3)):
        print(f"Path {i + 1}: {path}, Probability: {probability:.2f}")

    plot_paths([grid1, grid2, grid3], [all_paths1, all_paths2, all_paths3], [all_probabilities1, all_probabilities2, all_probabilities3])
else:
    print("No paths found.")
