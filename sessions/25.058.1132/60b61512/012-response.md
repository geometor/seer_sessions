# 60b61512 • 012 • refine_coder

---
```python
"""
1.  **Identify** all horizontal lines of yellow pixels.
2.  Determine, of the lines, which line(s) is the largest.
3.  Locate, in the input grid, the yellow pixel(s) at the right end of the largest horizontal line(s) of yellow.
4.  **Change** the color of *those* identified yellow pixels to orange (7).
5.  **Preserve** all other pixels as they are in the input.
"""

import numpy as np

def find_horizontal_lines(grid, color):
    """Finds all horizontal lines of a given color."""
    lines = []
    for row_idx, row in enumerate(grid):
        current_line = []
        for col_idx, pixel in enumerate(row):
            if pixel == color:
                current_line.append((row_idx, col_idx))
            else:
                if current_line:
                    lines.append(current_line)
                    current_line = []
        if current_line:  # Handle lines that extend to the end of the row
            lines.append(current_line)
    return lines

def find_largest_lines(lines):
    """Finds the largest line(s) from a list of lines."""
    if not lines:
        return []
    max_length = max(len(line) for line in lines)
    largest_lines = [line for line in lines if len(line) == max_length]
    return largest_lines

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all horizontal yellow lines
    yellow_lines = find_horizontal_lines(input_grid, 4)

    # Find the largest yellow lines
    largest_yellow_lines = find_largest_lines(yellow_lines)

    # Change the rightmost pixel of the largest lines to orange
    for line in largest_yellow_lines:
        rightmost_pixel = line[-1]
        output_grid[rightmost_pixel[0], rightmost_pixel[1]] = 7

    return output_grid
```
