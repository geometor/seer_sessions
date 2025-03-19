# b0c4d837 • 012 • refine_coder

---
```python
"""
1.  **Locate Azure Rectangle:** Find the smallest rectangle containing all azure (8) pixels in the input grid.
2.  **Extract Top Row:** Take the top row of the azure rectangle.
3. **Take first 3:** take the first three values from this row.
4.  **Create Output:** Create a 3x3 output grid.
5.  **Populate Top Row:** Place the extracted values from step 3, into the top row of the output grid.
6.  **Fill Remaining Rows:** Fill the remaining rows (rows 1 and 2) of the output grid with black (0) pixels.
"""

import numpy as np

def find_rectangle_by_color(grid, color):
    """Finds the top-left and bottom-right coordinates of a rectangle of a specific color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None  # No rectangle found
    top_left = (min(rows), min(cols))
    bottom_right = (max(rows), max(cols))
    return top_left, bottom_right

def transform(input_grid):
    # Create output grid (3x3, filled with 0s)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find azure rectangle
    azure_rectangle = find_rectangle_by_color(input_grid, 8)

    if azure_rectangle:
        # Extract top row of the azure rectangle
        top_left, _ = azure_rectangle
        top_row = input_grid[top_left[0], :]

        # Extract the relevant part of the top row (first three elements within the rectangle)
        start_col = top_left[1]
        extracted_row = top_row[start_col : start_col + 3]

        # Populate the top row of the output grid
        output_grid[0, :len(extracted_row)] = extracted_row

    return output_grid
```
