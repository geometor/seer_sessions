"""
1.  **Identify Green and Red:** Locate all contiguous blocks of green (3) and red (2) pixels in the input grid.

2.  **Determine Relative Position:** Note that every green pixel is to the *left* of a red pixel. Because input grids have multiple rows, consider "left" as the same row, or any row above.

3. **Simplify and Create Gray Regions:** From the top-left, find the most-up-and-left green pixel. Trace a diagonal down-and-right using the green pixels location as a starting point, and replace all green with gray. If a red pixel exist on the diagonal down-and-right of the green pixel, also replace the red with gray.

4. **Background:** Preserve or fill the remaining cells with white (0).
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

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    input_grid = np.array(input_grid)  # Ensure it's a NumPy array
    output_grid = np.zeros_like(input_grid)  # Initialize with white (0)

    green_objects = find_objects(input_grid, 3)
    red_objects = find_objects(input_grid, 2)

    green_pixels = [pixel for obj in green_objects for pixel in obj]
    red_pixels = [pixel for obj in red_objects for pixel in obj]
    
    # find the most up and left green pixel
    if (len(green_pixels) > 0):
        green_pixels.sort() # sorts by row, then by column
        start_r, start_c = green_pixels[0]

        # replace all green with gray
        for r, c in green_pixels:
                output_grid[r,c] = 5

        # Trace diagonally down and right
        for i in range(min(input_grid.shape[0] - start_r, input_grid.shape[1] - start_c)):
           
            current_r = start_r + i
            current_c = start_c + i
            
            output_grid[current_r, current_c] = 5

            # check if any red exist on this diag
            for red_r, red_c in red_pixels:

                if (red_r == current_r and red_c == current_c):
                     output_grid[red_r, red_c] = 5

    return output_grid