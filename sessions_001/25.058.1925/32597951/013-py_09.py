"""
1. **Identify the Azure Region:** Find the smallest rectangular region within the grid that contains all azure (8) pixels. If no azure pixels exist, the output is identical to the input.

2. **Iterate through Azure Pixels:** For each azure pixel within the identified azure region:

    a. **Temporarily Remove:** Temporarily remove the azure pixel (conceptually, set its value to 0, or any color other than azure).

    b. **Check for Disconnection:** After removing the pixel, check if the remaining azure pixels are still a *single connected component*. Use 8-connectivity (including diagonals) for determining connectedness. A good way to do this to perform a flood fill (or Depth First Search) starting from any remaining azure pixel. If the flood fill can reach all other originally azure pixels (excluding the one temporarily removed) then no disconnection happened.

    c. **Conditional Change:** If, and *only if*, removing the pixel causes the remaining azure pixels to become disconnected (i.e., form two or more separate azure regions), change the original azure pixel's color to green (3) in the output grid. Otherwise, keep the pixel's original azure color.

3. **Output:** The final output grid is the result of these modifications.
"""

import numpy as np

def find_azure_region(grid):
    azure_coords = np.argwhere(grid == 8)
    if azure_coords.size == 0:
        return None, None, None, None
    min_row = np.min(azure_coords[:, 0])
    max_row = np.max(azure_coords[:, 0])
    min_col = np.min(azure_coords[:, 1])
    max_col = np.max(azure_coords[:, 1])
    return min_row, max_row, min_col, max_col

def flood_fill(grid, row, col, original_color, visited):
    rows, cols = grid.shape
    if (row < 0 or row >= rows or col < 0 or col >= cols or
        grid[row, col] != original_color or (row, col) in visited):
        return
    visited.add((row, col))
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            flood_fill(grid, row + dr, col + dc, original_color, visited)

def is_connected(grid, removed_row, removed_col):
    rows, cols = grid.shape
    azure_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 8 and (r != removed_row or c != removed_col):
                azure_pixels.append((r,c))
    
    if not azure_pixels:
      return True

    visited = set()
    flood_fill(grid, azure_pixels[0][0], azure_pixels[0][1], 8, visited)
    
    return len(visited) == len(azure_pixels)


def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Find the region of interest (where azure pixels are)
    min_row, max_row, min_col, max_col = find_azure_region(input_grid)
    
    if min_row is None:  # No azure pixels found, return the original grid
        return output_grid

    # Iterate through the region of interest
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            # Check if the current pixel is azure
            if output_grid[row, col] == 8:
                # Temporarily remove the pixel
                original_color = output_grid[row, col]
                output_grid[row, col] = 0  

                # Check if removing this pixel disconnects the region
                if not is_connected(output_grid, row, col):
                    output_grid[row, col] = 3  # Change to green
                else:
                    output_grid[row, col] = original_color  # Restore original color

    return output_grid