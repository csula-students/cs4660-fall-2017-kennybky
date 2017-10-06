"""
Searches module defines all different search algorithms
"""
import math

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = [initial_node]
    visited = [initial_node]
    parents = {}
    while q:
        node = q.pop(0)
        for child in graph.neighbors(node):
            if child == dest_node:
                visited.append(child)
                parents[child] = node
                return print_path(graph, initial_node, dest_node, [], parents)
            elif child not in visited:
                visited.append(child)
                parents[child] = node
                q.append(child)
            else:
                continue


def print_path(graph, initial_node, dest_node, path, parents):
    if dest_node not in parents:
        return None
    if dest_node == initial_node:
        return path
    elif parents[dest_node] is None:
        return None
    else:
        path.insert(0, graph.get_edge(parents[dest_node], dest_node))
        print_path(graph, initial_node, parents[dest_node], path, parents)
        return path


def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    parents = []
    visited = [initial_node]
    depth_first(graph, initial_node, dest_node, parents, visited)
    return parents

def depth_first(graph, current, dest_node, parents, visited):
    for node in graph.neighbors(current):
        if node in visited:
            continue
        elif node == dest_node:
            parents.insert(0, graph.get_edge(current, node))
            return True
        else:
            visited.append(node)
            found = depth_first(graph, node, dest_node, parents, visited)
            if found:
                parents.insert(0,graph.get_edge(current, node))
                return True
    return False


def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = [initial_node]
    parents = {initial_node: None}
    distance = {initial_node: 0}
    while q:
        node = extract_min(q, distance)
        for child in graph.neighbors(node):
            if child not in distance.keys():
                distance[child] = float("inf")
                q.append(child)
            if distance[child] >  (distance[node] + graph.distance(node, child)):
                distance[child] = (distance[node] + graph.distance(node, child))
                parents[child] = node
    return print_path(graph, initial_node, dest_node, [], parents)


def extract_min(q, distance):
    minimum = q[0]
    for node in q:
        if distance[node] < distance[minimum]:
            minimum = node
    q.remove(minimum)
    return minimum


def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    parents = {initial_node: None}
    priority = {}
    distance = {}
    for n in graph.nodes:
        priority[n] = float("inf")
        distance[n] = float("inf")
    distance[initial_node] = 0
    priority[initial_node] = 0
    q = PriorityQueue()
    q.insert(initial_node, priority)
    while q.queue:
        node = q.extract_min(priority)
        if node == dest_node:
            break
        for child in graph.neighbors(node):
            new_cost = distance[node] + graph.distance(node, child)
            if new_cost < distance[child]:
                distance[child] = new_cost
                p = new_cost + heuristic(child, dest_node)
                priority[child] = p
                parents[child] = node
                q.insert(child, priority)
    return print_path(graph, initial_node, dest_node, [], parents)

def heuristic(node, goal):
    dx = abs(node.data.x - goal.data.x)
    dy = abs(node.data.y - goal.data.y)
   #D is a scale value for you to adjust performance vs accuracy
    return 1 * (dx + dy)


class PriorityQueue(object):
    def __init__(self):
        self.queue = []

    def parent(self, i):
        return int(math.ceil((i/float(2)) - 1))

    def left(self, i):
        return (2 * i) + 1

    def right(self, i):
        return (2 * i) + 2

    def extract_min(self, priority):
        if len(self.queue) > 0:
            minimum = self.queue[0]
            self.queue[0] = self.queue[len(self.queue)-1]
            self.queue.pop(len(self.queue)-1)
            self.min_heapify(0, priority)
            return minimum
    def min_heapify(self, i, priority):
        l = self.left(i)
        r = self.right(i)
        if l < len(self.queue) and priority[self.queue[l]] < priority[self.queue[i]]:
            largest = l
        else:
            largest = i
        if r < len(self.queue) and priority[self.queue[r]] < priority[self.queue[largest]]:
            largest = r
        if largest != i:
            temp = self.queue[i]
            self.queue[i] = self.queue[largest]
            self.queue[largest] = temp
            self.min_heapify(largest, priority)

    def reduce_key(self, i, priority):
          while i > 0 and priority[self.queue[self.parent(i)]] > priority[self.queue[i]]:
              temp = self.queue[i]
              self.queue[i] = self.queue[self.parent(i)]
              self.queue[self.parent(i)] = temp
              i = self.parent(i)
    def insert(self, key, priority):
        self.queue.append(key)
        i = len(self.queue) -1
        self.reduce_key(i, priority)

    def build_min_heap(self, a, priority):
        for node in a:
            self.queue.append(node)
        start = self.parent(len(a)-1)
        for i in range(start, -1, -1):
            self.min_heapify(i, priority)

