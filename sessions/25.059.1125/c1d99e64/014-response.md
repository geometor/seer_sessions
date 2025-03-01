# c1d99e64 • 014 • refine_coder

---
```python
"""
1.  Identify All Vertical White Lines: Find all contiguous vertical lines of white (0) pixels within the input grid.
2.  Find Longest Lines: Determine the maximum length among all identified vertical white lines.
3.  Select Longest Lines: Select all vertical white lines that have the maximum length.
4.  Determine Replacement Color: Identify a color from the set [1, 2, 3, 4] that is *not* present in the input grid.
5.  Replace Pixels: Replace all pixels in the selected longest vertical white lines with the determined replacement color.
"""

import numpy as np

def find_all_white_lines(grid):
    """Finds all contiguous vertical lines of white pixels in the grid."""
    rows, cols = grid.shape
    white_lines = []
    for col in range(cols):
        in_segment = False
        start_row = -1
        for row in range(rows):
            if grid[row, col] == 0:
                if not in_segment:
                    in_segment = True
                    start_row = row
            elif in_segment:
                in_segment = False
                white_lines.append((start_row, row - 1, col))
                start_row = -1
        if in_segment:
            white_lines.append((start_row, rows - 1, col))
    return white_lines

def determine_replacement_color(grid):
    """Finds a color from [1, 2, 3, 4] not present in the input grid."""
    unique_colors = np.unique(grid)
    for color in [1, 2, 3, 4]:
        if color not in unique_colors:
            return color
    return None  # Should not happen in valid cases

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify All Vertical White Lines
    white_lines = find_all_white_lines(output_grid)

    # Find Longest Lines and Select them
    if not white_lines:
        return output_grid

    max_length = max(end - start + 1 for start, end, _ in white_lines)
    longest_lines = [(start, end, col) for start, end, col in white_lines if end - start + 1 == max_length]

    # Determine Replacement Color
    replacement_color = determine_replacement_color(output_grid)

    # Replace Pixels
    for start_row, end_row, col in longest_lines:
        for row in range(start_row, end_row + 1):
            output_grid[row, col] = replacement_color

    return output_grid
```
