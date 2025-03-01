"""
1.  **Create Output Grid:** Create an output grid that is twice the width of the input grid. The output grid height is also based on the input, calculated as `2 * input_height - (input_height % 2)`.
2.  **Locate Red Pixel:** Find the red pixel (value 2) in the input grid.
3.  **Place First Red Pixel**: Copy the red pixel to the output grid at row = `input_row * 2 - (input_row % 2)` and col = `input_col * 2`
4.  **Place Second Red Pixel:** Place a second red pixel in the output grid. This pixel is vertically mirrored from the first red pixel. Row = `output_height - 1 - first_red_pixel_row`, col = `first_red_pixel_col`.
5.  **Azure Fill:** In the rows that contain the red pixels, fill every other cell with azure (value 8), starting from column 0.
6.  **Retain Background:** all white pixels should be present in output
"""

import numpy as np

def transform(input_grid):
    # Create output grid
    input_height, input_width = input_grid.shape
    output_height = 2 * input_height - (input_height % 2)
    output_width = 2 * input_width
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Retain background (white pixels)
    for i in range(input_height):
        for j in range(input_width):
            if input_grid[i,j] == 0:
                # Calculate correct output indices
                out_i = i * 2 - (i % 2)
                
                # Ensure mapping to input rows don't exceed output height
                if(out_i < output_height):
                  for k in range(2):
                      output_grid[out_i, j*2 + k] = 0
                

    # Locate red pixel
    red_pixels = np.argwhere(input_grid == 2)

    for red_pixel in red_pixels:
        # Place first red pixel
        input_row, input_col = red_pixel
        first_red_pixel_row = input_row * 2 - (input_row % 2)
        first_red_pixel_col = input_col * 2
        output_grid[first_red_pixel_row, first_red_pixel_col] = 2

        # Place second red pixel (vertical mirroring)
        second_red_pixel_row = output_height - 1 - first_red_pixel_row
        output_grid[second_red_pixel_row, first_red_pixel_col] = 2

        # Azure fill
        for row in [first_red_pixel_row, second_red_pixel_row]:
            for col in range(0, output_width, 2):
                output_grid[row, col] = 8

    return output_grid