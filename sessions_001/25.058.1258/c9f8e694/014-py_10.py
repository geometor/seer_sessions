"""
1.  **Identify Gray Regions:** Locate all contiguous regions of gray (5) pixels in the input grid. Contiguous means horizontally or vertically adjacent, not diagonally.

2.  **Seed Check:** For each gray region, determine if it has a "seed" color. A seed color is a non-gray, non-white (not 0) color that is directly adjacent (horizontally or vertically) to any pixel within the gray region.

3.  **Conditional Replacement:**
    *   If a gray region *has* a seed color, replace all gray pixels in that region with the seed color.
    *   If a gray region *does not have* a seed color, leave the gray pixels unchanged (do not replace them).

4.  **Output:** The output grid is the result of these replacements (or lack thereof). Pixels that are not gray are unchanged.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Gets the valid neighbors of a cell (up, down, left, right)."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def flood_fill(grid, row, col, target_color, replacement_color):
    """Performs a flood fill operation."""
    if grid[row, col] != target_color:
        return
    grid[row, col] = replacement_color
    for r, c in get_neighbors(grid, row, col):
        flood_fill(grid, r, c, target_color, replacement_color)

def find_seed_color(grid, row, col, gray_color=5):
    """Finds the non-gray, non-white color adjacent to a gray region."""
    rows, cols = grid.shape

    #check up
    if row > 0 and grid[row-1, col] != gray_color and grid[row-1, col] != 0:
      return grid[row-1, col]
    #check down
    if row < rows -1 and grid[row+1, col] != gray_color and grid[row+1, col] != 0:
      return grid[row+1, col]
    #check left
    if col > 0 and grid[row, col-1] != gray_color and grid[row, col-1] != 0:
      return grid[row, col-1]
    #check right
    if col < cols - 1 and grid[row, col+1] != gray_color and grid[row, col+1] != 0:
        return grid[row, col+1]

    return None

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid to find gray regions
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 5:  # Found a gray pixel
                # Find the seeding color
                seed_color = find_seed_color(output_grid, row, col)
                if seed_color is not None:
                   # Apply flood fill to replace gray with the seed color
                   flood_fill(output_grid, row, col, 5, seed_color)

    return output_grid