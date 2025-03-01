# 3631a71a • 006 • refine_coder

---
```python
"""
1.  **Identify and Remove:** Locate the contiguous block of maroon (9) colored pixels in the input grid. Remove all pixels within this block, effectively changing their color to the background color (0).
2.  **Column-wise Shift:** For each column in the grid, independently shift downwards any non-background colored pixels above the now-empty spaces. Pixels should only shift down within their own column. Pixels maintain their relative positions within their columns.
"""

import numpy as np

def find_maroon_block(grid):
    """
    Finds the contiguous block of maroon pixels using a breadth-first search.
    """
    maroon_pixels = np.argwhere(grid == 9)
    if maroon_pixels.size == 0:
        return []

    start_pixel = tuple(maroon_pixels[0])
    block = set()
    queue = [start_pixel]

    while queue:
        current_pixel = queue.pop(0)
        if current_pixel in block:
            continue
        block.add(current_pixel)
        row, col = current_pixel

        # Check adjacent pixels (up, down, left, right)
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for r, c in neighbors:
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == 9 and (r, c) not in block:
                queue.append((r, c))

    return list(block)

def transform(input_grid):
    """
    Transforms the input grid by removing the maroon block and shifting down other pixels column-wise.
    """
    # initialize output_grid
    output_grid = input_grid.copy()

    # Find and remove the maroon block
    maroon_block = find_maroon_block(output_grid)
    for row, col in maroon_block:
        output_grid[row, col] = 0  # Set to background color

    # Column-wise shift
    for col in range(output_grid.shape[1]):
        # Extract the column
        column = output_grid[:, col]

        # Find non-zero (non-background) pixels
        non_zero_indices = np.nonzero(column)[0]
        non_zero_values = column[non_zero_indices]


        # Create a new column with non-zero values shifted down
        new_column = np.zeros_like(column)
        new_column[len(new_column) - len(non_zero_values):] = non_zero_values

        # Update the column in the output grid
        output_grid[:, col] = new_column

    return output_grid
```
