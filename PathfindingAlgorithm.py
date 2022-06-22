from random import randint
import numpy as np


def generate_env_grid(start: tuple, end: tuple, obstacles: list,
                      height: int = 10, width: int = 10):
    """
    Create a matrix describing the environment which is to be navigated

    :param start: where navigation starts
    :param end: where navigation ends
    :param obstacles: the objects to be avoided
    :param height: the height of the environment    (y-axis)
    :param width: the width of the environment      (x-axis)
    :return: created environment matrix
    """

    # create grid
    env_grid = np.zeros((height, width))

    # add start and end points
    env_grid[start] = 4
    env_grid[end] = 5

    # populate with obstacles
    for position in obstacles:
        env_grid[position] = 1

    return env_grid


def add_random_obstacles(grid, num_obstacles: int = 20):
    height, width = np.shape(grid)
    obstacles_added = []

    for i in range(num_obstacles):
        while True:
            coord = (randint(0, height-1), randint(0, width-1))

            if grid[coord] not in {1, 4, 5}:
                # the position is not an obstacle, the stat, or the stop
                grid[coord] = 1
                obstacles_added.append(coord)
                break

    return grid, obstacles_added


def generate_steps_grid(env_grid, start_pos: tuple):
    height, width = np.shape(env_grid)

    # set all the position with an unknown number of moves to -1
    # set the start position to 0

    moves_grid = -1*np.ones((height, width))
    moves_grid[start_pos] = 0

    return moves_grid


def next_steps(moves_grid, env_grid, n: int) -> list:
    height, width = np.shape(moves_grid)
    n_move_positions = []
    surrounding_positions = []

    # find the positions reached in n steps
    for i in range(height):
        for j in range(width):
            if moves_grid[(i, j)] == n:
                n_move_positions.append((i, j))

    # find the positions surrounding those places
    for i, j in n_move_positions:
        surrounding_positions.extend([
            (i+1, j+1),
            (i+1, j),
            (i+1, j-1),
            (i, j+1),
            (i, j-1),
            (i-1, j+1),
            (i-1, j),
            (i-1, j-1),
        ])

    # take out invalid surrounding positions
    valid_positions = set()
    for i, j in surrounding_positions:
        if (i not in range(0, height)) or (j not in range(0, width)):
            # then position is outside grid
            pass

        elif env_grid[(i, j)] == 1:
            # the position is coincides with an obstacle
            pass

        elif -1 < moves_grid[(i, j)] <= n:
            # the position can be reached in fewer moves
            pass

        else:
            # add pos to valid set
            valid_positions.add((i, j))

    # update the position grid
    for position in valid_positions:
        moves_grid[position] = n + 1

    return moves_grid


def get_all_steps(moves_grid, env_grid, end_pos, step_limit: int = 100):
    n = 0
    while moves_grid[end_pos] == -1:
        moves_grid = next_steps(moves_grid, env_grid, n=n)
        n += 1

        if n == step_limit:
            print("The end position is unreachable")
            break

    return moves_grid


def unfilled_positions(env_grid, position):
    i, j = position
    height, width = np.shape(env_grid)

    surrounding_positions = [
        (i+1, j+1),
        (i+1, j),
        (i+1, j-1),
        (i, j+1),
        (i, j-1),
        (i-1, j+1),
        (i-1, j),
        (i-1, j-1),
    ]

    valid_positions = set()

    for i, j in surrounding_positions:
        if (i not in range(0, height)) or (j not in range(0, width)):
            # then position is outside grid
            pass

        elif env_grid[(i, j)] == 1:
            # the position coincides with an obstacle
            pass

        else:
            # add pos to valid set
            valid_positions.add((i, j))

    return list(valid_positions)


def shortest_path(moves_grid, env_grid, end_pos, start_pos):
    path = [end_pos]
    current_position = end_pos

    while True:
        # determine all points around current position
        # and find the one with the lowest valid value

        adj_positions = unfilled_positions(env_grid, current_position)
        lowest_value_position = adj_positions[0]
        lowest_value = moves_grid[lowest_value_position]

        for position in adj_positions:
            if -1 < moves_grid[position] < lowest_value:
                lowest_value = moves_grid[position]
                lowest_value_position = position

        path.append(lowest_value_position)
        current_position = lowest_value_position

        if current_position == start_pos:
            path.reverse()
            return path


##############################################################################
##############################################################################

# generate the frameworks
OBS = [(9, 7), (8, 7), (6, 7), (6, 8)]
NUM_RAND_OBS = 20
END = (9, 9)
START = (0, 0)
ROWS = 10
COLS = 10

environment_grid = generate_env_grid(start=START, end=END, obstacles=OBS,
                                     height=ROWS, width=COLS)
steps_grid = generate_steps_grid(environment_grid, START)

########################################################################
# Phase 1
print("PHASE 1: calculate a valid path which avoids the given obstacles")

print("The environment for this question is visualised below!\n"
      "4 represents the starting position, 5 represents the delivery\n"
      "position, 1 represents an obstacle, and 0 an empty position.\n")
print(environment_grid, end="\n"*2)

steps_grid = get_all_steps(steps_grid, environment_grid,
                           END, step_limit=ROWS*COLS)
print("The graph below represents how many 'moves' it takes to get to \n"
      "each grid position. -1 represents that a position cannot \n"
      "be reached\n")
print(steps_grid, end="\n"*2)


print("One of the optimum paths to the delivery point from the start is:")
sp = shortest_path(steps_grid, environment_grid, END, START)
print(sp, end="\n"*2)


########################################################################
# Phase 2
print("#"*80, "#"*80, sep="\n", end="\n"*2)
print("PHASE 2: calculate a valid path which avoids the given obstacles")

environment_grid, new_ob = add_random_obstacles(environment_grid, NUM_RAND_OBS)
print(f"The environment grid with {NUM_RAND_OBS} extra obstacles is:\n")
print(environment_grid, end="\n"*2)
print("The extra obstacles are:", new_ob)

print("The steps gird is:\n")
steps_grid = generate_steps_grid(environment_grid, START)
steps_grid = get_all_steps(steps_grid, environment_grid,
                           END, step_limit=ROWS*COLS)
print(steps_grid, end="\n"*2)


# determine the path
if steps_grid[END] != -1:
    print("One of the optimum paths to the delivery point is:\n")
    sp = shortest_path(steps_grid, environment_grid, END, START)
    print(sp, end="\n"*2)
else:
    print("It is not possible to get to the end location without\n"
          "moving an obstacle", end="\n"*2)

########################################################################
# Phase 3
print("#"*80, "#"*80, sep="\n", end="\n"*2)
print("PHASE 3: calculate minimum number of objects to be removed if \n"
      "otherwise impossible")

if steps_grid[END] == -1:
    print("the answer is probability 1 - i did make an attempt at this, but it"
          " is unfinished code")
else:
    print("current solutions has been given")
