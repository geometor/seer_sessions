```python
"""
1.  **Identify Pivots:** Locate all pixels with a value of '5' (gray) in the input grid. These pixels are "pivot pixels" and their values will remain unchanged in the output grid.

2.  **Left Transformation:** For any pixel *to the left* of a pivot pixel, apply the following transformation to its value:
    *   0 becomes 6 (white becomes magenta)
    *   1 becomes 6 (blue becomes magenta)
    *   2 becomes 7 (red becomes orange)
    *   3 becomes 8 (green becomes azure)
    *   4 becomes 9 (yellow becomes maroon)

3.  **Right Transformation:** For any pixel *to the right* of a pivot pixel, apply the following transformation to its value:
    *   0 becomes 6 (white becomes magenta)
    *   1 becomes 6 (blue becomes magenta)
    *   2 becomes 7 (red becomes orange)
    *   3 becomes 8 (green becomes azure)
    *   4 becomes 9 (yellow becomes maroon)

4. **Output Construction:** Create the output grid by applying the above transformations. Copy pivot pixels (value 5) directly to the output grid. Transform the non-pivot pixels according to the left or right transformation rules based on their position relative to the nearest pivot pixel on the same row. If a pixel is both to the left of *one* pivot pixel and to the right of *another*, the transformation is applied consistently based on the mapping. The presence of any 5 transforms all of the digits to its left to the 'left_mapping' and all digits to the right to the 'right_mapping'.
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
        pivot_indices = np.where(input_grid[r] == 5)[0]

        for c in range(cols):
            if input_grid[r, c] == 5:
                continue  # Pivot pixels remain unchanged

            if len(pivot_indices) > 0:
                if c < pivot_indices[0]:
                    # Apply left transformation
                    output_grid[r, c] = left_mapping.get(input_grid[r, c], input_grid[r, c])
                else:
                    #Apply right transformation
                    output_grid[r,c] = right_mapping.get(input_grid[r,c], input_grid[r,c])
            # else no transformation (no pivot on that row)

    return output_grid.tolist()
```