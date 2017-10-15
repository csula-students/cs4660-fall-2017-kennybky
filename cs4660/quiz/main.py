"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
from Queue import Queue
from Queue import PriorityQueue


# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def bfs(initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = Queue()
    q.put(initial_node)
    visited = [initial_node['id']]
    parents = {}
    edge_to = {}
    while not q.empty():
        node = q.get()
        for c in node['neighbors']:
            child = get_state(c['id'])
            edge = transition_state(node['id'], child['id'])
            if child['id'] == dest_node['id']:
                visited.append(child['id'])
                parents[child['id']] = node['id']
                edge_to[child['id']] = edge
                path = print_path(dest_node['id'], parents, edge_to)
                output_path(path, initial_node['id'])
                return
            elif child['id'] not in visited:
                visited.append(child['id'])
                parents[child['id']] = node['id']
                edge_to[child['id']] = edge
                q.put(child)
            else:
                continue


def print_path(node_id, parents, edge_to):
    path = []
    while node_id in parents:
        path.append(edge_to[node_id])
        node_id = parents[node_id]
    path.reverse()
    return path

def output_path(path, start):
    prev_id = start
    total = 0
    for p in path:
        prev_node = get_state(prev_id)
        next_id = p['id']
        total += p['event']['effect']
        print ("%s(%s):%s(%s): %i" % (prev_node['location']['name'], prev_id, p['action'], p['id'], p['event']['effect']))
        prev_id = next_id
    print("\nTotalHP: %i" % total)

def dijkstra_search(initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = PriorityQueue()
    q.put((0, initial_node))
    parents = {}
    distance = {initial_node: 0}
    edge_to = {}
    visited = []
    while not q.empty():
        node =get_state(q.get()[1])
        visited.append(node['id'])
        for child in node['neighbors']:
            edge = transition_state(node['id'], child['id'])
            weight = distance[node['id']] + int(edge['event']['effect'])
            if child['id'] not in visited and (child['id'] not in distance or weight > distance[child['id']]):
                q.put((-weight, child['id']))
                distance[child['id']] = weight
                parents[child['id']] = node['id']
                edge_to[child['id']] = edge
    path = print_path(dest_node, parents, edge_to)
    output_path(path, initial_node)

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


if __name__ == "__main__":
    # Your code starts here
    empty_room = get_state('7f3dc077574c013d98b2de8f735058b4')
    dest_room = get_state('f1f131f647621a4be7c71292e79613f9')
    print ("\nBFS Path")
    bfs(empty_room, dest_room)
    start = '7f3dc077574c013d98b2de8f735058b4'
    end = 'f1f131f647621a4be7c71292e79613f9'
    print ("\nDijkstra Path")
    dijkstra_search(start, end)




