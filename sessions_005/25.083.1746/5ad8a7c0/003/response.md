```python
"""
The transformation rule identifies continuous, straight, un-branching lines of red pixels (value 2) within the input grid. These can be either horizontal or vertical. If such a line exists, *and it's the only such line*, it is expanded to fill the entire row (if horizontal) or the entire column (if vertical) it occupies. If there are isolated red pixels, or more than one line of red pixels, or any L shapes, no change occurs.
"""

import numpy as np

def get_red_lines(grid):
    """Finds all connected horizontal and vertical lines of red pixels."""
    red_lines = []
    rows, cols = grid.shape

    # Check for horizontal lines
    for r in range(rows):
        line = []
        for c in range(cols):
            if grid[r, c] == 2:
                line.append((r, c))
            else:
                if len(line) > 1:
                    red_lines.append(line)
                line = []
        if len(line) > 1:
            red_lines.append(line)

    # Check for vertical lines
    for c in range(cols):
        line = []
        for r in range(rows):
            if grid[r, c] == 2:
                line.append((r, c))
            else:
                if len(line) > 1:
                    red_lines.append(line)
                line = []
        if len(line) > 1:
            red_lines.append(line)
    return red_lines

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)
    red_lines = get_red_lines(grid)

    # If there's exactly one red line, expand it
    if len(red_lines) == 1:
        line = red_lines[0]
        rows = [r for r, _ in line]
        cols = [c for _, c in line]

        if len(set(rows)) == 1:  # Horizontal
            output_grid[rows[0], :] = 2
        elif len(set(cols)) == 1:  # Vertical
            output_grid[:, cols[0]] = 2

    return output_grid.tolist()
```
