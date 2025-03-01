"""
1.  **Locate:** Find the single red (2) pixel and the single green (3) pixel within the input grid. These are the start and end points.
2.  **Horizontal Segment:** Starting at the red pixel's location, draw a horizontal line of azure (8) pixels.
    *   The line extends to the column *immediately before* the green pixel's column if the green pixel is to the right of the red pixel.
    *   The line extends to the column *immediately after* the green pixel's column if the green pixel is to the left of the red pixel.
3.  **Vertical Segment:**
    *   If a horizontal segment was drawn:  From the last azure pixel of the horizontal segment, draw a vertical line of azure (8) pixels extending *to the same row as* the green pixel.
    * If no horizontal segment was drawn: Do not draw a vertical segment.
4. The red and green pixels must remain with their original color values.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the location of the first pixel of a given color."""
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.copy(input_grid)
    input_grid_array = np.array(input_grid)

    # 1. Locate red and green pixels
    red_loc = find_pixel(input_grid_array, 2)
    green_loc = find_pixel(input_grid_array, 3)

    if red_loc is None or green_loc is None:
        return output_grid  # Return original if either pixel is missing

    # 2. Horizontal Segment
    if red_loc[1] < green_loc[1]:  # Green is to the right of red
        for c in range(red_loc[1] + 1, green_loc[1]): # Start one to the right
            output_grid[red_loc[0], c] = 8
        last_horizontal_x = green_loc[1] - 1
    elif red_loc[1] > green_loc[1]:  # Green is to the left of red
        for c in range(green_loc[1] + 1, red_loc[1]): #stop one before
            output_grid[red_loc[0], c] = 8
        last_horizontal_x = green_loc[1] + 1
    else:
      last_horizontal_x = red_loc[1]

    # 3. Vertical Segment
    if red_loc[0] != green_loc[0]:#only draw vertical if not on same line
        if red_loc[1] == green_loc[1]: #red and green are vertically aligned
            if red_loc[0] < green_loc[0]:
                for r in range(red_loc[0] + 1, green_loc[0] + 1):
                    output_grid[r,last_horizontal_x] = 8
            else:
                for r in range(green_loc[0], red_loc[0]):
                    output_grid[r,last_horizontal_x] = 8

        elif red_loc[0] < green_loc[0]: #green is below red
            for r in range(red_loc[0] + 1, green_loc[0] + 1): #start one below, stop at green
                output_grid[r, last_horizontal_x] = 8
        else: #green is above red
            for r in range(green_loc[0], red_loc[0]): #stop at green
                output_grid[r, last_horizontal_x] = 8


    return output_grid