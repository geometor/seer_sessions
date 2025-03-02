"""
1.  **Identify Objects:** Find the green (3) "cross" shape and the red (2) pixels within it.
2.  **Red Pixel Duplication:** The red pixels are duplicated. For each original red pixel in the input, create four more copies in the output: One directly above, one directly below, one to the left, and one to the right. If green occupies the copy location, maintain green, only copy to white space.
3.  **Green Cross Expansion:** The green cross expands. From each exist green pixel, examine the spaces to it's left and right, and duplicate if white.
4. **Vertical Fill:** From each green pixel on the cross, scan upwards and downwards to any 0 and replace with a 3. Stop before other non-zero pixels.
"""

import numpy as np

def get_objects(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Identify red pixels
    red_pixels = get_objects(input_grid, 2)
    
    # Duplicate red pixels
    for r, c in red_pixels:
        neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
        for nr, nc in neighbors:
            if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 0:
                output_grid[nr, nc] = 2

    # Identify green pixels
    green_pixels = get_objects(input_grid, 3)

    # Expand green cross to the left and right
    for r, c in green_pixels:
        if c > 0 and output_grid[r,c-1] == 0:
            output_grid[r,c-1] = 3
        if c < cols -1 and output_grid[r, c+1] == 0:
            output_grid[r, c+1] = 3

    green_pixels = get_objects(output_grid, 3)

    # Vertical fill for green pixels
    for r, c in green_pixels:
        # Upwards
        for ur in range(r - 1, -1, -1):
            if output_grid[ur, c] == 0:
                output_grid[ur, c] = 3
            else:
                break
        # Downwards
        for dr in range(r + 1, rows):
            if output_grid[dr, c] == 0:
                output_grid[dr, c] = 3
            else:
                break

    return output_grid