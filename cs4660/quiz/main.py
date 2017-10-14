"""
quiz2!

Use path finding algorithm to find your way through dark dungeon!

Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9

TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json

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
    q = [initial_node]
    visited = [initial_node['id']]
    parents = {}
    while q:
        node = q.pop(0)
        for c in node['neighbors']:
            child = get_state(c['id'])
            if child['id'] == dest_node['id']:
                visited.append(child['id'])
                parents[child['id']] = node['id']
                total = 0
                return print_path(initial_node['id'], dest_node['id'], [], parents, total)
            elif child['id'] not in visited:
                visited.append(child['id'])
                parents[child['id']] = node['id']
                q.append(child)
            else:
                continue


def print_path(initial_node, dest_node, path, parents, total):
    if dest_node == initial_node:
        return path
    elif parents[dest_node] is None:
        return None
    else:
        effect = transition_state(parents[dest_node], dest_node)['event']['effect']
        total += effect
        dest_name = get_state(dest_node)['location']['name']
        parent_name = get_state(parents[dest_node])['location']['name']
        path.insert(0, parent_name + "(" + parents[dest_node] + "):"
                    + dest_name + "(" + dest_node + "):" + str(effect))
        print_path(initial_node, parents[dest_node], path, parents, total)
        return path, effect

def dijkstra_search(initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    q = [initial_node]
    parents = {initial_node['id']: None}
    distance = {initial_node['id']: 0}
    visited = [initial_node['id']]
    while q:
        node = extract_min(q, distance)
        for child in node['neighbors']:
            if child in visited:
                continue
            if child['id'] not in distance.keys():
                distance[child['id']] = 0
                q.append(child)
            if distance[child['id']] < (distance[node['id']] + int(transition_state(node['id'], child['id'])['event']['effect'])):
                distance[child['id']] = (distance[node] + int(transition_state(node['id'], child['id'])['event']['effect']))
                parents[child['id']] = node['id']
    return print_path(initial_node['id'], dest_node['id'], [], parents)

def extract_min(q, distance):
    minimum = q[0]
    for node in q:
        if distance[node['id']] < distance[minimum['id']]:
            minimum = node
    q.remove(minimum)
    return minimum


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
    print(empty_room)
    #print (empty_room['neighbors'][1])
    #print (get_state(empty_room['neighbors'][1]['id']))
    print(transition_state(empty_room['id'], empty_room['neighbors'][0]['id']))
    print
    #print empty_room['location']['name']
    print bfs(empty_room, dest_room)
    #print dijkstra_search(empty_room, dest_room)
