"""
1.  **Identify Center Pixels:** Find all pixels in the input grid that have a value of '2' (red) or '1' (blue). These are the "center pixels."

2.  **Conditional Red Expansion:** For each red (2) center pixel, examine its immediate neighbors (above, below, left, and right). If a neighboring cell has a value of '0' (white), change that cell's value to '4' (yellow) in the output grid. Do *not* change the value of the center pixel or any non-white neighboring cell.

3.  **Conditional Blue Expansion:** For each blue (1) center pixel, examine its immediate neighbors (above, below, left, and right). If a neighboring cell has a value of '0' (white), change that cell's value to '7' (orange) in the output grid. Do *not* change the value of the center pixel or any non-white neighboring cell.

4. **Preserve:** Any input pixels that are not center pixels or changed during expansion, should keep the same value.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    get the neighbor coordinates of the current cell
    """
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Above
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Below
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid
    rows, cols = input_grid.shape
    for row in range(rows):
        for col in range(cols):
            # Find center pixels (red or blue)
            if input_grid[row, col] == 2:
                # Conditional Red Expansion
                for r, c in get_neighbors(input_grid, row, col):
                    if output_grid[r, c] == 0:  # Check if the neighbor is white
                        output_grid[r, c] = 4  # Change to yellow

            elif input_grid[row, col] == 1:
                # Conditional Blue Expansion
                for r, c in get_neighbors(input_grid, row, col):
                    if output_grid[r, c] == 0:  # Check if the neighbor is white
                        output_grid[r, c] = 7  # Change to orange

    return output_grid