```python
"""
1.  **Identify Green Pixels:** Iterate through the grid, focusing on *green* pixels first.

2.  **Find Adjacent Reds:** For *each* green pixel, identify all adjacent red pixels (horizontally or vertically).

3.  **Transform Adjacent Reds (One-to-One):** For each red pixel found adjacent to the current green pixel, change the red pixel to azure. Mark the *green* pixel as "consumed" after processing all its adjacent red pixels so that this green pixel cannot be used to process any additional reds in the future.

4. **Iterate:** Continue this process for all remaining *green* pixels in the grid.

5.  **Unchanged Pixels:** Any pixel that is not transformed by the above rules remains unchanged.
"""

import numpy as np

def is_adjacent(coord1, coord2):
    """
    Checks if two coordinates are adjacent (horizontally or vertically).

    Args:
      coord1: Tuple (row1, col1)
      coord2: Tuple (row2, col2)

    Returns:
      True if adjacent, False otherwise.
    """
    row_diff = abs(coord1[0] - coord2[0])
    col_diff = abs(coord1[1] - coord2[1])
    return (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)

def get_neighbors(grid, row, col):
    """
    Returns a list of adjacent neighbors (horizontally or vertically).
    """
    rows, cols = grid.shape
    neighbors = []
    for i in range(max(0, row - 1), min(rows, row + 2)):
        for j in range(max(0, col - 1), min(cols, col + 2)):
            if (i != row or j != col) and is_adjacent((row, col), (i, j)):
                neighbors.append((i, j))
    return neighbors

def transform(input_grid):
    """
    Transforms the input grid according to the revised rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    consumed_green = set()

    # Iterate through each cell of the input grid, looking for green pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 3 and (i, j) not in consumed_green:  # Check for green and not consumed
                neighbors = get_neighbors(input_grid, i, j)
                red_neighbors = [(r, c) for r, c in neighbors if input_grid[r,c] == 2]

                # Transform all adjacent red pixels to azure
                for red_row, red_col in red_neighbors:
                    output_grid[red_row, red_col] = 8
                
                consumed_green.add((i,j)) #mark green as consumed

    return output_grid
```