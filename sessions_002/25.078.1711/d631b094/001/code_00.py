"""
1.  **Identify** the single non-zero color in the input grid.
2.  **Count** the number of times this non-zero color appears in the input grid.
3. **Create** output grid using the non-zero color from step 1:
    *   if the non-zero color appears twice, the output is a 1x2 grid
    *   if the non-zero color appears 3 times, the output grid is a 1x3 grid, etc.
4.  **Populate** the output grid completely with the identified non-zero color.
"""

import numpy as np

def get_nonzero_color(grid):
    # Flatten the grid and remove zeros
    non_zero_values = grid[grid != 0]
    # Return first element if exists, otherwise return default 0.
    return non_zero_values[0] if non_zero_values.size > 0 else 0

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the non-zero color
    non_zero_color = get_nonzero_color(input_grid)

    # Count the occurrences of the non-zero color
    count = np.count_nonzero(input_grid)

    # Create the output grid, row vector
    output_grid = np.full((1, count), non_zero_color)
    
    return output_grid.tolist()