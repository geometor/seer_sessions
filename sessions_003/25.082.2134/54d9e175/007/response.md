```python
"""
1.  **Identify Pivot Pixels:** In each row of the input grid, find all pixels with a value of '5' (gray). These are the "pivot pixels."

2.  **Nearest Pivot:** For every non-pivot pixel in a row, determine the *nearest* pivot pixel within that same row. Distance is measured by the difference in column indices.

3.  **Left Transformation:** For each non-pivot pixel *to the left* of its nearest pivot pixel, apply the `left_mapping` to transform its value:
    *   0 becomes 6 (white becomes magenta)
    *   1 becomes 6 (blue becomes magenta)
    *   2 becomes 7 (red becomes orange)
    *   3 becomes 8 (green becomes azure)
    *   4 becomes 9 (yellow becomes maroon)

4.  **Right Transformation:** For each non-pivot pixel *to the right* of its nearest pivot pixel, apply the `right_mapping` to transform its value:
    *   0 becomes 6 (white becomes magenta)
    *   1 becomes 6 (blue becomes magenta)
    *   2 becomes 7 (red becomes orange)
    *   3 becomes 8 (green becomes azure)
    *   4 becomes 9 (yellow becomes maroon)

5.  **Pivot Pixel Preservation:** Pivot pixels (value 5) remain unchanged in the output grid. Copy their values directly.

6.  **No Pivot Row:** If a row has no pivot pixels leave it unchanged

7.  **Output:** Construct the output grid by combining the transformed non-pivot pixels and the unchanged pivot pixels.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    input_grid = np.array(input_grid)  # Ensure numpy array
    output_grid = np.copy(input_grid)   # Initialize output_grid
    rows, cols = input_grid.shape

    left_mapping = {0: 6, 1: 6, 2: 7, 3: 8, 4: 9}
    right_mapping = {0: 6, 1: 6, 2: 7, 3: 8, 4: 9}

    for r in range(rows):
        # Find pivot indices in the current row
        pivot_indices = np.where(input_grid[r] == 5)[0]

        # If no pivots in this row, skip to the next row
        if len(pivot_indices) == 0:
            continue

        for c in range(cols):
            # Skip pivot pixels themselves
            if input_grid[r, c] == 5:
                continue

            # Find the nearest pivot
            nearest_pivot_index = min(pivot_indices, key=lambda x: abs(x - c))

            # Apply transformation based on position relative to nearest pivot
            if c < nearest_pivot_index:
                output_grid[r, c] = left_mapping.get(input_grid[r, c], input_grid[r, c])
            else:
                output_grid[r, c] = right_mapping.get(input_grid[r, c], input_grid[r, c])

    return output_grid.tolist()
```