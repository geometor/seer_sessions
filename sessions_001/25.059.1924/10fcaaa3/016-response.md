# 10fcaaa3 • 016 • refine_coder

---
```python
"""
Transforms an input grid into an output grid based on the following rules:

1.  **Input Analysis:** Examine the input grid to determine its dimensions (height, width) and the presence and location of any yellow pixels (value 4) and white pixels (value 0).

2.  **Output Grid Initialization:**
    *   The output grid's width is always twice the input grid's width.
    *   The output grid height is determined as follows:
        *   If there are no yellow pixels, the output grid's height equals the number of white pixel rows x 2.
        *   If there are yellow pixels:
            *    If yellow is the only color in the row, the output height is 2.
            *    If the input grid contains both yellow and white, expand white pixels to 2x2 white blocks.
               When a yellow pixel is present, expand the yellow pixel to a 2x2 yellow block.
               Place the yellow 2x2 block at output row 0, and column at 2x the input yellow pixel column
               White blocks are placed by expanding white pixels, starting at row 0, skipping rows when there are yellow pixels.

3.  **Pixel Expansion:**
    *   **White Pixels:** Every white pixel (0) in the input grid is replaced by a 2x2 block in the output grid with the pattern: `[[8, 0], [0, 8]]` (azure and white).
    *   **Yellow Pixels:** If a yellow pixel (4) is present in the input grid, it is expanded into a 2x2 block in the output grid with the pattern: `[[4, 4], [4, 4]]` (all yellow).

4.  **Yellow Block Placement (if Yellow exists):**

   * The output grid has at least two rows
   * The expanded yellow 2x2 block in placed with it's top-left corner at output row 0 if the only pixel in that row is yellow.
   * The 2x2 yellow block is placed starting at the column = 2 * the original yellow pixel's column.

5. **White Block Placement**

   * White blocks are placed by expanding in place each of the white pixels to the 2x2 white block.
   * If there are no yellow pixels, they expand in place, doubling the output height, as well as doubling the output width.
   * When there are yellow pixels, the white blocks are placed beginning at row 0, but skipping rows when there is a yellow pixel block.

6.  **Output:** The final output grid is formed by applying these expansions and placements. The yellow block, if present, takes priority over any overlapping white blocks.
"""

import numpy as np

def find_yellow_pixels(grid):
    # Helper function to find the coordinates of all yellow pixels.
    grid = np.array(grid)
    return np.argwhere(grid == 4)

def find_white_pixels(grid):
    # Helper function to find coordinates of all white pixels
    grid = np.array(grid)
    return np.argwhere(grid == 0)

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    yellow_pixels = find_yellow_pixels(input_grid)
    white_pixels = find_white_pixels(input_grid)
    has_yellow = len(yellow_pixels) > 0

    if not has_yellow:
        output_height = rows * 2
        output_grid = np.zeros((output_height, cols * 2), dtype=int)
    else:
       #check if the yellow pixel's row has any other colors
        yellow_row = yellow_pixels[0][0]
        if np.all(input_grid[yellow_row, :] == input_grid[yellow_row, 0]): #all elements the same
          output_height = 2
          output_grid = np.zeros((output_height, cols*2), dtype=int)
        else: # mix of yellow and white
          output_height = 0
          for i in range(rows):
            if 4 in input_grid[i]:
              output_height +=1
            elif 0 in input_grid[i]:
              output_height += 2
          output_grid = np.zeros((output_height, cols*2),dtype=int)


    # change output pixels

    # Expand white pixels
    if not has_yellow:
        for i in range(rows):
            for j in range(cols):
                if input_grid[i, j] == 0:
                    output_grid[2 * i, 2 * j] = 8
                    output_grid[2 * i, 2 * j + 1] = 0
                    output_grid[2 * i + 1, 2 * j] = 0
                    output_grid[2 * i + 1, 2 * j + 1] = 8
    else:
      #place yellow block:
      yellow_row, yellow_col = yellow_pixels[0]
      #if input_grid[yellow_row,yellow_col]
      output_grid[0, 2 * yellow_col] = 4
      output_grid[0, 2 * yellow_col + 1] = 4
      output_grid[1, 2 * yellow_col] = 4
      output_grid[1, 2 * yellow_col + 1] = 4
      output_row = 0
      for i in range(rows):
        if 4 in input_grid[i]:
          continue #yellow block already placed
        for j in range(cols):
          if input_grid[i,j] == 0:

            output_grid[output_row, 2 * j] = 8
            output_grid[output_row, 2 * j + 1] = 0
            output_grid[output_row+ 1, 2 * j] = 0
            output_grid[output_row + 1, 2 * j + 1] = 8
        if 0 in input_grid[i]: #only increment if it had white pixels
          output_row += 2
          #print(f"checking {i} and {output_row}")

    return output_grid
```
