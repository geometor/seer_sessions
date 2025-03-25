```python
"""
Transforms an input grid by replacing certain azure (8) pixels with red (2) pixels.
The replacement strategy focuses on azure pixels that have at least one orthogonally adjacent white (0) pixel.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Returns the orthogonally adjacent neighbors of a pixel."""
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

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    input_grid = np.array(input_grid)  # Ensure numpy array for easier manipulation
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is azure (8)
            if input_grid[row, col] == 8:
                # Get the orthogonally adjacent neighbors
                neighbors = get_neighbors(input_grid, row, col)
                # Check if any neighbor is white (0)
                for neighbor_row, neighbor_col in neighbors:
                    if input_grid[neighbor_row, neighbor_col] == 0:
                        # If a white neighbor is found, replace the current azure pixel with red (2)
                        output_grid[row, col] = 2
                        break  # Move to the next pixel after replacement

    return output_grid.tolist()
```
