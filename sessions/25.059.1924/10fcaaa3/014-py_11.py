"""
Transforms an input grid into an output grid based on the following rules:

1.  **Initialization:**
    *   Examine the input grid. Determine its dimensions (height, width).
    *   Identify the row index (`i`) of the yellow pixel (value 4). If no yellow pixel exists, skip the yellow-related steps.
    *   The output will have the a height of 6, and a width equal to the input width times 2.

2.  **Yellow Pixel Handling (if present):**
    *   A single yellow pixel at `input[i,j]` in the input grid is transformed into a 2x2 block of yellow pixels in the output grid.
    *   The yellow 2x2 block will always appear at a specific row, determined by the original yellow pixel position in the input grid:
        *  If the yellow pixel is at row i of the input grid, the 2x2 yellow block's top-left corner is at row (2 + row), and the original column x 2.

3.  **White Pixel Handling:**
    *   Each white pixel (value 0) in the input grid is replaced by a 2x2 block in the output grid.
    *   The 2x2 block has the following pattern:
        ```
        8 0
        0 8
        ```
        where 8 represents azure and 0 represents white.
    *   The white pixels are expanded to the 2x2 blocks, and inserted into the correct locations, skipping rows when needed to accomodate the position of the yellow block.

4. **No Yellow Pixel:**
    * If there is no yellow pixel in the input grid, white pixels are expanded in place.

5.  **Output:** The resulting output grid is a transformed version of the input grid, with expanded dimensions and the 2x2 block substitutions.
"""

import numpy as np

def find_yellow_pixel(grid):
    # Helper function to find the coordinates of the yellow pixel.
    grid = np.array(grid)
    yellow_coords = np.argwhere(grid == 4)
    if yellow_coords.size > 0:
        return yellow_coords[0]  # Return only the first yellow pixel if multiple exist
    else:
        return None

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros((6, cols * 2), dtype=int)

    yellow_pixel = find_yellow_pixel(input_grid)

    # change output pixels

    if yellow_pixel is not None:
      yellow_row, yellow_col = yellow_pixel
      # Place the 2x2 yellow block.
      output_grid[2 + yellow_row, 2 * yellow_col] = 4
      output_grid[2 + yellow_row, 2 * yellow_col + 1] = 4
      output_grid[3 + yellow_row, 2 * yellow_col] = 4
      output_grid[3 + yellow_row, 2 * yellow_col + 1] = 4
        
      # Fill in the white pixel expansions, skipping rows as needed.
      output_row = 0
      for i in range(rows):
          for j in range(cols):
              if input_grid[i,j] == 0:
                if output_row == 2 + yellow_row or output_row == 3+yellow_row:
                      output_row += 2 #skip rows for yellow block.
                output_grid[output_row, 2 * j] = 8
                output_grid[output_row, 2 * j + 1] = 0
                output_grid[output_row + 1, 2 * j] = 0
                output_grid[output_row + 1, 2 * j + 1] = 8
          output_row +=2
          if output_row >= 6:
            break
    else: #no yellow pixel
        for i in range(rows):
          for j in range(cols):
            if input_grid[i,j] == 0:
              output_grid[2 * i, 2 * j] = 8
              output_grid[2 * i, 2 * j + 1] = 0
              output_grid[2*i + 1, 2 * j] = 0
              output_grid[2*i + 1, 2 * j + 1] = 8


    return output_grid