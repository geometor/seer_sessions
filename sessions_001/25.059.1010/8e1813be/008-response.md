# 8e1813be • 008 • refine_coder

---
```python
"""
1.  **Identify:** Find all horizontal lines (rows) in the input grid that consist of a single, uniform, non-zero color. These are the "solid color lines".
2.  **Construct:** Create the output grid by taking all of the solid color lines.
3. **Dimensions:** Output width matches input width. Output height equals the number of identified solid color lines.
"""

import numpy as np

def is_solid_color_line(line):
    """Checks if a line (list) contains only one unique non-zero value."""
    unique_values = np.unique(line)
    return len(unique_values) == 1 and unique_values[0] != 0

def transform(input_grid):
    """Transforms the input grid by extracting and stacking solid color lines, preserving original width."""
    
    # Initialize an empty list to hold the selected lines.
    selected_lines = []

    # Iterate through each row of the input grid, collecting solid color lines (excluding 0).
    for row in input_grid:
        if is_solid_color_line(row):
            selected_lines.append(row)

    # Construct the output grid by vertically stacking the selected lines.
    if not selected_lines:
        return np.array([])  # Return an empty array if no solid color lines are found.
    output_grid = np.array(selected_lines)

    return output_grid
```
