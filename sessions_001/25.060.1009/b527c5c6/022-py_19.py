"""
1.  **Identify Key Pixels:** Locate the isolated red (2) pixels in the input grid.

2.  **Vertical Expansion (Green):** The large green (3) region expands downwards. It takes over the rows containing the red pixel on the top-left, keeping the original width of the green area and its leftmost coordinate.

3. **Transformation of the Top Left Red Pixel:** the red pixel at the top, expands vertically along the entire height of the grid. Keeping the original x coordinate.

4.  **Transformation of the Bottom Right Red Pixel:** The red pixel at row 13, changes into horizontal line of red pixels to the right. This starts from where the isolated red pixel was, and now occupies the whole width of the original object made by the green color.
    The whole red line also moves up by one row, to start now at row 12.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels of the given color
    return np.array(np.where(grid == color)).T

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Find the isolated red pixels
    red_pixels = find_object(input_grid, 2)
    
    # Find top-left green object boundary
    green_pixels = find_object(input_grid, 3)
    if len(green_pixels) > 0:  # Check if green_pixels is not empty
        min_green_row = np.min(green_pixels[:, 0])
        max_green_row = np.max(green_pixels[:, 0])
        min_green_col = np.min(green_pixels[:, 1])
        max_green_col = np.max(green_pixels[:, 1])


    # 1. Vertical expansion of green
    if len(red_pixels) > 0 and len(green_pixels) > 0 :
        for r_pix in red_pixels:
            if r_pix[0] > max_green_row:
                continue # we only deal here with red pixel above green bottom
            for col in range(min_green_col, max_green_col+ 1):
                output_grid[r_pix[0], col] = 3

    # 2. Transform top-left red pixel to vertical line
    if len(red_pixels) > 0 :
        for r_pix in red_pixels:
            if r_pix[0] <= max_green_row:
                output_grid[:, r_pix[1]] = 2
                break  # Assuming only one such pixel, we break after finding first.


    # 3. Bottom-right red pixel expansion + moving 1 row up.
    if len(red_pixels) > 0 and len(green_pixels) > 0:  # Ensure green_pixels is not empty
        for r_pix in red_pixels:
            if r_pix[0] > max_green_row: # we want the lower red pixel
                row = r_pix[0] -1
                for col in range(r_pix[1], max_green_col + 1):
                    output_grid[row,col] = 2
                output_grid[r_pix[0], r_pix[1]] = input_grid[r_pix[0], r_pix[1]] # cleanup original pixel - no change

    return output_grid