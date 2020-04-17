from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# Inverse direction of backtracking.
inverse_direction = {
    'n': 's',
    's': 'n',
    'w': 'e',
    'e': 'w'
}

# Traverse the map to find paths recursively


def find_path(searched=[]):
    path = []

    for direction in player.current_room.get_exits():
        player.travel(direction)
        # if current room hasn't been searched/traversed
        # add it to searched list to keep track
        # add direction traveled to path to keep track
        if player.current_room.id not in searched:
            searched.append(player.current_room.id)
            path.append(direction)
            path = path + find_path(searched)
            player.travel(inverse_direction[direction])
            path.append(inverse_direction[direction])
        else:
            player.travel(inverse_direction[direction])

    return path


traversal_path = find_path()

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#    cmds = input("-> ").lower().split(" ")
#    if cmds[0] in ["n", "s", "e", "w"]:
#        player.travel(cmds[0], True)
#    elif cmds[0] == "q":
#        break
#    else:
#        print("I did not understand that command.")
