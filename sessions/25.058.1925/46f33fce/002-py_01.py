"""
The transformation rule is as follows:

1. Iterate through each pixel in the input grid.
2. If the pixel is not the background color (0), expand it into a 4x4 block of the same color.
3. The top-left corner of the 4x4 block is determined by rounding the original pixel's row and column indices down to the nearest multiple of 4.
4. Place the expanded block in the output grid.
5. Repeat until all pixels are processed.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_rows = rows * 2
    output_cols = cols * 2
    if output_rows < 20 : output_rows = 20
    if output_cols < 20: output_cols = 20

    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Iterate through each pixel of the input grid
    for i in range(rows):
        for j in range(cols):
            pixel_color = input_grid[i, j]

            # Check if it is not the background
            if pixel_color != 0:
                # Determine top-left corner of the block
                block_row_start = (i // 4) * 4
                block_col_start = (j // 4) * 4

                # Expand into a 4x4 block
                for row_offset in range(4):
                    for col_offset in range(4):
                        output_grid[block_row_start + row_offset, block_col_start + col_offset] = pixel_color
    
    # increase output rows and cols
    output_rows = (rows//4 + 1) * 4
    output_rows = max(output_rows,(rows//4) * 4 + 4 )
    if rows <= output_rows -4:
        if rows * 2 > output_rows:
            output_rows = rows*2

    output_cols = (cols//4 + 1) * 4
    output_cols = max(output_cols, (cols//4) * 4 + 4)
    if cols <= output_cols -4:
          if cols *2 > output_cols:
              output_cols = cols * 2

    output_grid = output_grid[:output_rows, :output_cols]


    return output_grid.tolist()