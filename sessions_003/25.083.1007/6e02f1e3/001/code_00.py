"""
Transforms a 3x3 input grid into a 3x3 output grid based on the following rules:

1.  **Check Input Values:** Examine the unique values present in the input grid.

2.  **Single Value Rule:**
    *   If the input grid contains *only* the value 3, or *only* the value 4, fill the output grid entirely with 5s.

3.  **Mixed Values Rule:**
    *    If input grid has only values of 3 and 4, the output grid will have a diagonal of 5 from top-left to bottom-right, 0 otherwise.
    *   If the input grid contains 2 and 3: Create an output grid where the *anti-diagonal* (top-right to bottom-left) is filled with 5s, and all other cells are 0.
    *   If the input grid contains 2 and 4: Create an output grid where the *diagonal* (top-left to bottom-right) is filled with 5s, and all other cells are 0.

4.  **Overwrite rule:**
    *   If the single color rule is met, and the color is not 3 or 4, apply mixed value rule.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as all zeros
    output_grid = np.zeros((3, 3), dtype=int)
    unique_values = np.unique(input_grid)

    # Single Value Rule
    if len(unique_values) == 1:
        if unique_values[0] == 3 or unique_values[0] == 4:
            output_grid[:] = 5
        
    # Mixed Values Rule
    elif set(unique_values) == {2, 3}:
        for i in range(3):
            output_grid[i, 2 - i] = 5  # Anti-diagonal
    elif set(unique_values) == {2, 4}:
        for i in range(3):
            output_grid[i, i] = 5  # Diagonal
    elif set(unique_values) == {3, 4}:
        for i in range(3):
            output_grid[i,i] = 5


    return output_grid