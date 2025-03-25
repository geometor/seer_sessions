```python
"""
1.  **Seed Identification:** For each row in the *input* grid, find the rightmost non-zero pixel. This is the "seed" pixel, and its value is the "seed color".

2.  **Horizontal Filling:** For each row:
    *   If a seed exists, iterate from the seed's position *leftwards* to the beginning of the row.
    *   Change any non-zero pixel encountered to the seed color.

3.  **Vertical Propagation:**
    *   Iterate through the rows of the grid from top to bottom.
    *    For each row *i*:
       *     If row *i* in the *original input* had a seed pixel:
            *    Copy all the non-zero cells from row i (after horizontal filling in step 2) to all rows below it, replacing any non-zero values.
            *  Do not copy values to rows above row *i*.
"""

import numpy as np

def get_rightmost_nonzero(row):
    """Finds the index of the rightmost non-zero element in a 1D array."""
    non_zero_indices = np.nonzero(row)[0]
    return non_zero_indices[-1] if non_zero_indices.size > 0 else None

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    input_copy = np.copy(input_grid)  # Keep a copy of the original input

    # Iterate through each row to perform seed identification and horizontal filling
    for i in range(rows):
        # Identify Seed: rightmost non-zero color in the *input* grid
        rightmost_index = get_rightmost_nonzero(input_copy[i])

        if rightmost_index is None:
            continue  # Skip rows with no seed

        seed_color = input_copy[i, rightmost_index]

        # Horizontal Filling: Iterate leftwards from the seed
        for j in range(rightmost_index):
            if output_grid[i, j] != 0:  # Only change non-zero pixels
                output_grid[i, j] = seed_color

    # Vertical Propagation: Copy rows downwards
    for i in range(rows):
        rightmost_index = get_rightmost_nonzero(input_copy[i])
        if rightmost_index is None:
            continue  # Skip rows that had no seed in the original input

        # Copy the horizontally-filled row 'i' to all subsequent rows
        for k in range(i + 1, rows):
            for l in range(cols):
                if output_grid[i, l] != 0: #copy only non-zero from source
                    output_grid[k, l] = output_grid[i, l]

    return output_grid
```