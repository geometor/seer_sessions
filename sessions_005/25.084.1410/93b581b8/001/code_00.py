"""
Identifies a 2x2 non-background object within the input grid.
Copies the input grid to the output grid.
Determines the four colors within the identified 2x2 object.
Adds four new 2x2 solid-colored objects to the corners of the output grid.
The color of each corner object is determined by the color of the diagonally opposite pixel within the original 2x2 object.
- Top-left corner gets the color of the original object's bottom-right pixel.
- Top-right corner gets the color of the original object's bottom-left pixel.
- Bottom-left corner gets the color of the original object's top-right pixel.
- Bottom-right corner gets the color of the original object's top-left pixel.
"""

import numpy as np

def find_2x2_object(grid):
    """
    Finds the top-left corner coordinates (r, c) of the first 2x2 block
    where all cells are non-zero (non-white).
    Assumes exactly one such block exists.
    """
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if all four cells in the 2x2 block are non-zero
            if (grid[r, c] != 0 and
                grid[r, c+1] != 0 and
                grid[r+1, c] != 0 and
                grid[r+1, c+1] != 0):
                return r, c
    return None # Should not happen based on task description

def draw_2x2_square(grid, r, c, color):
    """
    Fills a 2x2 area in the grid starting at (r, c) with the specified color.
    Modifies the grid in place.
    """
    grid[r:r+2, c:c+2] = color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    height, width = output_grid.shape

    # Locate the 2x2 block of non-white pixels in the input grid
    obj_r, obj_c = find_2x2_object(input_np)
    
    # Identify the colors of the four pixels within this 2x2 block
    color_tl = input_np[obj_r, obj_c]
    color_tr = input_np[obj_r, obj_c+1]
    color_bl = input_np[obj_r+1, obj_c]
    color_br = input_np[obj_r+1, obj_c+1]

    # Fill the corner 2x2 areas in the output grid based on diagonal opposition
    
    # Top-left corner (0, 0) uses BottomRight color
    draw_2x2_square(output_grid, 0, 0, color_br)
    
    # Top-right corner (0, width-2) uses BottomLeft color
    draw_2x2_square(output_grid, 0, width-2, color_bl)
    
    # Bottom-left corner (height-2, 0) uses TopRight color
    draw_2x2_square(output_grid, height-2, 0, color_tr)
    
    # Bottom-right corner (height-2, width-2) uses TopLeft color
    draw_2x2_square(output_grid, height-2, width-2, color_tl)

    # Return the modified grid (as a list of lists if needed, or numpy array)
    # Assuming the environment expects list of lists:
    # return output_grid.tolist() 
    # Returning numpy array as it's often more convenient for further processing
    return output_grid