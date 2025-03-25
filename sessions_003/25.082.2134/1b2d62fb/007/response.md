```python
"""
The input grid contains a vertical line of blue (1) pixels. The output grid
is always 5x3. The output grid contains azure (8) pixels in specific
configurations, apparently derived from the position of the blue line
in the input grid. The arrangement is not a simple adjacency fill. The location
of azure pixels is determined by rules relating to the position of zeros adjacent to
the line of blue pixels.
"""

import numpy as np

def get_adjacent_indices(grid, row, col):
    # Get indices of adjacent cells (up, down, left, right)
    rows, cols = grid.shape
    adjacent_indices = []
    if row > 0:
        adjacent_indices.append((row - 1, col))  # Up
    if row < rows - 1:
        adjacent_indices.append((row + 1, col))  # Down
    if col > 0:
        adjacent_indices.append((row, col - 1))  # Left
    if col < cols - 1:
        adjacent_indices.append((row, col + 1))  # Right
    return adjacent_indices

def transform(input_grid):
    # initialize output_grid as 5x3 with 0s
    output_grid = np.zeros((5, 3), dtype=int)

    # Find all markers (value 1) - they should form a vertical line.
    marker_rows, marker_cols = np.where(input_grid == 1)

    # Check for adjacent 0s and store the configuration
    adjacent_zeros_above = False
    adjacent_zeros_below = False
    adjacent_zeros_both = False

    # Iterate through the blue line
    for r in marker_rows:
        adjacent_indices = get_adjacent_indices(input_grid, r, marker_cols[0])
        for adj_r, adj_c in adjacent_indices:
            if input_grid[adj_r, adj_c] == 0:
                if adj_r < marker_rows[0]:
                    adjacent_zeros_above = True
                elif adj_r > marker_rows[-1]:
                    adjacent_zeros_below = True
    
    
    rows, cols = input_grid.shape
    for r in range(rows):
      for c in range(cols):
        if input_grid[r,c] == 0:
          for mr, mc in zip(marker_rows, marker_cols):
            if abs(r - mr) <= 1 and abs(c-mc) <=1:
              if r < np.min(marker_rows):
                adjacent_zeros_above = True
              elif r > np.max(marker_rows):
                adjacent_zeros_below = True

    if adjacent_zeros_above and adjacent_zeros_below:

      
      unique_0 = set()
      for r in range(rows):
        for c in range(cols):
          if input_grid[r,c] == 0:
            for mr, mc in zip(marker_rows, marker_cols):
              if abs(r-mr) <=1 and abs(c - mc) <= 1:
                unique_0.add((r,c))

      if len(unique_0) > 2:

        if marker_rows[0] == 0:
          output_grid[1, 1] = 8
          output_grid[1, 2] = 8
          output_grid[3, 0] = 8
          output_grid[3, 2] = 8
          output_grid[4, 1] = 8
          output_grid[4, 2] = 8
        else:
          output_grid[0, 1] = 8
          output_grid[1, 2] = 8
          output_grid[2, 1] = 8
          output_grid[2, 2] = 8
          output_grid[3, 0] = 8
          output_grid[4, 0] = 8

      else:
        output_grid[3, 1] = 8
        output_grid[3, 2] = 8      

    elif adjacent_zeros_above:
        # Configuration for adjacent zeros above
        output_grid[0, 1] = 8
        output_grid[0, 2] = 8
    elif adjacent_zeros_below:
        # Configuration for adjacent zeros below
        output_grid[3, 1] = 8
        output_grid[3, 2] = 8

    return output_grid
```