"""
1.  **Identify** the inner magenta (6) shape (shape_2) and the surrounding yellow (4) shape. (shape_1).
2.  **Expand** the magenta shape (shape_2) outwards by one pixel in all four cardinal directions (up, down, left, right). The magenta shape will replace elements of the yellow shape.
3.  **Move** the entire combined shape, which now consists of expanded magenta, and the remaining yellow one row up.
4. Any rows that are above or below this area are not modified
"""

import numpy as np

def find_object(grid, color):
    # find coordinates of pixels with the specified color
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None
    return coords

def expand_shape(grid, shape_coords, color):
    # expand the shape defined by shape_coords by one pixel in all directions
    expanded_coords = set()
    for r, c in shape_coords:
        expanded_coords.add((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            expanded_coords.add((r + dr, c + dc))
    
    expanded_coords_list = list(expanded_coords)
    return expanded_coords_list


def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # find magenta shape
    magenta_coords = find_object(input_grid, 6)
    
    # expand magenta shape
    expanded_magenta_coords = expand_shape(input_grid, magenta_coords, 6)


    # apply expanded magenta, overwriting yellow
    for r, c in expanded_magenta_coords:
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
        output_grid[r, c] = 6

    # find yellow shape
    yellow_coords = find_object(input_grid, 4)
    
    # move up
    moved_grid = np.copy(output_grid) * 0
    
    for r,c in yellow_coords:
        if 0 <= r-1 < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
          if output_grid[r,c] == 4:
            moved_grid[r-1,c] = 4

    for r,c in expanded_magenta_coords:
        if 0 <= r-1 < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
            moved_grid[r-1,c] = 6

    #fill with original background above and below affected rows

    output_grid = np.copy(input_grid) * 0 #clear grid
    min_r = min(r for r, c in np.argwhere(moved_grid !=0))
    max_r = max(r for r, c in np.argwhere(moved_grid !=0))

    output_grid[min_r:max_r+1, :] = moved_grid[min_r:max_r+1,:]

    return output_grid