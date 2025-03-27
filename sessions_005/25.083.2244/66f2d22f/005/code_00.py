"""
1.  **Object Identification:** Identify all contiguous blocks of green (3) and red (2) pixels in the input grid.
2.  **Find Origins:** Determine the top-leftmost green pixel and the top-leftmost red pixel.
3.  **Calculate Column Difference:** Calculate the difference in column indices between the top-left red pixel and the top-left green pixel.
4.  **Output Grid:** Create an output grid of size 4x7, initially filled with white (0).
5.  **Create Gray Diagonal:** Starting from the top-left green pixel, create a diagonal line of gray (5) pixels extending downwards and to the right. The length of the diagonal is equal to the *column difference* calculated in step 3 + 1. It appears from example 4 that there is an exception when the leftmost green pixel is closer than the output width, the diagonal length extends across the entire grid.
6.  **Conditional Red Replacement:** Iterate through the red pixels. If a red pixel lies on the created gray diagonal, replace it with gray (5); otherwise, leave it unchanged (do not include in the output).
7. **Fill Background:** Ensure all remaining cells in the output grid are white (0).
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous blocks of a given color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def top_leftmost(pixels):
    """Returns the top-leftmost pixel from a list of pixels."""
    return min(pixels, key=lambda p: (p[0], p[1])) if pixels else None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros((4, 7), dtype=int)  # Fixed output size

    # find green and red objects
    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)

    # flatten into pixel lists
    green_pixels = [pixel for obj in green_objects for pixel in obj]
    red_pixels = [pixel for obj in red_objects for pixel in obj]

    # find top-left green and red
    top_left_green = top_leftmost(green_pixels)
    top_left_red = top_leftmost(red_pixels)

    # create diagonal
    if top_left_green:
        start_r, start_c = top_left_green

        # calculate column difference
        if top_left_red:
          column_diff = top_left_red[1] - start_c
        else:
          column_diff = 0

        # determine diagonal length, extends the entire grid
        diag_len = column_diff + 1

        # create diagonals
        for i in range(diag_len):
            current_r = start_r + i
            current_c = start_c + i

            if 0 <= current_r < 4 and 0 <= current_c < 7:
                output_grid[current_r, current_c] = 5

            # Conditional Red replacement
            if top_left_red:
                for red_r, red_c in red_pixels:
                  if red_r == current_r and red_c == current_c:
                      output_grid[red_r, red_c] = 5
    return output_grid