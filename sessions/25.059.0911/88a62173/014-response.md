# 88a62173 • 014 • refine_coder

---
```python
"""
The input grid is divided into four quadrants. Each quadrant maps to a cell in the 2x2 output grid. The output cell's color is determined by the most frequent color in the corresponding input quadrant, excluding white (0). If multiple colors have the same highest frequency, or if the quadrant consists only of white, the behavior is deterministic but needs further clarification (likely defaults to a pre-defined color or the first non-white color encountered).
"""

import numpy as np

def get_quadrant(input_grid, row_start, row_end, col_start, col_end):
    """Extracts a quadrant from the input grid."""
    return input_grid[row_start:row_end, col_start:col_end]

def most_frequent_color(quadrant):
    """
    Determines the most frequent color in a quadrant, excluding white (0).
    Returns 0 if the quadrant contains only white.
    If there's a tie for most frequent, this currently returns one of the tied colors (not deterministic across runs - needs improvement!)
    """
    colors = list(quadrant.flatten())
    if not colors:
        return 0

    # Count occurrences of each color
    counts = {}
    for color in colors:
        if color != 0:  # Exclude white (0)
            counts[color] = counts.get(color, 0) + 1

    if not counts: # Only white present
        return 0
    
    # Find the maximum count
    max_count = 0
    for color in counts:
        if counts[color] > max_count:
            max_count = counts[color]
    
    # Get colors that have the maximum count
    most_frequent = []
    for color in counts:
      if counts[color] == max_count:
        most_frequent.append(color)

    # Return the lowest color if there is a tie (deterministic).
    if len(most_frequent) > 0:
      return min(most_frequent)
    else:
      return 0

def transform(input_grid):
    """Transforms the input grid to the output grid based on quadrant analysis."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Calculate midpoints for quadrant division
    row_mid = rows // 2
    col_mid = cols // 2

    # Initialize the output grid as 2x2 with all white pixels (0)
    output_grid = np.zeros((2, 2), dtype=int)

    # Define the four quadrants
    quadrants = [
        (0, row_mid + (rows%2), 0, col_mid + (cols%2)),  # Top-left
        (0, row_mid + (rows%2), col_mid, cols),         # Top-right
        (row_mid, rows, 0, col_mid + (cols%2)),         # Bottom-left
        (row_mid, rows, col_mid, cols)                # Bottom-right
    ]

    # Iterate through quadrants and determine output colors
    for i, (row_start, row_end, col_start, col_end) in enumerate(quadrants):
        quadrant = get_quadrant(input_grid, row_start, row_end, col_start, col_end)
        output_color = most_frequent_color(quadrant) # use most frequent logic
       
        output_row = i // 2
        output_col = i % 2
        output_grid[output_row, output_col] = output_color

    return output_grid.tolist()
```
