"""
1.  **Locate Yellow:** Find all yellow (4) pixels in the input grid.
2.  **Initial Bounding Box:** Create the smallest rectangular bounding box that contains all yellow pixels.
3.  **Expand Bounding Box:** Expand the bounding box to the left and upwards. The expansion stops when it encounters a pixel that is *not* blue (1) or white (0).
4. **Extract Subgrid:** Create the output grid by copying the content of the input grid within the expanded bounding box coordinates.
"""

import numpy as np

def find_object(grid, color):
    # returns a list of coordinates
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(coords):
    # finds the bounding box of a set of coordinates
    min_y = np.min(coords[:, 0])
    max_y = np.max(coords[:, 0])
    min_x = np.min(coords[:, 1])
    max_x = np.max(coords[:, 1])
    return (min_y, min_x), (max_y, max_x)

def expand_bounding_box(grid, top_left, bottom_right):
    # Expands the bounding box to include contiguous white and blue pixels, upwards and left only.
    min_y, min_x = top_left
    max_y, max_x = bottom_right  # max_y and max_x are not modified in this version

    def is_valid(y, x):
        # check if pixel is in the grid
        return 0 <= y < grid.shape[0] and 0 <= x < grid.shape[1]

    def should_expand(y, x):
        # only expand to white or blue
        return (grid[y, x] == 0) or (grid[y, x] == 1)

    # Expand upwards
    while min_y > 0 and should_expand(min_y - 1, min_x):
        min_y -= 1

    # Expand left
    while min_x > 0 and should_expand(min_y, min_x - 1):
        min_x -= 1
        
    # Expand upwards (using max_x to ensure we expand up along the whole width of the initial bounding box.
    while min_y > 0 and should_expand(min_y - 1, max_x):
         min_y -= 1

    return (min_y, min_x), (max_y, max_x)

def transform(input_grid):
    # Find coordinates of yellow pixels (color 4).
    yellow_coords = find_object(input_grid, 4)

    # Determine the bounding box around the yellow region.
    top_left, bottom_right = get_bounding_box(yellow_coords)

    # Expand bounding box upwards and to the left, including blue and white.
    top_left, bottom_right = expand_bounding_box(input_grid, top_left, bottom_right)

    # Extract the sub-grid based on the expanded bounding box.
    output_grid = input_grid[top_left[0]:bottom_right[0]+1, top_left[1]:bottom_right[1]+1].copy()

    return output_grid