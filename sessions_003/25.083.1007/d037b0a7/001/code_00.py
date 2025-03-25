"""
The rightmost non-zero color in each row is setting colors to the left, then the full row is propagated downwards, filling the output grid below that row with the color, and stopping with the grid boundary.
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

    # Iterate through each row
    for i in range(rows):
        # Identify Seed: rightmost non-zero color
        rightmost_index = get_rightmost_nonzero(output_grid[i])

        #if no non-zero values, skip
        if rightmost_index is None:
          continue

        #get the seed
        seed_color = output_grid[i, rightmost_index]

        # Propagation: go left setting colors
        for j in range(cols):
            if output_grid[i,j] != 0 and j < rightmost_index:
              output_grid[i,j] = seed_color
        
    # Copy down: Copy all rows downwards
    for i in range(rows):
      # Identify Seed: rightmost non-zero color
      rightmost_index = get_rightmost_nonzero(output_grid[i])
      if rightmost_index is None:
        continue

      seed_color = output_grid[i, rightmost_index]
      for k in range(i + 1,rows):
        for l in range(cols):
          if output_grid[k,l] != 0:
            output_grid[k,l] = output_grid[i,l]

    return output_grid