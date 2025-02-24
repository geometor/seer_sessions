# 3631a71a • 016 • refine_coder

---
```python
"""
The transformation simplifies the input grid by reducing the length of linear stretches of colors to a maximum of 2, effectively shortening any horizontal or vertical series of identical colors that are 3 or more pixels long.
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

def shorten_series(grid, series_list):
    new_grid = np.copy(grid)
    for series in series_list:
        start, end, direction, color = series
        
        if direction == 'horizontal':
            if end[1] - start[1] + 1 >=3: #only make changes if len 3 or greater
              new_grid[start[0], start[1] + 2:end[1] + 1] = 0  #clear, leaving first two
        
        elif direction == 'vertical':
            if end[0] - start[0] + 1 >= 3:
              new_grid[start[0] + 2:end[0] + 1, start[1]] = 0  #clear, leaving first two

    return new_grid
    

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)

    # Get all series of length 3 or greater
    series = get_series(input_grid)
    # Shorten series
    output_grid = shorten_series(output_grid, series)

    return output_grid
```
