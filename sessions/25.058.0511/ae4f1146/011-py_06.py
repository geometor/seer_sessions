"""
1.  **Identify Objects:** Locate connected blocks of blue (1) and azure (8) pixels in the input grid.
2. Find the vertical lines of blue (1) and azure (8)
3. Recreate the vertical lines in the top right corner of a 3 x 3 grid.
4. Ignore all other objects
5. Mirror the objects on all axis
6. The output grid is always 3x3.
"""

import numpy as np

def find_vertical_lines(grid):
    """Finds vertical lines of color 1 and 8."""
    lines = []
    for j in range(grid.shape[1]):
        col = grid[:, j]
        line = []
        for i in range(len(col)):
            if col[i] == 1 or col[i] == 8:
                line.append((i, j, col[i]))
        if line:
            lines.append(line)
    return lines

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)
    input_grid = np.array(input_grid)

    # Find vertical lines of color 1 and 8.
    vertical_lines = find_vertical_lines(input_grid)

    # Extract relevant colors and their relative positions
    extracted_colors = []
    if vertical_lines:
        #consider only the last vertical line
        last_line = vertical_lines[-1]
        for cell in last_line:
          extracted_colors.append(cell[2])


    # Place the colors in the output grid
    row = 0
    for color in extracted_colors:
        if row < 3: #limit to 3x3
           output_grid[row, 2] = color
           row += 1

    # Mirror the object
    output_grid[0,0] = output_grid[0,2]
    output_grid[1,1] = output_grid[0,2]
    output_grid[2,0] = output_grid[2,2]
    output_grid[1,0] = output_grid[0,1] =  output_grid[0,2] #first row, last col
    if(output_grid.shape[0] > 1):
       output_grid[1,0] = output_grid[0,1] = output_grid[1,2] #second row
    if(output_grid.shape[0] > 2):
      output_grid[2,0] = output_grid[2,2] # third row

    return output_grid.tolist()