# 3631a71a • 018 • refine_coder

---
```python
"""
The transformation identifies horizontal and vertical series of identical colors with a length of 3 or more pixels. It shortens these series to a maximum length of 2 and shifts the remaining pixels to fill the gap.
"""

import numpy as np

def get_series(grid):
    series_list = []
    rows, cols = grid.shape

    # Horizontal series
    for r in range(rows):
        c = 0
        while c < cols:
            color = grid[r, c]
            length = 1
            while c + length < cols and grid[r, c + length] == color:
                length += 1
            if length >= 3:
                series_list.append(((r, c), (r, c + length - 1), 'horizontal', color))
            c += length

    # Vertical series
    for c in range(cols):
        r = 0
        while r < rows:
            color = grid[r, c]
            length = 1
            while r + length < rows and grid[r + length, c] == color:
                length += 1
            if length >= 3:
                series_list.append(((r, c), (r + length - 1, c), 'vertical', color))
            r += length

    return series_list

def shorten_and_shift(grid, series_list):
    new_grid = np.copy(grid)
    rows, cols = new_grid.shape
    
    # Keep track of how much each column has shifted
    horizontal_shifts = {r: 0 for r in range(rows)}

    for series in series_list:
        start, end, direction, color = series

        if direction == 'horizontal':
            series_length = end[1] - start[1] + 1
            if series_length >= 3:
                remove_count = series_length - 2
                row = start[0]
                start_col = start[1]

                # Shift elements to the left
                for c in range(start_col + 2, cols):
                    shifted_col = c - remove_count
                    if shifted_col < cols:
                        new_grid[row, shifted_col] = new_grid[row, c]
                
                # Update horizontal shifts for this row
                horizontal_shifts[row] += remove_count

    # Create the final grid after horizontal shifts
    final_grid = np.zeros((rows, cols - max(horizontal_shifts.values())), dtype=int)
    for r in range(rows):
      final_grid[r,:] = new_grid[r,:cols - horizontal_shifts[r]] #use the shift to trim

    #Vertical
    new_grid = np.copy(final_grid)
    rows,cols = new_grid.shape
    vertical_series = [s for s in series_list if s[2] == 'vertical']
    
    for series in vertical_series:
      start, end, direction, color = series
      series_length = end[0] - start[0] + 1
      if series_length >=3:
          remove_count = series_length -2
          col = start[1]
          start_row = start[0]
          #shift elements up
          for r in range(start_row + 2, rows):
            shifted_row = r - remove_count
            if shifted_row < rows:
              new_grid[shifted_row,col] = new_grid[r,col]
          #clear the bottom rows that were shifted from
          for r in range(rows - remove_count, rows):
            new_grid[r,col] = 0

    return new_grid

def transform(input_grid):
    # Get all series of length 3 or greater
    series = get_series(input_grid)
    # Shorten series and shift
    output_grid = shorten_and_shift(input_grid, series)

    return output_grid
```
