# 1f876c06 • 020 • refine_coder

---
```python
"""
The transformation rule involves identifying a vertical or horizontal line of uniform, non-zero colored pixels in the input grid. This line is then treated as an object and moved to the top-left of the output grid, maintaining its orientation. The output grid's dimensions are determined by the length of the line and the dimensions of the input grid, with empty cells filled with zeros.
"""

import numpy as np

def find_line(grid):
    """
    Finds a vertical or horizontal line of uniform, non-zero colored pixels.
    Returns the line as a list of (color, (row, col)) tuples, and its orientation ('v' or 'h').
    """
    rows, cols = len(grid), len(grid[0])

    # Check for horizontal lines
    for r in range(rows):
        first_color = grid[r][0]
        if first_color == 0:
            continue
        is_line = True
        line = []
        for c in range(cols):
            if grid[r][c] != first_color:
                is_line = False
                break
            line.append((first_color, (r, c)))
        if is_line:
            return line, 'h'

    # Check for vertical lines
    for c in range(cols):
        first_color = grid[0][c]
        if first_color == 0:
            continue
        is_line = True
        line = []
        for r in range(rows):
            if grid[r][c] != first_color:
                is_line = False
                break
            line.append((first_color, (r, c)))
        if is_line:
            return line, 'v'

    return None, None

def transform(input_grid):
    # Convert to numpy array
    input_grid = np.array(input_grid)
    
    # Find object
    line, orientation = find_line(input_grid)

    # If no line return blank grid
    if line is None:
        return np.zeros_like(input_grid)

    # Determine output dimensions.
    line_length = len(line)
    if orientation == 'h':
        output_grid = np.zeros((input_grid.shape[1],input_grid.shape[0]), dtype=int)
        output_height = 1
        output_width = line_length
          # Place the line in the output grid.
        for i, (color, _) in enumerate(line):
            output_grid[0,i] = color
    else:  # orientation == 'v'
        output_grid = np.zeros((input_grid.shape[1],input_grid.shape[0]), dtype=int)

        output_height = line_length
        output_width = 1

        # Place the line in the output grid.
        for i, (color, _) in enumerate(line):
            output_grid[i, 0] = color

    output_grid = output_grid[:max(output_height, input_grid.shape[1]), :max(output_width, input_grid.shape[0])]


    return output_grid[:input_grid.shape[1], :input_grid.shape[0]]
```
