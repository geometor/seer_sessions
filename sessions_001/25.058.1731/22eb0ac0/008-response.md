# 22eb0ac0 • 008 • refine_coder

---
```python
"""
1.  **Identify the Special Row:** Iterate through each row of the input grid. The "special row" is the first row where a change occurs between input and output. If there are *no* changes between the input and output, there is no change made to the special row in the output grid.
2.  **Determine the Replacement Action:**
    *   If the special row contains only one non-zero color, that entire row does not get changed.
    *   If the special row contains a mix of zeros and non-zeros, the row will be filled with the leftmost non-zero.
3.  **Fill or Copy:**
    *    If a special row is found, and needs changing, fill the entire corresponding row in the *output* grid with the replacement color.
    *   All other rows in the output grid are identical to the corresponding rows in the input grid.
"""

import numpy as np

def get_leftmost_nonzero(row):
    """Finds the leftmost non-zero element in a row."""
    for pixel in row:
        if pixel != 0:
            return pixel
    return 0

def find_special_row(input_grid, output_grid):
    """Identifies the index of the special row."""
    for i in range(len(input_grid)):
        if not np.array_equal(input_grid[i], output_grid[i]):
            return i
    return -1  # No special row found

def determine_replacement_color(row):
    """Determines the replacement color for the special row."""
    non_zero_pixels = [pixel for pixel in row if pixel != 0]
    unique_non_zero_pixels = set(non_zero_pixels)
    
    if len(unique_non_zero_pixels) <= 1 :
        return None # no replacement
    elif len(unique_non_zero_pixels) > 1:
        return get_leftmost_nonzero(row) # replace with leftmost
    else:
        return None
    

def transform(input_grid, output_grid):
    # initialize output_grid as a copy of input_grid
    output_grid_copy = np.copy(input_grid)

    # Find the special row index
    special_row_index = find_special_row(input_grid, output_grid)


    # if no special row, return copy of input
    if special_row_index == -1:
        return output_grid_copy
    
    # get the special row
    special_row = input_grid[special_row_index]

    # Determine the replacement color
    replacement_color = determine_replacement_color(special_row)

    # if there is a replacement_color, change the row
    if replacement_color is not None:
        output_grid_copy[special_row_index] = np.full(len(special_row), replacement_color)

    # return the updated grid
    return output_grid_copy
```
