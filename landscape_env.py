"""
Create the environment and the functions which affect it

1 represent the presence of an obstacle
0 represents a clear path
4 start position
5 end position

Note that indexing is (row index (x-axis), column index (y-axis)). Printing
the transpose gives the same view as the challenge description
"""

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
    environment_grid = np.zeros((height, width))

    # add start and end points
    environment_grid[start] = 4
    environment_grid[end] = 5

    # populate with obstacles
    for position in obstacles:
        environment_grid[position] = 1

    return environment_grid


def add_random_obstacles(grid, num_obstacles: int = 20):
    height, width = np.shape(grid)

    for i in range(num_obstacles):
        while True:
            coord = (randint(0, height-1), randint(0, width-1))

            if grid[coord] not in {1, 4, 5}:
                grid[coord] = 1
                break

    return grid


def generate_moves_to_position(grid, start: tuple):
    height, width = np.shape(grid)

    # set all the position with an unknown number of moves to -1
    # set the start position to 0

    moves_grid = -1*np.ones((height, width))
    moves_grid[start] = 0

    return moves_grid


avoid_obj = [(9, 7), (8, 7), (6, 7), (6, 8)]
landscape = generate_env_grid(start=(0, 0), end=(9, 9), obstacles=avoid_obj)
landscape = add_random_obstacles(landscape, 0)

moves_to_positions = generate_moves_to_position(landscape, (0, 0))
