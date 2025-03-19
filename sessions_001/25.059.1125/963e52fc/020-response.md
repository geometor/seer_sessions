# 963e52fc • 020 • refine_coder

---
```python
"""
1.  **Identify Pattern Rows:** Examine each row of the input grid. A "pattern row" is defined as a row containing an alternating sequence of blue (1) and red (2) pixels.

2.  **Double Pattern Rows:** For each identified pattern row, duplicate the entire row content and append it to itself, effectively doubling the pattern horizontally.

3. **Expand other rows.** For rows that are *not* pattern rows, simply duplicate it to double it's length.

4.  **Double Grid Width:** The output grid's width is always double the input grid's width. The height remains the same.
"""

import numpy as np

def is_pattern_row(row):
    """Checks if a row is a pattern row (alternating blue and red)."""
    if len(row) < 2:
        return False  # Need at least two elements to alternate
    if not set(row).issubset({1, 2}):
        return False # contains colors besides blue and red
    for i in range(len(row) - 1):
        if row[i] == row[i+1]:
            return False  # Check for alternation
    return True

def transform(input_grid):
    # Initialize output_grid with doubled width, same height.
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1] * 2), dtype=int)

    # Iterate through each row of the input grid.
    for i in range(input_grid.shape[0]):
        if is_pattern_row(input_grid[i]):
            # Double the pattern horizontally.
            output_grid[i] = np.concatenate((input_grid[i], input_grid[i]))
        else:
            # Expand other rows by duplicating
            output_grid[i] = np.concatenate((input_grid[i],input_grid[i]))

    return output_grid
```
