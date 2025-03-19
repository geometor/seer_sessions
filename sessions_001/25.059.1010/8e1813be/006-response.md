# 8e1813be • 006 • refine_coder

---
```python
"""
1.  **Identify:** Find all horizontal lines (rows) in the input grid that consist of a single, uniform color. These are the "solid color lines".
2.  **Exclude:** Ignore any solid color lines where the color is 0 (white/background).
3.  **Select:** From the solid colored lines, select those that match the row indices of solid colored lines in the output.
4.  **Determine Output Length:** Observe the length of the lines in the output grid. This length is consistent for all lines within a single example.
5.  **Construct:** Create the output grid by taking the selected solid color lines from the input grid. Truncate or pad (with what?) each line to match the determined output length. In the examples, the lines are simply truncated.
"""

import numpy as np

def is_solid_color_line(line):
    """Checks if a line (list) contains only one unique non-zero value."""
    unique_values = np.unique(line)
    return len(unique_values) == 1 and unique_values[0] != 0

def transform(input_grid):
    """Transforms the input grid by extracting and stacking solid color lines, truncating to output width."""
    
    # Initialize an empty list to hold the selected lines.
    selected_lines = []

    # Iterate through each row of the input grid, collecting solid color lines (excluding 0).
    solid_color_lines_indices = []
    for i, row in enumerate(input_grid):
      if is_solid_color_line(row):
        solid_color_lines_indices.append(i)

    # Determine the output width. We'll assume the training examples reliably tell us this.
    # In a more robust system, we'd need a strategy to determine this from the test input if needed.
    # The width is determined during the 'dream' phase and is fixed.
    
    # get output width from first example - assume it's consistent
    output_width = 0    
    
    # Construct the output grid by vertically stacking the selected lines.
    for row_index in solid_color_lines_indices:
      selected_lines.append(input_grid[row_index])

    if not selected_lines:
        return np.array([])

    output_grid = np.array(selected_lines)

    # Truncate each line to the output width.
    if output_grid.size > 0:
      output_grid = output_grid[:, :output_width]

    return output_grid
```
