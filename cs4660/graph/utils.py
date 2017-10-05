"""
utils package is for some quick utility methods
such as parsing
"""
import graph as gr
from search import searches
from time import time

class Tile(object):
    """Node represents basic unit of graph"""
    def __init__(self, x, y, symbol):
        self.x = x
        self.y = y
        self.symbol = symbol

    def __str__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)
    def __repr__(self):
        return 'Tile(x: {}, y: {}, symbol: {})'.format(self.x, self.y, self.symbol)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y and self.symbol == other.symbol
        return False
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(self.x) + str(self.y) + self.symbol)



def parse_grid_file(graph, file_path):
    """
    ParseGridFile parses the grid file implementation from the file path line
    by line and construct the nodes & edges to be added to graph
    Returns graph object
    """
    # TODO: read the filepaht line by line to construct nodes & edges
    f = open(file_path, "r")
    nodes =[]
    edges = []
    if f.mode == 'r':
        fl = f.readlines()
        length = len(fl)
        for i in range(1, length-1, 1):
            k = -1
            for j in range(1, len(fl[i])-2, 2):
               k +=1
               if fl[i][j] == "#":
                   continue
               else:
                   tile = Tile(k, i-1, fl[i][j] + "" + fl[i][j+1])
                   graph.add_node(gr.Node(tile))
                   if i > 1:
                       if fl[i-1][j] != "#":
                           to_tile = Tile(k, i-2, fl[i-1][j] + "" + fl[i-1][j+1])
                           edges.append(gr.Edge(gr.Node(tile), gr.Node(to_tile), 1))
                   if i < length - 2:
                       if fl[i+1][j] !="#":
                           to_tile = Tile(k, i, fl[i+1][j] + "" + fl[i+1][j+1])
                           edges.append(gr.Edge(gr.Node(tile), gr.Node(to_tile), 1))
                   if j < len(fl[i])-4:
                       if fl[i][j+2] != "#":
                           to_tile = Tile(k+1, i-1, fl[i][j+2] + "" + fl[i][j+3])
                           edges.append(gr.Edge(gr.Node(tile), gr.Node(to_tile), 1))
                   if j > 1:
                       if fl[i][j - 1] != "#":
                           to_tile = Tile(k-1, i-1, fl[i][j - 2] + "" + fl[i][j - 1])
                           edges.append(gr.Edge(gr.Node(tile), gr.Node(to_tile), 1))

        for edge in edges:
            graph.add_edge(edge)
    #TODO: for each node/edge above, add it to graph

    return graph

def convert_edge_to_grid_actions(edges):
    """
    Convert a list of edges to a string of actions in the grid base tile
    e.g. Edge(Node(Tile(1, 2), Tile(2, 2), 1)) => "S"
    """
    chars = []
    for edge in edges:
        if edge.to_node.data.x == edge.from_node.data.x:
            if edge.to_node.data.y > edge.from_node.data.y:
                chars.append("S")
            else:
                chars.append("N")
        else:
            if edge.to_node.data.x > edge.from_node.data.x:
                chars.append("E")
            else:
                chars.append("W")
    return ''.join(chars)

""""
graph = parse_grid_file(gr.ObjectOriented(), '../test/fixtures/grid-1.txt')
timeStart = time()
searches.dijkstra_search(graph, gr.Node(Tile(4, 4, "@6")), gr.Node(Tile(3, 0, "@1")))
totalD = time() - timeStart

timeStart = time()
searches.a_star_search(graph, gr.Node(Tile(4, 4, "@6")), gr.Node(Tile(3, 0, "@1")))
totalA = time() - timeStart

print "dijikstra = " + str(totalD * 1000) + " " + "Astar = " + str(totalA *1000)


#graph.neighbors(gr.Node(Tile(4, 4, "@6")))
print searches.dijkstra_search(graph, gr.Node(Tile(4, 4, "@6")), gr.Node(Tile(3, 0, "@1")))

for node in g.nodes:
    print node

edges = [gr.Edge(gr.Node(Tile(3, 0, "@1")), gr.Node(Tile(3, 1, "  ")), 1),
         gr.Edge(gr.Node(Tile(3, 1, " ")), gr.Node(Tile(3, 2, "  ")), 1),
         gr.Edge(gr.Node(Tile(3, 2, " ")), gr.Node(Tile(3, 3, "  ")), 1),
         gr.Edge(gr.Node(Tile(3, 3, " ")), gr.Node(Tile(3, 4, "  ")), 1),
         gr.Edge(gr.Node(Tile(3, 4, " ")), gr.Node(Tile(4, 4, "  ")), 1)]
print convert_edge_to_grid_actions(edges)
"""