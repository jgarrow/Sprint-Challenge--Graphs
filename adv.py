from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from pprint import pprint

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
backtrack_path = []
visited = set()
num_rooms = len(room_graph)
opposite_directions = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

# add to visited while there are still rooms we haven't visited
while len(visited) < num_rooms:
    exit_direction = None
    exits = player.current_room.get_exits()

    for direction in exits:
        # if the direction hasn't been visited yet, let's go there
        if player.current_room.get_room_in_direction(direction) not in visited:
            exit_direction = direction
            break
    
    # if the exit direction is valid/not a dead end
    if exit_direction is not None:
        # add the direction to our traversal path
        traversal_path.append(exit_direction)

        # add the opposite direction to our backtrack path
        backtrack_path.append(opposite_directions[exit_direction])

        # have the player travel in the exit_direction
        player.travel(exit_direction)

        # add the new room that we're in to our visited graph
        visited.add(player.current_room)

    # if the exit_direction is a dead end
    else:
        # we need to go backwards -- grab the most recently added direction from the backtrack path
        exit_direction = backtrack_path.pop()

        # add our new exit_direction to the traversal path
        traversal_path.append(exit_direction)

        # have the player travel in the exit_direction
        player.travel(exit_direction)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
