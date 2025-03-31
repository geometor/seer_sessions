import numpy as np
def get_coords_for_color(grid, color):
    return set(tuple(coord) for coord in np.argwhere(np.array(grid) == color))