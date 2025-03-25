"""
1.  **Identify Azure Regions:** Find all contiguous regions of azure (8) pixels in the input grid. Consider pixels to be part of the same region if they are directly adjacent horizontally or vertically (not diagonally). Also identify isolated azure pixels.

2.  **Classify Azure Pixels:** Within each azure region, classify each azure pixel as either:
    *   **Border:** An azure pixel is a border pixel if at least one of its directly adjacent neighbors (up, down, left, or right) is *not* an azure pixel.
    *   **Interior:** An azure pixel is an interior pixel if all of its directly adjacent neighbors (up, down, left, and right) are also azure pixels.
    *   **Isolated:** An azure pixel which has no azure neighbors.

3.  **Transform:**
    *   Change the color of all border azure pixels to red (2).
    *   Change the color of all interior azure pixels to blue (1).
    *   Change the color of all isolated azure pixels to red (2).
    *   Leave all other pixels (non-azure) unchanged.
"""

import numpy as np

def get_cardinal_neighbors(grid, row, col):
    """Gets the 4 directly adjacent neighbors (up, down, left, right) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Cardinal directions
        nr, nc = row + dr, col + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def is_border_or_isolated(grid, row, col, color):
    """Checks if a cell of the specified color is a border cell or isolated, using cardinal neighbors."""
    if grid[row, col] != color:
        return False

    neighbors = get_cardinal_neighbors(grid, row, col)
    if not neighbors: # added to take care of edge cases
        return True
    
    all_same_color = all(grid[r, c] == color for r, c in neighbors)
    return not all_same_color


def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the grid to find azure regions and apply replacements
    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 8:  # Found an azure pixel
                if is_border_or_isolated(input_grid, row, col, 8):
                    output_grid[row, col] = 2  # Replace border/isolated azure with red
                else:
                    output_grid[row, col] = 1  # Replace interior azure with blue

    return output_grid