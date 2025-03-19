# 272f95fa • 008 • example_1 • investigate_coder

---
```python
"""
This program transforms an input grid by identifying azure lines and filling the spaces between them with specific colors.
The azure lines are preserved, and the spaces are filled with red, magenta, blue, green and yellow in a specific order.
"""

import numpy as np

def find_azure_lines(grid):
    # Find the vertical and horizontal azure lines.
    azure_indices = np.where(grid == 8)
    rows = np.unique(azure_indices[0])
    cols = np.unique(azure_indices[1])
    
    vertical_line_col = None
    horizontal_lines_row = []

    for col in cols:
        if np.sum(grid[:, col] == 8) > 2:  # Assuming a vertical line has more than two azure pixels
            vertical_line_col = col
            break

    for row in rows:
        if np.sum(grid[row, :] == 8) > 2 :
            horizontal_lines_row.append(row)
    
    return vertical_line_col, horizontal_lines_row

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    # Find the azure lines
    vertical_line_col, horizontal_lines_row = find_azure_lines(input_grid)
    horizontal_line_row = horizontal_lines_row[0]
    horizontal_line_row2 = horizontal_lines_row[1]

    # Fill the spaces between the lines
    for r in range(rows):
        for c in range(cols):
            # Preserve azure pixels
            if input_grid[r, c] == 8:
                continue
            
            if horizontal_line_row < r < horizontal_line_row2 :
                # Check for the area to the left of the vertical line
                if c < vertical_line_col:

                    output_grid[r,c] = 1 #blue
                # Check for the area to the right of the vertical line
                elif c > vertical_line_col:

                    output_grid[r,c] = 3 #green

            elif r < horizontal_line_row:
                if c< vertical_line_col:
                    output_grid[r,c] = 2 if c > vertical_line_col -3 else output_grid[r,c]
                elif c > vertical_line_col:
                    output_grid[r,c] = 6 if c < vertical_line_col + 3  else output_grid[r,c]
            elif  r > horizontal_line_row2:
                if c< vertical_line_col:
                     output_grid[r,c] = 1 if c > vertical_line_col -3 else output_grid[r,c]
                elif c > vertical_line_col:
                     output_grid[r,c] = 1 if c < vertical_line_col + 3  else output_grid[r,c]
            if horizontal_line_row2 > r > horizontal_line_row :
                if c< vertical_line_col-2:

                    output_grid[r,c] = 4 #blue
                # Check for the area to the right of the vertical line
                elif c > vertical_line_col +2:

                    output_grid[r,c] = 3 #green

    return output_grid
```
