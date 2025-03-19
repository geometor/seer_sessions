# 67a423a3 • 002 • example_3 • investigate_coder

---
```python
"""
Transforms an input grid by identifying the longest straight line of a single
non-zero color, and then creating a "cross" pattern around it using a
replacement color. The replacement color is yellow (4).
"""

import numpy as np

def find_center_line(grid):
    """
    Finds the longest straight line of a single non-zero color in the grid.
    Returns a tuple: (color, orientation, start_row, start_col, length).
    Orientation is 'vertical' or 'horizontal'.  Returns None if no line is found.
    """
    rows, cols = grid.shape
    best_line = None

    # Check for horizontal lines
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                color = grid[r, c]
                length = 0
                for c2 in range(c, cols):
                    if grid[r, c2] == color:
                        length += 1
                    else:
                        break
                if best_line is None or length > best_line[4]:
                    best_line = (color, 'horizontal', r, c, length)

    # Check for vertical lines
    for c in range(cols):
        for r in range(rows):
            if grid[r, c] != 0:
                color = grid[r, c]
                length = 0
                for r2 in range(r, rows):
                    if grid[r2, c] == color:
                        length += 1
                    else:
                        break
                if best_line is None or length > best_line[4]:
                    best_line = (color, 'vertical', r, c, length)

    return best_line

def get_replacement_color(grid, center_line):
    """
    Determines the replacement color based on neighbors of the center line.
    Currently, this always returns 4 (yellow) based on the examples.
    """
    return 4

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = grid.shape
    output_grid = grid.copy()

    center_line = find_center_line(grid)

    if center_line:
        color, orientation, start_row, start_col, length = center_line
        replacement_color = get_replacement_color(grid, center_line)

        if orientation == 'horizontal':
            # find the midpoint on the horizontal line.
            mid_col = start_col + length // 2
            for r in range(rows):
              output_grid[r, mid_col] = replacement_color if grid[r, mid_col] == 0 else grid[r,mid_col]
            for c in range(start_col,start_col + length):
              output_grid[start_row, c] = color
              
        elif orientation == 'vertical':
             # find the midpoint on the vertical line
            mid_row = start_row + length // 2
            for c in range(cols):
                output_grid[mid_row, c] = replacement_color if grid[mid_row, c] == 0 else grid[mid_row,c]
            for r in range(start_row, start_row + length):
                output_grid[r,start_col] = color

    return output_grid.tolist()
```
