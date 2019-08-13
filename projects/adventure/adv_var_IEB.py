from roomGraphs import roomGraph3, roomGraph6, roomGraph9, roomGraph12, roomGraph18, roomGraph18startOnLoop, roomGraph20, roomGraph500, roomGraph10000
from room import Room
from player import Player
from world import World

import random
import collections
import copy
import time

''' Choose roomGraph here '''
roomGraph = roomGraph500
''' Choose roomGraph here '''

# Load world
world = World()
world.loadGraph(roomGraph)

# UNCOMMENT TO VIEW MAP
world.printRooms()

player = Player("Name", world.startingRoom)

# Fill this out

traversalPath = []

# For rooms with > 1 '?'s, the function must decide which '?' to explore first. The following are the 24 possible orders for the four cardinal directions. Each of the 24 orders is tested in the maze, and the one that yields the shortest path (or the first one if there's a tie) is returned.
dir_orders = [[w, x, y, z] for w in ['n', 'e', 's', 'w'] for x in ['n', 'e', 's', 'w'] for y in [
    'n', 'e', 's', 'w'] for z in ['n', 'e', 's', 'w'] if w != x and w != y and w != z and x != y and x != z and y != z]

# dir_orders = [['n', 'e', 's', 'w']]

opp_dirs = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}


def maze_traversal(num_rooms=500):
    print('Phase 1')
    traversalPath, graph, next_dir, prev_room, prev_dir = [], dict(), None, None, None

    # Fill in graph
    while True:
        cur, unexp_dir = player.currentRoom, False

        if cur.id not in graph:
            graph[cur.id] = {
                dir: '?' for dir in cur.getExits()}

        if len(graph) > 1:
            graph[prev_room][next_dir] = cur.id
            graph[cur.id][prev_dir] = prev_room

        for dir in dir_orders[0]:
            if dir in graph[cur.id] and graph[cur.id][dir] == '?':
                next_dir = dir
                unexp_dir = True
                break

        if unexp_dir == False:
            visited, q = set(), collections.deque([[cur.id]])
            while len(q) > 0:
                path = q.popleft()
                room = path[-1]

                if '?' in graph[room].values():
                    for dir in range(len(path) - 2):
                        traversalPath.append(path[dir])
                        player.travel(path[dir])
                    next_dir = path[-2]
                    break

                if room not in visited:
                    visited.add(room)
                    for dir, id in graph[room].items():
                        path_copy = list(path)
                        path_copy[-1] = dir
                        path_copy.append(id)
                        q.append(path_copy)

        prev_room = player.currentRoom.id
        prev_dir = opp_dirs[next_dir]

        if len(graph) == num_rooms:
            question = False
            for room in graph:
                for door in graph[room].values():
                    if door == '?':
                        question = True
            if question == False:
                break

        traversalPath.append(next_dir)
        player.travel(next_dir)

    # Fill in DEBRS
    print('Phase 2')
    DEBRs = copy.deepcopy(graph)
    for room in DEBRs:
        for door in DEBRs[room]:
            DEBRs[room][door] = None
    player.currentRoom = world.startingRoom

    for next_dir in traversalPath:
        cur = player.currentRoom
        for door in cur.getExits():
            # If door hasn't been tested for DEBR, test it
            if DEBRs[cur.id][door] == None:
                # Perform search for path to cur.id starting in the next room, forbidding return by the same door
                visited, q = set(), collections.deque(
                    [[cur.getRoomInDirection(door).id]])
                DEBR = True
                while len(q) > 0:
                    path = q.popleft()
                    room = path[-1]

                    if room == cur.id:
                        DEBR = False
                        break

                    if room not in visited:
                        visited.add(room)
                        for dir, id in graph[room].items():
                            if room == cur.getRoomInDirection(door).id and dir == opp_dirs[door]:
                                continue
                            else:
                                path_copy = list(path)
                                path_copy[-1] = dir
                                path_copy.append(id)
                                q.append(path_copy)

                if DEBR == True:
                    DEBRs[cur.id][door] = len(visited)
                    DEBRs[cur.getRoomInDirection(
                        door).id][opp_dirs[door]] = False
                else:
                    ''' 
                    This is where cycles get their weight. 0 means cycles are favored.
                    False means they're put off until every other direction is explored.
                    In some maps 0 gets a better score, and in some False does. My suspicion is that the starting room location in relation to any cycles is important.
                    '''
                    DEBRs[cur.id][door] = False
        player.travel(next_dir)
    # print(graph)

    # print(DEBRs)

    # Traverse again, obeying DEBRs
    print('Phase 3')

    # longest_DEB = room, direction, score
    longest_DEB = [float('inf'), None, float('-inf')]

    for room in DEBRs:
        for dir in DEBRs[room]:
            if DEBRs[room][dir] > longest_DEB[-1]:
                longest_DEB = [room, dir, DEBRs[room][dir]]

    print('longest_DEB: ', longest_DEB)
    print('DEBRs for whole room of the longest_DEB: ', DEBRs[longest_DEB[0]])
    print('DEBRs: ', DEBRs)

    shortest_traversalPath = []
    shortest_dir_order = None

    for dir_order in dir_orders:
        DEBRs_copy = copy.deepcopy(DEBRs)
        current_traversalPath = []
        player.currentRoom = world.startingRoom
        DEBR_values = collections.deque([[float('inf'), float('inf')]])
        new_graph = dict()
        next_dir = None
        prev_room = None

        while True:
            # print('next_dir: ', next_dir, 'current_room: ', player.currentRoom.id)
            new_dir = False
            DEB_candidates = []

            if player.currentRoom.id not in new_graph:
                new_graph[player.currentRoom.id] = {
                    dir: '?' for dir in player.currentRoom.getExits()}
                if len(new_graph) == num_rooms:
                    if len(shortest_traversalPath) == 0 or len(current_traversalPath) < len(shortest_traversalPath):
                        shortest_traversalPath = copy.deepcopy(
                            current_traversalPath)
                        shortest_dir_order = dir_order
                    break
            # print('prev_room: ', prev_room)

            if player.currentRoom.id == DEBR_values[-1][0] and prev_room == player.currentRoom.getRoomInDirection(DEBR_values[-1][-1]).id:
                # print('back to room', DEBR_values)
                # print(current_traversalPath)
                DEBR_values.pop()
                # print(player.currentRoom.id)
                # print(prev_dir)
                DEBRs_copy[player.currentRoom.id][prev_dir] = False
                # print('DEBRs_copy: ', DEBRs_copy)
                # print(DEBR_values)

            if len(new_graph) > 1:
                new_graph[prev_room][next_dir] = player.currentRoom.id
                new_graph[player.currentRoom.id][prev_dir] = prev_room

            for dir in dir_order:
                if dir in new_graph[player.currentRoom.id] and new_graph[player.currentRoom.id][dir] == '?' and type(DEBRs_copy[player.currentRoom.id][dir]) == int:
                    DEB_candidates.append(
                        [dir, DEBRs_copy[player.currentRoom.id][dir]])

            if len(DEB_candidates) > 0:
                # print('DEB_candidates', DEB_candidates)
                # print(new_graph)
                new_DEB = DEB_candidates[0]
                for candidate in DEB_candidates:
                    # print('new_DEB', new_DEB, 'candidate', candidate)
                    if candidate[-1] < new_DEB[-1]:
                        new_DEB = candidate
                DEBR_values.append([player.currentRoom.id, new_DEB[0]])
                # print('new DEBR: ', DEBR_values)
                next_dir = new_DEB[0]
                # print('NEXT', next_dir, new_DEB)
                new_dir = True

            if new_dir == False:
                for dir in dir_order:
                    if dir in new_graph[player.currentRoom.id] and new_graph[player.currentRoom.id][dir] == '?':
                        next_dir = dir
                        new_dir = True
                        break

            if new_dir == False:
                visited, q = set(), collections.deque(
                    [[player.currentRoom.id]])
                while len(q) > 0:
                    path = q.popleft()
                    room = path[-1]

                    if '?' in new_graph[room].values():
                        for dir in range(len(path) - 2):
                            prev_room = player.currentRoom.id
                            prev_dir = opp_dirs[path[dir]]
                            current_traversalPath.append(path[dir])
                            player.travel(path[dir])
                            if len(DEBR_values) > 1:
                                # print('DEBR VALUES VALUES VALUES: ', DEBR_values, player.currentRoom.id, prev_room)
                                # print(player.currentRoom.getRoomInDirection(opp_dirs[DEBR_values[-1][-1]]))
                                if player.currentRoom.id == DEBR_values[-1][0] and prev_room == player.currentRoom.getRoomInDirection(DEBR_values[-1][-1]).id:
                                    DEBR_values.pop()
                                    DEBRs_copy[player.currentRoom.id][prev_dir] = False
                        next_dir = path[-2]
                        break

                    if room not in visited:
                        visited.add(room)
                        for dir, id in new_graph[room].items():
                            path_copy = list(path)
                            path_copy[-1] = dir
                            path_copy.append(id)
                            q.append(path_copy)

            prev_room = player.currentRoom.id
            prev_dir = opp_dirs[next_dir]
            # print('REALLY THE next_dir: ', next_dir)
            current_traversalPath.append(next_dir)
            player.travel(next_dir)

        print(dir_order, ':', len(current_traversalPath))

    print('shortest_dir_order: ', shortest_dir_order)
    print('shortest_traversalPath: ', shortest_traversalPath)
    return shortest_traversalPath


start_time = time.time()
traversalPath = maze_traversal(len(roomGraph))
end_time = time.time()

# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)

for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(
        f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")

print(end_time - start_time, 'seconds')

#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == 'q':
#         break
#     else:
#         print("I did not understand that command.")
