"""
1.  **Identify:** Find all non-black pixels (yellow and red) within the input grid.
2.  **Conditional Logic:**
    *   If there's only a single vertical line of yellow above red, there will be no transformation.
    *   Otherwise, swap the vertical positions of the red and yellow pixels.
    *   Conceptually: swap the *y*-coordinates of the highest yellow pixel with the *y*-coordinate of the lowest red pixel, *without* regard for their x-coordinates.
"""

import numpy as np

def find_colored_pixels(grid):
    """Finds the coordinates of non-black pixels (yellow and red)."""
    yellow_pixels = []
    red_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 4:
                yellow_pixels.append((r, c))
            elif grid[r, c] == 2:
                red_pixels.append((r, c))
    return yellow_pixels, red_pixels

def transform(input_grid):
    """Transforms the input grid according to the swapping rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    yellow_pixels, red_pixels = find_colored_pixels(input_grid)

    # Conditional Logic: Check for single vertical line of yellow above red
    if len(yellow_pixels) > 0 and len(red_pixels) > 0:
        is_single_column = all(p[1] == yellow_pixels[0][1] for p in yellow_pixels) and all(p[1] == red_pixels[0][1] for p in red_pixels) and yellow_pixels[0][1] == red_pixels[0][1]

        all_yellow_above_red = all(y[0] < r[0] for y in yellow_pixels for r in red_pixels)
        
        if is_single_column and all_yellow_above_red:
          return output_grid # no swap
        

    # Swap vertical positions (y-coordinates)
        highest_yellow_y = min(y[0] for y in yellow_pixels) if yellow_pixels else -1
        lowest_red_y = max(r[0] for r in red_pixels) if red_pixels else -1

        if highest_yellow_y != -1 and lowest_red_y != -1:
            for y_r, y_c in yellow_pixels:
                output_grid[y_r,y_c] = 0 # clear original spot
            for r_r, r_c in red_pixels:
                output_grid[r_r,r_c] = 0

            for y_r, y_c in yellow_pixels:

                output_grid[lowest_red_y - (y_r - highest_yellow_y) ,y_c] = 4 #move yellow to lowest_red spot

            for r_r, r_c in red_pixels:
                output_grid[highest_yellow_y + (lowest_red_y- r_r),r_c] = 2 #move red to highest yellow spot

    return output_grid