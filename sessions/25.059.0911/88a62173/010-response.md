# 88a62173 • 010 • example_2 • investigate_coder

---
```python
"""
The input grid is reduced to a 2x2 output grid by summarizing the presence of blue pixels (value 1) within four quadrants of the input grid. If a quadrant in the input grid contains any blue pixels, the corresponding cell in the output grid is blue. Otherwise, it's white.
"""

import numpy as np

def get_quadrant(input_grid, row_start, row_end, col_start, col_end):
    """Extracts a quadrant from the input grid."""
    return input_grid[row_start:row_end, col_start:col_end]

def has_blue(quadrant):
    """Checks if a quadrant contains any blue pixels (value 1)."""
    return np.any(quadrant == 1)

def transform(input_grid):
    """Transforms the input grid to the output grid based on quadrant analysis."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Calculate midpoints for quadrant division (handle odd dimensions)
    row_mid = rows // 2
    col_mid = cols // 2

    # Initialize the output grid as 2x2 with all white pixels (0)
    output_grid = np.zeros((2, 2), dtype=int)

    # Define the four quadrants (handle edge cases for odd dimensions)
    quadrants = [
        (0, row_mid + (rows%2), 0, col_mid + (cols%2)),  # Top-left
        (0, row_mid + (rows%2), col_mid, cols),         # Top-right
        (row_mid, rows, 0, col_mid + (cols%2)),         # Bottom-left
        (row_mid, rows, col_mid, cols)                # Bottom-right
    ]

    # Iterate through quadrants and check for blue pixels
    for i, (row_start, row_end, col_start, col_end) in enumerate(quadrants):
        quadrant = get_quadrant(input_grid, row_start, row_end, col_start, col_end)
        if has_blue(quadrant):
            # Map quadrant index to output grid coordinates
            output_row = i // 2
            output_col = i % 2
            output_grid[output_row, output_col] = 1

    return output_grid.tolist()
```
