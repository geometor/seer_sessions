# 8e1813be • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify** all horizontal lines (rows) in the input grid that consist of a single, uniform color. We can refer to these as "solid color lines".
2.  **Exclude** any solid color lines where the color is 0 (white/background).
3. **Select:** select the solid colored lines.
4.  **Construct** the output grid by vertically stacking the selected solid color lines, in the order that they appeared in the input grid.
"""

import numpy as np

def is_solid_color_line(line):
    """Checks if a line (list) contains only one unique non-zero value."""
    unique_values = np.unique(line)
    return len(unique_values) == 1 and unique_values[0] != 0

def transform(input_grid):
    """Transforms the input grid by extracting and stacking solid color lines."""
    
    # Initialize an empty list to hold the selected lines.
    selected_lines = []

    # Iterate through each row of the input grid.
    for row in input_grid:
        # Check if the current row is a solid color line (excluding 0).
        if is_solid_color_line(row):
            selected_lines.append(row)

    # Construct the output grid by vertically stacking the selected lines.
    # If no lines were selected, return an empty grid (or handle as appropriate).
    if not selected_lines:
      return np.array([])
    
    output_grid = np.array(selected_lines)
    # get the first six lines
    output_grid = output_grid[:,:6]
    
    return output_grid
```
