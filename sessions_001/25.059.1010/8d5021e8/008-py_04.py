"""
1.  **Grid Expansion:** The output grid's height is three times the input grid's height, and its width is twice the input grid's width.
2.  **Column Duplication:** Each column in the input grid corresponds to *two* columns in the output grid.
3.  **Pixel Mapping and Replication:** For each pixel in the input grid at position (y, x), consider the corresponding 3x2 block in the output grid starting at position (3y, 2x). The pixel at (y,x) maps onto the output block at (3y, 2x).
4.  **Color Propagation:** Fill the top-left pixel (3y, 2x) of the output grid's 3x2 block with the color of the input pixel (y,x). Fill the rest of the rows, so the result will have three rows of color.
5. **White Rows Insertion:** Fill the two rows after the three rows with white.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    input_height, input_width = input_grid.shape
    output_height = input_height * 3
    output_width = input_width * 2
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # change output pixels
    for y in range(input_height):
        for x in range(input_width):
            # get color of current input pixel
            color = input_grid[y, x]

            # map to output block and fill top-left pixel
            output_y = 3 * y
            output_x = 2 * x
            output_grid[output_y, output_x] = color

            # fill 3 rows
            for i in range(3):
              output_grid[output_y + i, output_x] = color

            # duplicate color for next column
            output_grid[output_y, output_x+1] = color
            # fill next column 3 rows
            for i in range(3):
               output_grid[output_y+i, output_x+1] = color

    # insert white rows
    for y in range(output_height):
      if (y % 3 == 1) or (y % 3 == 2) :
        for x in range(output_width):
          output_grid[y,x] = 0

    return output_grid