import numpy as np

"""
Transformation Rule:
1. Locate the red pixel (2) and the green pixel (3) in the input grid.
2. Draw an L-shaped path of azure pixels (8) connecting the row of the red pixel and the column of the green pixel.
3. The path consists of:
    a. A vertical segment in the green pixel's column, extending between (but not including) the rows of the red and green pixels.
    b. A horizontal segment in the red pixel's row, extending between (but not including) the columns of the red and green pixels.
    c. A single azure pixel at the intersection of the red pixel's row and the green pixel's column.
4. The original red and green pixels remain unchanged.
"""

def find_pixel_coords(grid, color):
    """Finds the coordinates (row, col) of the first pixel with the given color."""
    coords = np.argwhere(grid == color)
    if coords.size > 0:
        return tuple(coords[0])
    return None

def transform(input_grid):
    """
    Draws an L-shaped azure path connecting the row of the red pixel
    and the column of the green pixel.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # 1. Locate the coordinates of the red pixel (2)
    red_coords = find_pixel_coords(output_grid, 2)
    if red_coords is None:
        # Handle error or return input if red pixel not found (though problem description implies it exists)
        return output_grid 
    red_row, red_col = red_coords

    # 2. Locate the coordinates of the green pixel (3)
    green_coords = find_pixel_coords(output_grid, 3)
    if green_coords is None:
         # Handle error or return input if green pixel not found (though problem description implies it exists)
        return output_grid
    green_row, green_col = green_coords

    # 3. Draw the L-shaped path with azure pixels (8)

    # a. Draw the vertical segment
    # Determine the row range, excluding the start and end rows themselves
    start_row = min(red_row, green_row) + 1
    end_row = max(red_row, green_row) 
    for r in range(start_row, end_row):
        # Check if the pixel is not the original red or green pixel before drawing
        if output_grid[r, green_col] == 0: 
             output_grid[r, green_col] = 8

    # b. Draw the horizontal segment
    # Determine the column range, excluding the start and end columns themselves
    start_col = min(red_col, green_col) + 1
    end_col = max(red_col, green_col)
    for c in range(start_col, end_col):
         # Check if the pixel is not the original red or green pixel before drawing
         if output_grid[red_row, c] == 0:
            output_grid[red_row, c] = 8

    # c. Draw the corner pixel
    # Check if the corner pixel is not the original red or green pixel before drawing
    # (It could be the green pixel if red_row == green_row, or red pixel if green_col == red_col)
    if output_grid[red_row, green_col] == 0:
        output_grid[red_row, green_col] = 8
        
    return output_grid