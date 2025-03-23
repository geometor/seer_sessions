"""
1. **Identify Object:** Locate the single rectangular object within the input grid. This is defined as a contiguous block of non-zero pixels.
2. **Determine Dimensions:** Calculate the width and height of the identified object.
3. **Rotate:** Rotate the object 90 degrees clockwise.  This swaps the object's width and height.
4. **Create Output Grid:** Create an output grid with the same dimensions as the input grid, filled with zeros (representing the white background).
5. **Center and Place:** Calculate the center coordinates of the *output grid*.  Place the *rotated* object onto the output grid such that the center of the rotated object coincides with the center of the output grid. The rotated object's pixels should overwrite any background pixels. If rotated object exceed grid boundaries after centering, crop it.
"""

import numpy as np

def find_object(grid):
    # Find coordinates of non-zero pixels
    rows, cols = np.nonzero(grid)
    if len(rows) == 0:  # Handle empty object case
        return None, None, None, None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return min_row, max_row, min_col, max_col

def rotate_object(grid, min_row, max_row, min_col, max_col):
    # Extract the object
    object_block = grid[min_row:max_row+1, min_col:max_col+1]
    # Rotate 90 degrees clockwise using numpy
    rotated_block = np.rot90(object_block, k=-1)
    return rotated_block

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)

    # 1. & 2. Identify Object and Determine Dimensions
    min_row, max_row, min_col, max_col = find_object(input_grid)

    if min_row is None:  # Handle case where no object is found
        return output_grid.tolist()

    # 3. Rotate
    rotated_block = rotate_object(input_grid, min_row, max_row, min_col, max_col)
    rotated_height, rotated_width = rotated_block.shape

    # 4. Create Output Grid (already done)

    # 5. Center and Place
    grid_height, grid_width = output_grid.shape
    center_row = grid_height // 2
    center_col = grid_width // 2

    # Calculate top-left corner for centered placement
    start_row = center_row - rotated_height // 2
    start_col = center_col - rotated_width // 2

    # Ensure the rotated object stays within bounds
    start_row = max(0, start_row)
    start_col = max(0, start_col)
    end_row = min(grid_height, start_row + rotated_height)
    end_col = min(grid_width, start_col + rotated_width)
    
    #Adjust the section taken from the rotated_object as well in case of cropping
    crop_start_row = 0
    crop_start_col = 0

    if start_row == 0 and rotated_height > grid_height:
        crop_start_row = rotated_height - (end_row-start_row)
    
    if start_col == 0 and rotated_width > grid_width:
        crop_start_col = rotated_width - (end_col - start_col)
        
    output_grid[start_row:end_row, start_col:end_col] = rotated_block[crop_start_row:, crop_start_col:]

    return output_grid.tolist()