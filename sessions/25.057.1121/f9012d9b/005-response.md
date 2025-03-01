# f9012d9b • 005 • refine_coder

---
```python
"""
The transformation identifies a horizontal line of azure (8) pixels within the input grid.
This line is then shifted down by one row in the output grid. If the horizontal line is
composed by more than one row, the transformation shifts down one row, and removes the rest of
the rows that are part of the line.
"""

import numpy as np

def find_horizontal_line(grid, color=8):
    """Finds the rows containing a horizontal line of the specified color."""
    rows_with_line = []
    for i, row in enumerate(grid):
        if np.all(np.isin(color, row)):
            if len(set(row)) == 2 and 0 in set(row):
                rows_with_line.append(i)
            elif len(set(row)) == 1:
                rows_with_line.append(i)

    return rows_with_line

def transform(input_grid):
    """Transforms the input grid by shifting a horizontal azure line down by one row."""
    input_np = np.array(input_grid)
    output_np = np.zeros_like(input_np)  # Initialize with background color (0)

    # Find the horizontal line of azure (8) pixels
    rows_with_line = find_horizontal_line(input_np)

    # Apply the shift based on row
    if rows_with_line:

        line_row_index = rows_with_line[0]

        new_row_index = line_row_index + 2
        if new_row_index < output_np.shape[0] and len(rows_with_line) < 3:
            if len(rows_with_line) > 1:
                new_row_index = rows_with_line[0] + 1

            row = input_np[line_row_index,:]
            first = -1
            last = -1
            for i in range(len(row)):
                pix = row[i]
                if pix == 8 and first == -1:
                    first = i
                if pix == 8:
                    last = i

            output_np[new_row_index, first:last+1] = 8

    return output_np.tolist()
```
