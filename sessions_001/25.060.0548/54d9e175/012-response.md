# 54d9e175 • 012 • refine_coder

---
```python
"""
Transforms the input grid by replacing non-zero and non-five values with specific colors in 3x3 blocks, centered on the original pixel's location, while keeping the values 0 and 5 unchanged. The replacement colors are assigned based on the order in which the unique non-zero, non-five values appear in the input grid.
"""

import numpy as np

def get_replacement_color(order):
    """
    Returns the replacement color based on the order of appearance.
    """
    if order == 1:
        return 7  # Orange
    elif order == 2:
        return 8  # Azure
    elif order == 3:
        return 6  # Magenta
    else:
        # Handle cases beyond the provided examples (extrapolate)
        return (order % 10)  # Cycle through colors 0-9

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Create a list to track the dynamic values found and their order
    dynamic_values_found = []
    dynamic_value_mapping = {} # value: replacement_color

    # Iterate through the input grid to find and map dynamic values
    for i in range(rows):
        for j in range(cols):
            value = input_grid[i, j]
            if value != 0 and value != 5:
                if value not in dynamic_values_found:
                    dynamic_values_found.append(value)
                    replacement_color = get_replacement_color(len(dynamic_values_found))
                    dynamic_value_mapping[value] = replacement_color

    # Iterate through the input grid and perform replacements
    for i in range(rows):
        for j in range(cols):
            value = input_grid[i,j]
            if value != 0 and value != 5:
              replacement_color = dynamic_value_mapping[value]
              # Apply 3x3 replacement, centered at (i, j)
              for x in range(max(0, i - 1), min(rows, i + 2)):
                  for y in range(max(0, j - 1), min(cols, j + 2)):
                      output_grid[x, y] = replacement_color
            # else the 0 and 5 values are automatically copied during init

    return output_grid
```
