"""
Copy non-zero pixels from input to output. Fill zero-valued pixels in the
output based on the values of their nearest non-zero neighbors in the four
cardinal directions (up, down, left, right). If at least two neighbors have the
same non-zero value, set the output pixel to that value; otherwise, leave it
unchanged (which should apply only if the input was zero).
"""

import numpy as np

def get_neighbors(grid, row, col):
    """
    Gets the non-zero neighbors of a cell in the grid.
    """
    rows, cols = grid.shape
    neighbors = []
    # Check up
    if row > 0 and grid[row - 1, col] != 0:
        neighbors.append(grid[row - 1, col])
    # Check down
    if row < rows - 1 and grid[row + 1, col] != 0:
        neighbors.append(grid[row + 1, col])
    # Check left
    if col > 0 and grid[row, col - 1] != 0:
        neighbors.append(grid[row, col - 1])
    # Check right
    if col < cols - 1 and grid[row, col + 1] != 0:
        neighbors.append(grid[row, col + 1])
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid
    for r in range(rows):
        for c in range(cols):
            # Process only zero-valued pixels in input
            if input_grid[r, c] == 0:
                neighbors = get_neighbors(input_grid, r, c)
                
                # Count the occurrences of each non-zero neighbor
                counts = {}
                for n in neighbors:
                    counts[n] = counts.get(n, 0) + 1

                # Find neighbors with count >= 2
                for val, count in counts.items():
                    if count >= 2:
                        output_grid[r, c] = val
                        break  # Found a match, move to next pixel

    return output_grid.tolist()