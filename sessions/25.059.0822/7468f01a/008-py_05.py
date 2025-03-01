"""
1.  **Identify the bounding box:** Find the smallest rectangle within the input grid that encompasses all non-zero (non-white) pixels. This is defined by the outermost '4' (yellow) pixels.
2.  **Crop:** Extract the region of the input grid defined by the bounding box in step 1.
3. **Output the bounding box** The cropped region is the output grid.
"""

import numpy as np

def find_bounding_box(grid):
    # Find row and column indices of all non-zero elements
    rows, cols = np.nonzero(grid)
    
    # If there are no non-zero elements, return None or handle the case appropriately
    if len(rows) == 0:
        return None  # Or whatever is appropriate for an empty bounding box
    
    # Calculate min and max row/col to define the bounding box
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # Find the bounding box of non-zero pixels
    bounding_box = find_bounding_box(input_grid)
    
    # Handle cases where there are no non-zero elements
    if bounding_box is None:
        return np.array([])  # Return empty grid or whatever is appropriate
    
    min_row, max_row, min_col, max_col = bounding_box

    # Crop the input grid to the bounding box
    output_grid = input_grid[min_row:max_row+1, min_col:max_col+1]

    return output_grid