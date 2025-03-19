# 54d9e175 • 014 • refine_coder

---
```python
"""
Transforms the input grid by replacing single, isolated pixels of dynamic colors (not 0 or 5) with new colors based on their order of appearance. Larger contiguous regions of dynamic colors remain unchanged. Colors 0 and 5 are always preserved.
"""

import numpy as np

def is_isolated(grid, i, j, color):
    """
    Checks if a pixel at (i, j) with the given color is isolated (no adjacent neighbors of the same color).
    """
    rows, cols = grid.shape
    for x in range(max(0, i - 1), min(rows, i + 2)):
        for y in range(max(0, j - 1), min(cols, j + 2)):
            if (x != i or y != j) and 0 <= x < rows and 0 <= y < cols and grid[x, y] == color:
                return False  # Found a neighbor with the same color
    return True

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

    # Iterate and perform replacements based on isolation
    for i in range(rows):
        for j in range(cols):
            value = input_grid[i, j]
            if value != 0 and value != 5:  # Dynamic value
                if is_isolated(input_grid, i, j, value):
                    output_grid[i, j] = dynamic_value_mapping[value]
                # else:  Non-isolated dynamic pixels are left unchanged
            # else: 0 and 5 values are automatically copied

    return output_grid
```
