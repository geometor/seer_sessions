# ea32f347 • 004 • example_1 • investigate_coder

---
```python
"""
Identify vertical lines of grey (5) pixels in the input grid. Replace these
grey lines with different colors based on their adjacency to other grey lines:
- Isolated lines become blue (1).
- If a line has adjacent line, use yellow(4), for the first and red(2) for
  second of pair.
Leave other pixels (0) unchanged.
"""

import numpy as np

def find_vertical_lines(grid, color=5):
    """Finds vertical lines of a specified color in the grid."""
    lines = []
    rows, cols = grid.shape
    for c in range(cols):
        start = -1
        for r in range(rows):
            if grid[r, c] == color:
                if start == -1:
                    start = r
            elif start != -1:
                lines.append((start, r - 1, c))
                start = -1
        if start != -1:
            lines.append((start, rows - 1, c))
    return lines

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    output_grid = np.copy(input_grid)
    lines = find_vertical_lines(input_grid)
    
    # Create a dictionary to track line columns
    line_cols = {}
    for start_row, end_row, col in lines:
        line_cols.setdefault(col, []).append((start_row, end_row))

    # Determine the output color for each line based on adjacency
    for col in sorted(line_cols.keys()):
        lines_in_col = line_cols[col]
        
        is_first = (col == sorted(line_cols.keys())[0])
        has_right_neighbor = (col + 1) in line_cols
        
        
        if not has_right_neighbor :
              output_color = 1 #blue
        elif is_first:
              output_color = 4  # yellow

        else:
              output_color = 2 #red


        for start_row, end_row in lines_in_col:
            for r in range(start_row, end_row + 1):
                output_grid[r, col] = output_color

    return output_grid
```
