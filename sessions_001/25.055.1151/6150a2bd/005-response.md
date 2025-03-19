# 6150a2bd • 005 • refine_coder

---
```python
"""
Transpose the grid: Swap the rows and columns of the input grid.  The value at input[row][column] becomes the value at output[column][row].
Preserve pixel values: The transposition must maintain the values and their respective relative locations, just with transposed coordinates.
"""

def transform(input_grid):
    # Get dimensions of the input grid
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize the output grid with transposed dimensions
    output_grid = [[0] * rows for _ in range(cols)]

    # Transpose the grid: swap rows and columns
    for i in range(rows):
        for j in range(cols):
            output_grid[j][i] = input_grid[i][j]

    return output_grid
```
