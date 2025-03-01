"""
1.  **Identify Objects:** Locate the azure (8) pixel and the orange (7) pixel within the input grid.

2.  **Extend Azure:** Create a horizontal and a vertical line of azure (8) pixels, extending from the original azure pixel's position to the edges of the grid. The azure lines occupy the entire row and column of the initial azure pixel.

3.  **Extend Orange:**  Create a horizontal and vertical line of orange (7) pixels, extending in all directions from the original orange pixel's position to the edges of the grid. The orange lines occupy the entire row and column of the initial orange pixel.

4. **Place Red:** Determine the intersection point of the extended azure and orange lines. Place a red (2) pixel at this intersection point.

5. **Output:** The output is grid combining all actions.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    for r, row in enumerate(grid):
        for c, val in enumerate(row):
            if val == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid_size = len(input_grid)

    # Find azure and orange pixels
    azure_pos = find_pixel(input_grid, 8)
    orange_pos = find_pixel(input_grid, 7)

    if azure_pos is None or orange_pos is None:
      return output_grid

    # Extend azure lines
    if azure_pos:
        for i in range(grid_size):
            output_grid[azure_pos[0]][i] = 8  # Horizontal
            output_grid[i][azure_pos[1]] = 8  # Vertical

    # Extend orange lines
    if orange_pos:
        for i in range(grid_size):
            output_grid[orange_pos[0]][i] = 7  # Horizontal
            output_grid[i][orange_pos[1]] = 7  # Vertical
    
    # Place red pixel at intersection
    if azure_pos and orange_pos:
      output_grid[azure_pos[0]][orange_pos[1]] = 2
      output_grid[orange_pos[0]][azure_pos[1]] = 2


    return output_grid