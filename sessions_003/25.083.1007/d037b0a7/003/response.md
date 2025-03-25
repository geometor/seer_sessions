```python
"""
1.  **Seed Identification:** For each row in the input grid, find the rightmost non-zero pixel. This pixel's color is the "seed" color for that row. If a row has no non-zero pixels, it is skipped for horizontal and vertical filling.

2.  **Horizontal Filling:** For each row, if a seed color exists, iterate from the seed position *leftwards*.  Replace any non-zero pixel colors to the left of the seed with the seed color.

3.  **Vertical Filling:** Starting from the top row, propagate each filled row (rows where a seed color exists) downwards. For each subsequent row, replace any *non-zero* color with the color from the same column in the source row (filled row above). Stop when the bottom of the grid is reached.
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

    # Iterate through each row to perform seed identification and horizontal filling
    for i in range(rows):
        # Identify Seed: rightmost non-zero color
        rightmost_index = get_rightmost_nonzero(output_grid[i])

        #if no non-zero values, skip
        if rightmost_index is None:
          continue

        #get the seed
        seed_color = output_grid[i, rightmost_index]

        # Horizontal Propagation: go left setting colors
        for j in range(rightmost_index):  # Iterate only up to the rightmost index
            if output_grid[i, j] != 0:
                output_grid[i, j] = seed_color

    # Vertical Filling: Copy rows downwards, only replacing non-zero values
    for i in range(rows):
        rightmost_index = get_rightmost_nonzero(output_grid[i])
        if rightmost_index is None:
            continue  # Skip rows with no seed
        
        #seed color is from the output grid after horizontal fill
        seed_color = output_grid[i,rightmost_index]

        for k in range(i + 1, rows):
            for l in range(cols):
                # Only replace non-zero values
                if output_grid[k, l] != 0:
                    output_grid[k, l] = output_grid[i, l]

    return output_grid
```