# 1b2d62fb • 018 • refine_coder

---
```python
"""
1.  **Identify a Vertical Blue Line:** Examine the input grid to find a vertical line composed entirely of blue (1) pixels. If no such line exists, skip to step 4.
2.  **Create Output Grid.** If the vertical blue line exists, create a new grid with the same height as the input grid, and with width of 3.
3.  **Transformation (Blue Line Case):**
    *   **Left Column:** Select the column immediately to the left of the blue line. Transform it based on the colors present, replacing only the colors that also appear adjacent to the blue line with white.
    *   **Center Column:** Transform the blue line itself by replacing all blue pixels with white.
    *    **Right Column:** Select the column immediately to the right of the blue line. Transform this column based on colors adjacent to the blue line, replacing them with the white and other colors as indicated in the examples.
4.  **No Vertical Blue Line Case:** If no continuous vertical blue line is found, perform one of the following actions:
    * If any blue is present, change all pixels to white.
    * If there is no blue present, return the original grid.
"""

import numpy as np

def find_blue_line(grid):
    # Find the column index of the vertical blue line.
    height = len(grid)
    width = len(grid[0])
    for j in range(width):
        is_blue_line = True
        for i in range(height):
            if grid[i][j] != 1:
                is_blue_line = False
                break
        if is_blue_line:
            return j
    return -1  # Return -1 if no blue line is found

def get_adjacent_colors(grid, blue_line_col):
    # returns the set of colors present adjacent to blue_line_col
    height, width = grid.shape
    adjacent_colors = set()

    if blue_line_col > 0:
        for i in range(height):
            adjacent_colors.add(grid[i][blue_line_col-1])
    if blue_line_col < width -1:
        for i in range(height):
            adjacent_colors.add(grid[i][blue_line_col + 1])

    return adjacent_colors

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    height, width = input_grid.shape
    
    # Find the blue line
    blue_line_col = find_blue_line(input_grid) # this should be index 3

    if blue_line_col != -1:
        output_grid = np.zeros((height, 3), dtype=int)
        adjacent_colors = get_adjacent_colors(input_grid, blue_line_col)

        # process column to left of blue line
        if blue_line_col > 0:
          for i in range(height):
              if input_grid[i][blue_line_col - 1] in adjacent_colors:
                output_grid[i][0] = 0  # white
              if input_grid[i][blue_line_col -1] == 0 and 8 in adjacent_colors: # additional rule based on example 1
                output_grid[i][0] = 8

        # process the blue line itself, turning to white
        for i in range(height):
            output_grid[i][1] = 0

        # process column to right of blue line
        if blue_line_col < width - 1:
            for i in range(height):
              if input_grid[i][blue_line_col+1] in adjacent_colors:
                output_grid[i][2] = 0
              if input_grid[i][blue_line_col+1] == 0 and 8 in adjacent_colors: # additional rule based on example 1
                output_grid[i][2] = 8

    else:  # No blue line found
        if 1 in input_grid:  # Any blue present?
            output_grid = np.zeros((height, width), dtype=int) # all white
        else:
            output_grid = input_grid.copy() # return original grid
        

    return output_grid.tolist()
```
