# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 00:16:21 2023

@author: Muntadher
"""

import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, q, parent):
        self.q = q
        self.parent = parent

class RRT:
    def __init__(self, start, goal, obstacle_list, xlim, ylim, step_size):
        self.start = Node(start, None)
        self.goal = Node(goal, None)
        self.obstacle_list = obstacle_list
        self.nodes = [self.start]
        self.xlim = xlim
        self.ylim = ylim
        self.step_size = step_size
    
    def generate_random_node(self):
        return Node(np.array([np.random.uniform(self.xlim[0], self.xlim[1]), 
                              np.random.uniform(self.ylim[0], self.ylim[1])]), None)
    
    def nearest_node(self, q_rand):
        distances = [np.linalg.norm(node.q - q_rand.q) for node in self.nodes]
        return self.nodes[np.argmin(distances)]
    
    def new_node(self, q_near, q_rand):
        direction = q_rand.q - q_near.q
        distance = np.linalg.norm(direction)
        if distance > self.step_size:
            direction = direction / distance * self.step_size
        q_new = Node(q_near.q + direction, q_near)
        return q_new
    
    def is_collision_free(self, q_near, q_new):
        line = np.linspace(q_near.q, q_new.q, num=10)
        for q in line:
            for obstacle in self.obstacle_list:
                if obstacle.contains(q):
                    return False
        return True
    
    def plan(self, max_iter):
        for _ in range(max_iter):
            q_rand = self.generate_random_node()
            q_near = self.nearest_node(q_rand)
            q_new = self.new_node(q_near, q_rand)
            if self.is_collision_free(q_near, q_new):
                self.nodes.append(q_new)
                if np.linalg.norm(q_new.q - self.goal.q) < self.step_size:
                    self.goal.parent = q_new
                    return self.goal
        return None

class Obstacle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        
    def contains(self, point):
        return np.linalg.norm(point - self.center) <= self.radius

# Define the workspace boundaries
xlim = [0, 10]
ylim = [0, 10]

# Define the start and goal positions
start = np.array([1, 1])
goal = np.array([5, 8])

# Define the obstacles
obstacles = [Obstacle(np.array([5, 5]), 1), 
             Obstacle(np.array([7, 4]), 1),
             Obstacle(np.array([3, 7]), 1),
             Obstacle(np.array([2, 7]), 1)]

# Initialize the RRT planner
rrt = RRT(start, goal, obstacles, xlim, ylim, step_size=0.5)

# Plan the path
max_iter = 1000
result = rrt.plan(max_iter)

# Visualize the path
fig, ax = plt.subplots()
ax.set_xlim(xlim)
ax.set_ylim(ylim)

for obstacle in obstacles:
    circle = plt.Circle(obstacle.center, obstacle.radius, color='r')
    ax.add_artist(circle)

if result:
    path = [result.q]
    current_node = result.parent
    while current_node:
        path.append(current_node.q)
        current_node = current_node.parent
    path = np.array(path)
    ax.plot(path[:, 0], path[:, 1], 'b-')
    ax.plot(start[0], start[1], 'go', label='start')
    ax.plot(goal[0], goal[1], 'ro', label='goal')
    ax.legend()
else:
    print("Failed to find a path")

plt.show()


