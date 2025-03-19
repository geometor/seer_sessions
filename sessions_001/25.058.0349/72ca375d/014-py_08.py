"""
1.  **Identify the Target Object:** Examine the input grid and locate the object that is gray (color value 5).

2.  **Determine Output Dimensions:** The height is determined by the height of the identified object. The length of the first row in output will be the length from first grey pixel to last grey pixel.

3. **Construct simplified Object:** The output grid should have two rows. The first one should have a white (0) cell between grey (5) cells. And, the length of each row corresponds to the max length of the target object.

4.  **Populate Output:** Fill all cells of the output grid with the gray color (value 5), except two white cells (value of 0) between grey cells in first row.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of all pixels with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None  # Object not found
    return coords

def get_object_dimensions(coords):
    # Calculate the height and width of the object's bounding box.
     min_row, min_col = np.min(coords, axis=0)
     max_row, max_col = np.max(coords, axis=0)
     height = max_row - min_row + 1
     width = max_col - min_col + 1

     return height, width, min_col, max_col

def transform(input_grid):
    # Find the gray object (color 5).
    gray_coords = find_object(input_grid, 5)
    
    if gray_coords is None:
        return None  # Handle case where gray object isn't found.

    # Get dimensions and min/max columns of the gray object.
    gray_height, gray_width, min_col, max_col = get_object_dimensions(gray_coords)

    # output height is 2
    output_height = 2
    
    # Determine output width
    output_width = gray_width

    # Initialize the output grid with the determined dimensions, filled with gray.
    output_grid = np.full((output_height, output_width), 5, dtype=int)
    
    # set 0 for white
    output_grid[0, (output_width-1)//2] = 0
    output_grid[0, output_width//2 ] = 0

    return output_grid