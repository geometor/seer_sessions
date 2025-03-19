# 36fdfd69 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation rule is as follows:

1.  **Identify Target Pixels:** Locate all red (2) pixels within the input grid.
2.  **Check Adjacency:** For each identified red pixel, examine its immediate neighbors (up, down, left, and right - not diagonally).
3. **Conditional Modification (Specifically Replacing with Yellow):**
    *   If a red pixel is adjacent to a white (0) pixel, change the red pixel to yellow (4).
    *   If a red pixel is not adjacent to any white pixels, it remains red.
"""

import numpy as np

def get_adjacent_pixels(grid, row, col):
    """
    Gets the values of adjacent pixels (up, down, left, right) for a given cell.
    """
    rows, cols = grid.shape
    adjacent = []
    if row > 0:
        adjacent.append(grid[row-1, col])  # Up
    if row < rows - 1:
        adjacent.append(grid[row+1, col])  # Down
    if col > 0:
        adjacent.append(grid[row, col-1])  # Left
    if col < cols - 1:
        adjacent.append(grid[row, col+1])  # Right
    return adjacent


def transform(input_grid):
    """
    Transforms the input grid according to the specified rule:
    Red pixels adjacent to white pixels become yellow.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each pixel in the grid
    for row in range(rows):
        for col in range(cols):
            # Check if the current pixel is red
            if input_grid[row, col] == 2:
                # Get adjacent pixel values
                adjacent_values = get_adjacent_pixels(input_grid, row, col)
                # Check for adjacency to white (0)
                if 0 in adjacent_values:
                    output_grid[row, col] = 4  # Change to yellow

    return output_grid
```
