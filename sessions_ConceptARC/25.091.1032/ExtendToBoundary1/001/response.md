```python
import numpy as np
import math

"""
Transforms the input grid by finding the single non-white rectangular object and extending a line from its middle row or column to the edge of the grid.

The extension is horizontal (to the right edge) if the object's height is less than or equal to its width.
The extension is vertical (to the bottom edge) if the object's height is greater than its width.

The line extended corresponds to the middle row or column of the object. If there are two middle rows/columns (even dimension), the one with the lower index (topmost row or leftmost column) is chosen.
"""

def find_object_properties(grid):
    """
    Finds the single non-white object in the grid and returns its color and bounding box.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (object_color, min_row, max_row, min_col, max_col) or (None, -1, -1, -1, -1) if no object found.
    """
    non_white_pixels = np.argwhere(grid != 0)
    if non_white_pixels.size == 0:
        return None, -1, -1, -1, -1  # No object found

    # Assuming only one object and one non-white color
    object_color = grid[non_white_pixels[0][0], non_white_pixels[0][1]]
    
    min_row = np.min(non_white_pixels[:, 0])
    max_row = np.max(non_white_pixels[:, 0])
    min_col = np.min(non_white_pixels[:, 1])
    max_col = np.max(non_white_pixels[:, 1])
    
    return object_color, min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    1. Finds the non-white object.
    2. Determines its dimensions (height H, width W).
    3. If H > W, extends the middle column vertically downwards.
    4. If H <= W, extends the middle row horizontally rightwards.
    
    Args:
        input_grid (list[list[int]]): The input grid.
        
    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    grid_h, grid_w = output_grid.shape

    # 1. Identify the single contiguous block of non-white pixels (the object).
    object_color, min_row, max_row, min_col, max_col = find_object_properties(input_np)

    # If no object is found, return the original grid
    if object_color is None:
        return input_grid 

    # 3. Calculate the object's height
    H = max_row - min_row + 1
    # 4. Calculate the object's width
    W = max_col - min_col + 1

    # 5. Compare the height and width.
    if H > W:
        # 6. Extend vertically if height is greater than width.
        # a. Calculate the index of the middle column
        # Use integer division // which is equivalent to floor() for positive numbers
        extend_col = min_col + (W - 1) // 2 
        
        # b. Iterate through rows from below the object to the grid bottom
        for r in range(max_row + 1, grid_h):
            # c. Set the pixel color
            output_grid[r, extend_col] = object_color
            
    else: # H <= W
        # 7. Extend horizontally if height is less than or equal to width.
        # a. Calculate the index of the middle row
        extend_row = min_row + (H - 1) // 2 
        
        # b. Iterate through columns from right of the object to the grid edge
        for c in range(max_col + 1, grid_w):
             # c. Set the pixel color
            output_grid[extend_row, c] = object_color

    # 8. Return the modified output grid (converted back to list of lists)
    return output_grid.tolist()
```