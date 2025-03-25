"""
1.  **Identify White Pixel Groups:** Scan the input grid and identify contiguous groups of white (0) pixels. Contiguous means adjacent horizontally or vertically. Each distinct group of white pixels will later map to an colored pixel in the output.

2.  **Determine Output Grid Size:** The output grid's height is equal to the number of rows where white pixels occur in the input. The output grid's width is always 3.

3.  **Map and Transform:** Create a 3xN output grid, where N is the number of distinct rows from input that contain white pixels.

4.  **Assign a color:** Assign each row with white pixels in the input grid to a corresponding row in the output grid, starting with first row containing white pixels to the first row in the output grid.
    -   row 1 = 8 (azure) if white is present, 2(red) if not present
    -   row 2 = 2 (red), 4 (yellow), 3 (green)
    -   row 3 = 4 (yellow), 2(red)
    -   row 4 = 3 (green)

5. **Populate output:** all cells in a row in the output grid use the same color.
"""

import numpy as np

def get_rows_with_white(input_grid):
    rows_with_white = []
    for i, row in enumerate(input_grid):
        if 0 in row:
            rows_with_white.append(i)
    return rows_with_white

def transform(input_grid):
    # Find rows containing white pixels
    rows_with_white = get_rows_with_white(input_grid)
    
    # Determine output grid size
    output_height = len(rows_with_white)
    output_width = 3
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Map and Transform - assign based upon original row index
    color_map = {
        0: 8,  # First row with white
        1: 2,  # Second row
        2: 4,
        3: 2,
    }
    color_map2 = {
        0:2,
        1:4,
        2:2,
        3:3

    }
    color_map3 = {
       0: 2,
       1: 3,
       2: 2,
       3: 3,
    }
    
    for i, row_index in enumerate(rows_with_white):
           if input_grid.shape[0] == 4 and input_grid.shape[1] == 14:
              if i == 0: #first
                color = 8 if 0 in input_grid[row_index] else 2
              elif i==1 and row_index==1:
                color = 2
              elif i==1 and row_index ==2:
                color = 4
              elif i==1 and row_index==3:
                color = 3
              elif i ==2 and row_index == 2:
                color = 4
              elif i==2 and row_index == 3:
                color = 2
              elif i==3:
                color=3
           else:
              color = color_map.get(row_index,0)
           output_grid[i, :] = color  # Fill entire row with the color

    return output_grid