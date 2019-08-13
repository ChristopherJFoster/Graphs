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

# For rooms with > 1 unexplored directions, we must decide which unexplored direction to explore first. The following are the 24 possible orders for the four cardinal directions. Each of the 24 orders is tested in the maze, and the one that yields the shortest path (or the first one if there is a tie) is returned.
dir_orders = [[w, x, y, z] for w in ['n', 'e', 's', 'w'] for x in ['n', 'e', 's', 'w'] for y in [
    'n', 'e', 's', 'w'] for z in ['n', 'e', 's', 'w'] if w != x and w != y and w != z and x != y and x != z and y != z]

# This dictionary is convenient for calculating the direction of the room we just exited, which is useful for filling out the graph of the maze.
opp_dirs = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}


def maze_traversal(num_rooms=500):

    print('\nPhase 1: Initial Traversal\n')
    # This is a first pass through the maze to build the graph.

    traversalPath = []
    graph = dict()
    next_dir, prev_room, prev_dir = None, None, None
    finished = False

    # Build the graph
    while True:
        current = player.currentRoom
        unexp_dir = False

        if current.id not in graph:
            graph[current.id] = {
                dir: '?' for dir in current.getExits()}

        if len(graph) > 1:
            graph[prev_room][next_dir] = current.id
            graph[current.id][prev_dir] = prev_room

        # For this first pass, we always move in an unexplored direction, of which there can be 1 - 4 in any room (though only the starting room could have 4). When there are > 1 unexplored directions, we must decide which among them to prioritize. Since this is a first pass, we can't know which set of dir_orders might be optimal, so we use the first one: ['n', 'e', 's', 'w'].
        for dir in dir_orders[0]:
            if dir in graph[current.id] and graph[current.id][dir] == '?':
                next_dir = dir
                unexp_dir = True
                break

        # If there are no unexplored directions in the current room, we perform a breadth-first search (BFS) to find the nearest room with an unexplored dir (as well as the shortest path to that room). Once the path is determined, we follow that path.
        if unexp_dir == False:
            visited = set()
            q = collections.deque([[current.id]])

            while len(q) > 0:
                path = q.popleft()
                room = path[-1]

                if '?' in graph[room].values():
                    for dir in range(len(path) - 2):
                        traversalPath.append(path[dir])
                        player.travel(path[dir])
                    next_dir = path[-2]
                    # Before leaving BFS, make sure 'current' is up-to-date.
                    current = player.currentRoom
                    break

                if room not in visited:
                    visited.add(room)
                    for dir, id in graph[room].items():
                        path_copy = list(path)
                        path_copy[-1] = dir
                        path_copy.append(id)
                        q.append(path_copy)

        prev_room = current.id
        prev_dir = opp_dirs[next_dir]

        # We check to see if we are finished building the graph. First, have we visited each vertex?
        if len(graph) == num_rooms:
            finished = True
            # Next, have we filled in each each edge?
            for room in graph:
                for door in graph[room].values():
                    if door == '?':
                        finished = False
            if finished:
                break

        traversalPath.append(next_dir)
        player.travel(next_dir)

    print('Phase 2: Build dictionary of DEBRs (Dead End Branch Roots)\n')
    # Here we traverse the maze again in order to identify each 'dead end branch root' (DEBR). A DEBR is a room and direction combination (such as 145n) such that by travelling from that room in that direction one _must_ return to that room, from the opposite of that direction, in order to continue traversing the maze (i.e., the branch is a 'dead end branch' (DEB)). My key insight in achieving the 917-step traversal is that there is never a better time explore a DEB than when one is standing at its root. Phase 2 of my algorithm identifies every DEBR, and Phase 3 traverses the maze again while making sure to stop and explore every DEBR identified in Phase 2.

    DEBRs = copy.deepcopy(graph)
    for room in DEBRs:
        for door in DEBRs[room]:
            DEBRs[room][door] = None

    # Move player back to the starting room
    player.currentRoom = world.startingRoom

    for next_dir in traversalPath:
        current = player.currentRoom

        for door in current.getExits():
            # If door hasn't been tested for DEBR, test it
            if DEBRs[current.id][door] == None:
                # To determine if a room/dir combo is a DEBR, start in the next room (in the candidate direction). Perform a BFS for the current room while forbidding return by the same door. If the current room cannot be found, then the room/dir combo is a DEBR.
                visited, q = set(), collections.deque(
                    [[current.getRoomInDirection(door).id]])
                DEBR = True
                while len(q) > 0:
                    path = q.popleft()
                    room = path[-1]

                    if room == current.id:
                        # Another path back to the current room was discovered, so the room/dir is not a DEBR.
                        DEBR = False
                        break

                    if room not in visited:
                        visited.add(room)
                        for dir, id in graph[room].items():
                            if room == current.getRoomInDirection(door).id and dir == opp_dirs[door]:
                                continue
                            else:
                                path_copy = list(path)
                                path_copy[-1] = dir
                                path_copy.append(id)
                                q.append(path_copy)

                if DEBR == True:
                    # A room/dir combo is marked as a DEBR by an integer representing the size of the DEB (its number of rooms).
                    DEBRs[current.id][door] = len(visited)
                    # Any DEBR has a 'mirror' DEBR in the next room (if traveling north from room 34 leads to room 65, then if 34n is a DEBR, then so is 65s). However, these mirror DEBRs disrupt the algorithm used in Phase 3, and so they must be explicity marked as non-DEBRs:
                    DEBRs[current.getRoomInDirection(
                        door).id][opp_dirs[door]] = False
                else:
                    # Mark non-DEBRs as False.
                    DEBRs[current.id][door] = False

        player.travel(next_dir)

    print('Phase 3: New Traversal, always exploring DEBRs when encountered\n')
    # Here we traverse the maze again, this time exploring each DEBR as it is encountered. There is still the matter of which DEBR to explore when there are more than one in the same room. I test every combination of directions (24 total), keeping track of the number of steps taken, and return the shortest path (or the first path in the case of a tie).
    # I recognize that testing all direction combinations is a weakness of my solution - see 'Notes About Further Optimization' at the very bottom of this file for more information.

    print('[ Direction order  ]: # of steps')

    # Keep track of which of the direction orders yields the shortest path.
    shortest_traversalPath = []
    shortest_dir_order = None

    # Test each of the 24 direction orders.
    for dir_order in dir_orders:
        DEBRs_copy = copy.deepcopy(DEBRs)
        current_traversalPath = []
        player.currentRoom = world.startingRoom
        DEBR_values = collections.deque([[float('inf'), float('inf')]])
        new_graph = dict()
        next_dir = None
        prev_room = None

        while True:
            new_dir = False
            # DEBR_candidates covers cases where there is more than one DEBR in the same room.
            DEBR_candidates = []

            # This the same graph-building approach as in Phase 1.
            if player.currentRoom.id not in new_graph:
                new_graph[player.currentRoom.id] = {
                    dir: '?' for dir in player.currentRoom.getExits()}
                if len(new_graph) == num_rooms:
                    if len(shortest_traversalPath) == 0 or len(current_traversalPath) < len(shortest_traversalPath):
                        shortest_traversalPath = copy.deepcopy(
                            current_traversalPath)
                        shortest_dir_order = dir_order
                    break

            # As DEBRs are completed, mark them so they are not re-explored.
            if player.currentRoom.id == DEBR_values[-1][0] and prev_room == player.currentRoom.getRoomInDirection(DEBR_values[-1][-1]).id:
                DEBR_values.pop()
                DEBRs_copy[player.currentRoom.id][prev_dir] = False

            if len(new_graph) > 1:
                new_graph[prev_room][next_dir] = player.currentRoom.id
                new_graph[player.currentRoom.id][prev_dir] = prev_room

            # For each direction in a room, check if that direction is an unexplored DEBR (if a direction is an unexplored DEBR, it will have an integer value - otherwise its value will be False). If there are multiple DEBRs, the list will be populated according to the direction order currently being tested.
            for dir in dir_order:
                if dir in new_graph[player.currentRoom.id] and new_graph[player.currentRoom.id][dir] == '?' and type(DEBRs_copy[player.currentRoom.id][dir]) == int:
                    DEBR_candidates.append(
                        [dir, DEBRs_copy[player.currentRoom.id][dir]])

            # If there are any unexplored DEBRs in the current room, explore them.
            if len(DEBR_candidates) > 0:
                new_DEBR = DEBR_candidates[0]
                for candidate in DEBR_candidates:
                    if candidate[-1] < new_DEBR[-1]:
                        new_DEBR = candidate
                DEBR_values.append([player.currentRoom.id, new_DEBR[0]])
                next_dir = new_DEBR[0]
                new_dir = True

            # If there are no explored DEBRs in the current room, check for regular untraversed directions ('?'s) and go in one of those directions (according to the direction order currently being tested).
            if new_dir == False:
                for dir in dir_order:
                    if dir in new_graph[player.currentRoom.id] and new_graph[player.currentRoom.id][dir] == '?':
                        next_dir = dir
                        new_dir = True
                        break

            # Finally, if there are neither any unexplored DEBRs nor any regular untraversed directions in the current room, we perform a BFS to find the nearest untraversed direction (as well as the shortest path to its room). Once the path is determined, we follow that path.
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
            current_traversalPath.append(next_dir)
            player.travel(next_dir)

        # Prints the tested direction order and its step count (even if it is not the shortest path).
        print(f'{dir_order}: {len(current_traversalPath)}')

    # Once all 24 direction orders have been tested, print the direction order that yielded the shortest path (or the first, if there is a tie). Then print and return the set of directions for testing in the next section (per project guidelines).
    print(f'\nshortest_dir_order: {shortest_dir_order}')
    print(f'\nshortest_traversalPath:\n{shortest_traversalPath}')
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
        f'\nTESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited')
else:
    print('\nTESTS FAILED: INCOMPLETE TRAVERSAL')
    print(f'{len(roomGraph) - len(visited_rooms)} unvisited rooms')

print(f'\n{end_time - start_time} seconds')

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


# Notes About Further Optimization
# The rules of this maze traversal contest require us to generate a list a directions that, when followed, step into each room at least once. The moment the final room is entered, the traversal is complete - we need not return to the starting room. This means that there is likely further opportunity for optimization - roughly by ending our traversal as far from the starting room as possible.

# A simple example: Let's say our maze is a single row of 10 rooms, numbered from west to east 0 - 9. If the starting room is room 1, then there are two directions to explore: east and west (each direction is DEBR, in fact). Regardless of which direction is chosen first, we must return to the starting room in order to explore the other direction. This means that (in this example at least) we should explore in the direction with the fewest rooms. To the west, there is one room, while to the east there are eight rooms. The optimal traversal would begin by traveling west to room 0, then traveling east to room 9, resulting in a 10-step traversal (traveling east then west results in a suboptimal 17-step traversal).

# Though the above example is simple, I believe its principles apply to any graph whose branches, as measured from the starting room, are not of equal length. An optimal traversal, I hypothesize, would determine the ideal ending branch (IEB) for a traversal and its path would thus end in that branch. However, I have not yet implemented a solution that takes the IEB into account. I have, however, identified two problems in determining an IEB:
# 1. We must _only_ count the longest DEB within the branch as part of its IEB score, since all DEBs except one will have to be re-traversed.
# 2. The distance of the starting room to each candidate branch must be subtracted from that branch's IEB score, since every additional step taken to ensure that a candidate branch is last will (obviously) add to the length of the traversal.
