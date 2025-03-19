"""
1.  **Identify Gray Pixels:** Locate all gray pixels (value 5) in the input grid. These pixels will not change.

2.  **Transform White Pixels:** Iterate through the white pixels (value 0). Their transformation depends on their position relative to gray pixels:

    *   **Below Right of Gray:** If a white pixel is *directly below and directly to the right* of a gray pixel, change it to yellow (4).
    *    **To the Right of Gray:**
        * If a white pixel is *directly to the right* of a gray pixel and another gray pixel is directly *below and to the left* of current position, change it to red (2)
        *  If a white pixel *is at the top left and to the right* of a gray pixel, change it to red (2).
        * If a white pixel is *directly to the right* of a gray pixel, change it to red (2).
    * **Directly Below Gray:** If a white pixel is directly below of gray, and *at the top left corner*, change it to red(2).

3.  **Output:** Create the output grid by applying these changes. The gray pixels remain the same, and the white pixels are transformed according to the rules above.
"""

import numpy as np

def get_gray_pixels(grid):
    # find coordinates of gray pixels
    gray_pixels = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 5:
                gray_pixels.append((i, j))
    return gray_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    gray_pixels = get_gray_pixels(input_grid)

    # change output pixels
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] == 0:  # White pixel
                is_below_right_of_gray = False
                is_right_of_gray = False
                is_top_left_right_of_gray = False
                is_directly_below_gray_top_left_corner = False


                for gray_row, gray_col in gray_pixels:
                    # Below Right of Gray
                    if i == gray_row + 1 and j == gray_col + 1:
                        is_below_right_of_gray = True

                    # To the Right of Gray
                    if j == gray_col + 1:
                        is_right_of_gray = True

                    # Top Left and to the right of Gray
                    if i == 0 and j == 1 and gray_col == 0:
                        is_top_left_right_of_gray = True
                        
                    # Directly below a gray, top left
                    if i == gray_row + 1 and i == 1 and j == 0:
                        is_directly_below_gray_top_left_corner = True


                if is_below_right_of_gray:
                    output_grid[i, j] = 4
                elif is_right_of_gray:
                    output_grid[i,j] = 2
                elif is_top_left_right_of_gray:
                    output_grid[i,j] = 2
                elif is_directly_below_gray_top_left_corner:
                    output_grid[i,j] = 2


    return output_grid