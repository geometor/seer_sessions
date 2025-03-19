"""
1.  **Identify Gray Regions:** Locate all contiguous regions of gray (value 5) pixels within the input grid.
2.  **Find Seed Color:** For each gray region, examine its neighboring pixels (up, down, left, right). Identify a "seed" pixel, which is a neighbor that is neither gray (5) nor white (0).
3.  **Flood Fill:** If a valid seed pixel is found, replace the entire gray region with the color of the seed pixel using a flood-fill algorithm. If multiple different valid seed pixels are adjacent to the same gray object, maintain the original grey color.
4. **Output:** if a gray object does not have a seed pixel neighbor, do not perform the flood fill.
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
    """Finds the non-gray, non-white color adjacent to a gray region, handling multiple seeds."""
    rows, cols = grid.shape
    seed_colors = set()

    # Check neighbors
    if row > 0 and grid[row - 1, col] != gray_color and grid[row - 1, col] != 0:
        seed_colors.add(grid[row - 1, col])
    if row < rows - 1 and grid[row + 1, col] != gray_color and grid[row + 1, col] != 0:
        seed_colors.add(grid[row + 1, col])
    if col > 0 and grid[row, col - 1] != gray_color and grid[row, col - 1] != 0:
        seed_colors.add(grid[row, col - 1])
    if col < cols - 1 and grid[row, col + 1] != gray_color and grid[row, col + 1] != 0:
        seed_colors.add(grid[row, col + 1])

    if len(seed_colors) == 1:
        return seed_colors.pop()  # Return the single seed color
    else:
        return None  # No seed or multiple different seeds

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid to find gray regions
    for row in range(rows):
        for col in range(cols):
            if output_grid[row, col] == 5:  # Found a gray pixel
                # Find the seeding color, now handling multiple seeds.
                seed_color = find_seed_color(output_grid, row, col)
                if seed_color is not None:
                    # Apply flood fill to replace gray with the seed color
                    flood_fill(output_grid, row, col, 5, seed_color)

    return output_grid