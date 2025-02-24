"""
The transformation simplifies the input grid by reducing the length of linear stretches of colors, and removing many series altogether. Specifically:
1. Identify Series/Strings: Locate all horizontal and vertical series of adjacent pixels with identical colors that have a length of 3 or 4.
2. Shorten: For each identified series, reduce its length to 2.
3. Locate complex areas: Identify areas where many series of different numbers converge or intersect.
4. Remove: In areas where multiple different series meet, remove the complete series.
"""

import numpy as np

def get_series(grid, length):
    series_list = []
    rows, cols = grid.shape

    # Horizontal series
    for r in range(rows):
        for c in range(cols - length + 1):
            if len(set(grid[r, c:c+length])) == 1:
                series_list.append(((r, c), (r, c+length-1), 'horizontal', grid[r,c]))

    # Vertical series
    for r in range(rows - length + 1):
        for c in range(cols):
            if len(set(grid[r:r+length, c])) == 1:
                series_list.append(((r, c), (r+length-1, c), 'vertical', grid[r,c]))

    return series_list

def shorten_series(grid, series_list):
  new_grid = np.copy(grid)
  for series in series_list:
        start, end, direction, color = series
        
        if direction == 'horizontal':
            if end[1] - start[1] + 1 >=3: #only make changes if len 3 or 4
              new_grid[start[0], start[1] + 1:end[1]] = 0  #clear, leaving first
        
        elif direction == 'vertical':
            if end[0] - start[0] + 1 >= 3:
              new_grid[start[0] + 1:end[0], start[1]] = 0

  return new_grid
    

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Get series of length 3
    series_3 = get_series(input_grid, 3)
    # Shorten series of length 3
    output_grid = shorten_series(output_grid, series_3)

    # Get series of length 4
    series_4 = get_series(output_grid, 4)  # Use output_grid here, not the original
    # Shorten series of length 4
    output_grid = shorten_series(output_grid, series_4)


    return output_grid