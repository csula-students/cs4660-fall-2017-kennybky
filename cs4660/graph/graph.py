"""
graph module defines the knowledge representations files

A Graph has following methods:

* adjacent(node_1, node_2)
    - returns true if node_1 and node_2 are directly connected or false otherwise
* neighbors(node)
    - returns all nodes that is adjacency from node
* add_node(node)
    - adds a new node to its internal data structure.
    - returns true if the node is added and false if the node already exists
* remove_node
    - remove a node from its internal data structure
    - returns true if the node is removed and false if the node does not exist
* add_edge
    - adds a new edge to its internal data structure
    - returns true if the edge is added and false if the edge already existed
* remove_edge
    - remove an edge from its internal data structure
    - returns true if the edge is removed and false if the edge does not exist
"""

from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    nodes = []
    edges = []
    f = open(file_path, "r")
    if f.mode == 'r':
        fl = f.readlines()
        length = int(fl[0])
        for i in range(length):
            nodes.append(Node(i))
        for x in range(1, len(fl), 1):
            data = fl[x].split(":")
            from_node = nodes[int(data[0])]
            to_node = nodes[int(data[1])]
            weight = int(data[2])
            edges.append(Edge(from_node, to_node, weight))

    for node in nodes:
        graph.add_node(node)
    for edge in edges:
        graph.add_edge(edge)
    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictionary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        if node_2 in self.adjacency_list[node_1]:
            return True
        else:
            return False

    def neighbors(self, node):
        return self.adjacency_list[node]

    def add_node(self, node):
        if node in self.adjacency_list.keys():
            return False
        else:
            self.adjacency_list[node] = []
            return True

    def remove_node(self, node):
        if node in self.adjacency_list.keys():
            for n in self.adjacency_list:
                if node in self.adjacency_list[n]:
                    self.adjacency_list[n].remove(node)
            del self.adjacency_list[node]
            return True
        else:
            return False

    def add_edge(self, edge):
        from_node = edge.from_node
        to_node = edge.to_node
        if from_node not in self.adjacency_list.keys() or to_node not in self.adjacency_list.keys():
            return False
        elif to_node in self.adjacency_list[from_node]:
            return False
        else:
            self.adjacency_list[from_node].append(to_node)
            return True

    def remove_edge(self, edge):
        from_node = edge.from_node
        to_node = edge.to_node
        if from_node not in self.adjacency_list.keys() or to_node not in self.adjacency_list.keys():
            return False
        elif to_node not in self.adjacency_list[from_node]:
            return False
        else:
            self.adjacency_list[from_node].remove(to_node)
            return True

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        return self.adjacency_matrix[node_1.data][node_2.data] == 1

    def neighbors(self, node):
        adj = self.adjacency_matrix[node.data]
        nodes = []
        for i in range(len(adj)):
            if adj[i] == 1:
                nodes.append(self.nodes[i])
        return nodes

    def add_node(self, node):
        if node in self.nodes:
            return False
        else:
            self.nodes.append(node)
            for x in range(len(self.adjacency_matrix)):
                self.adjacency_matrix[x].append(0)
            new_row = []
            for y in range(len(self.adjacency_matrix) + 1):
                new_row.append(0)
            self.adjacency_matrix.append(new_row)
            return True

    def remove_node(self, node):
        if node not in self.nodes:
            return False
        else:
            for x in self.adjacency_matrix[node.data]:
                x = None
            for y in self.adjacency_matrix:
                y[node.data] = None
            self.nodes.remove(node)
            return True

    def add_edge(self, edge):
        from_node = edge.from_node
        to_node = edge.to_node
        if to_node not in self.nodes or from_node not in self.nodes:
            return False
        elif self.adjacency_matrix[from_node.data][to_node.data] == 1:
            return False
        else:
            self.adjacency_matrix[from_node.data][to_node.data] = 1
            return True



    def remove_edge(self, edge):
        from_node = edge.from_node
        to_node = edge.to_node
        if self.adjacency_matrix[from_node.data][to_node.data] == 1:
            self.adjacency_matrix[from_node.data][to_node.data] = 0
            return True
        else:
            return False

    def __get_node_index(self, node):
        """helper method to find node index"""
        return node.data

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        neighbors = self.neighbors(node_1)
        if node_2 in neighbors:
            return True
        else:
            return False

    def neighbors(self, node):
        neighbors = []
        for e in self.edges:
            if e.from_node == node:
                neighbors.append(e.to_node)
        return neighbors

    def add_node(self, node):
        if node in self.nodes:
            return False
        else:
            self.nodes.append(node)
            return True

    def remove_node(self, node):
        for e in self.edges:
            if e.from_node == node or e.to_node == node:
                self.edges.remove(e)
        if node in self.nodes:
            self.nodes.remove(node)
            return True
        else:
            return False

    def add_edge(self, edge):
        if edge in self.edges:
            return False
        else:
            self.edges.append(edge)
            return True

    def remove_edge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)
            return True
        else:
            return False

