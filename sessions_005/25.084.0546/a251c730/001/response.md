```python
"""
1.  **Identify the central region:** Determine a central region within the input grid. This region appears to be defined by consistent internal color, and it can vary.
2.  **Crop the Grid:** Find the top most and bottom most rows where we can find colors other than the top and bottom most color. The slice the image vertically to remove left and right columns where the pixel value equal the first and last value.
3. **Remove outside band** Remove the one unit band of uniform color at the boarder.
4.  **Return Center:** Extract the inner core and return it as the output grid.
"""

import numpy as np

def crop_grid(grid):
    # Find the top and bottom rows with colors different from the background
    first_color = grid[0, 0]
    last_color = grid[-1, 0]

    top_row = 0
    for i in range(grid.shape[0]):
        if not np.all(grid[i] == first_color):
            top_row = i
            break

    bottom_row = grid.shape[0] - 1
    for i in range(grid.shape[0] - 1, -1, -1):
        if not np.all(grid[i] == last_color):
            bottom_row = i
            break
    
    # Find first and last col
    first_col = 0
    for j in range(grid.shape[1]):
        if not (grid[top_row,j] == first_color and grid[bottom_row,j] == last_color) :
            first_col = j
            break
    
    last_col = grid.shape[1]-1
    for j in range(grid.shape[1]-1, -1, -1):
        if not (grid[top_row,j] == first_color and grid[bottom_row,j] == last_color):
            last_col = j
            break

    # Crop the grid
    cropped_grid = grid[top_row : bottom_row + 1, first_col: last_col + 1]
    return cropped_grid

def remove_outer_band(grid):
    # Remove the one-unit band of uniform color at the border
    return grid[1:-1, 1:-1]


def transform(input_grid):
    # Convert input to numpy array
    grid = np.array(input_grid)

    # Crop grid
    cropped = crop_grid(grid)

    # Remove outer band
    inner_core = remove_outer_band(cropped)
    
    return inner_core.tolist()
```