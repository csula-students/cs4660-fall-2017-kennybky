"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
from graph import graph
from Queue import Queue
from Queue import PriorityQueue

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.
    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = json.load(urlopen(req, jsondataasbytes))
    return response


def do_path(dest_node, parents, path, distance, cost):
    if parents[dest_node] is None:
        path.reverse()
        return path, cost
    else:
        child_name = dest_node.data[1]
        child_id = dest_node.data[0]
        parent_name = parents[dest_node].data[1]
        parent_id = parents[dest_node].data[0]
        weight = distance[dest_node]
        path.append(str(parent_name) + "(" + str(parent_id) + "):"
                    + str(child_name) + "(" + str(child_id) + "):" + str(weight))
        cost += weight
        return do_path(parents[dest_node], parents, path, distance, cost)


def bfs(g, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = Queue()
    q.put(initial_node)
    visited = [initial_node]
    parents = {}
    parents[initial_node] = None
    edge_to = {}
    distance = {}
    while not q.empty():
        node = q.get()
        for child in g.neighbors(node):
            weight = g.distance(node, child)
            if child == dest_node:
                visited.append(child)
                parents[child] = node
                distance[child] = weight
                path, cost = do_path(dest_node, parents, [], distance, 0)
                for p in path:
                    print p
                print "\nTotal HP " + str(cost)
                return
            elif child not in visited:
                visited.append(child)
                parents[child] = node
                distance[child] = weight
                #edge_to[child['id']] = edge
                q.put(child)
            else:
                continue

def dijkstra_search(g, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = PriorityQueue()
    q.put((0, initial_node))
    parents = {}
    parents[initial_node] = None
    distance = {initial_node: 0}
    edge_to = {}
    visited = []
    while not q.empty():
        node =q.get()[1]
        visited.append(node)
        for child in g.neighbors(node):
            edge = g.distance(node, child)
            weight = distance[node] + int(edge)
            if child not in visited and (child not in distance or weight > distance[child]):
                q.put((-weight, child))
                distance[child] = weight
                parents[child] = node
                edge_to[child] = edge
    path, cost = do_path(dest_node, parents, [], edge_to, 0)
    for p in path:
        print p
    print "\nTotal HP " + str(cost)

def parse_graph(start):
    g = graph.AdjacencyList()
    q = Queue()
    edges = []
    discovered = []
    q.put(start)
    discovered.append(start)
    while not q.empty():
        current = get_state(q.get())
        node = graph.Node((current['id'], current['location']['name']))
        g.add_grid_node(node)
        for child in current['neighbors']:
            if child['id'] not in discovered:
                q.put(child['id'])
                discovered.append(child['id'])
            state = transition_state(current['id'], child['id'])
            weight = state['event']['effect']
            to_node = graph.Node((child['id'], child['location']['name']))
            edge = graph.Edge(node, to_node, weight)
            edges.append(edge)
    for e in edges:
        g.add_grid_edge(e)
    return g


if __name__ == "__main__":
    start = '7f3dc077574c013d98b2de8f735058b4'
    end = 'f1f131f647621a4be7c71292e79613f9'
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dark_room = get_state('f1f131f647621a4be7c71292e79613f9')
    gr = parse_graph(start)
    initial = graph.Node((empty_room['id'], empty_room['location']['name']))
    dest = graph.Node((dark_room['id'], dark_room['location']['name']))
    print "\n\nBFS Path:"
    bfs(gr, initial, dest)
    print "\n\nDijkstra Path:"
    dijkstra_search(gr, initial, dest)