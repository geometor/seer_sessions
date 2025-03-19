# 47c1f68c • 020 • refine_coder

---
```python
"""
1.  **Identify the bounding box:** Find the smallest rectangle within the input grid that contains all non-background pixels.
2.  **Examine the shape formed.** Determine if it's an L or a cross.
3.  **If L-shape, rotate:** If the shape is an L, Rotate the L-shape 90 degrees Clockwise, placing it inside a bounding box of the same size as the original and in the same relative position within the overall input grid.
4. If cross-shape, reflect. If it's a plus, perform a reflection (or 180 degree rotation). The position of the shape's bounding box relative to the input grid is consistent with the output grid.
5. **Create Output:** Create the output with the same size as the input grid
6. **Render:** Render the object into the output grid
"""

import numpy as np

def get_bounding_box(grid):
    """Finds the bounding box of non-background pixels."""
    grid = np.array(grid)
    non_background_indices = np.argwhere(grid != 0)
    if len(non_background_indices) == 0:
        return None  # Handle empty input

    min_row = np.min(non_background_indices[:, 0])
    max_row = np.max(non_background_indices[:, 0])
    min_col = np.min(non_background_indices[:, 1])
    max_col = np.max(non_background_indices[:, 1])

    return (min_row, max_row, min_col, max_col)

def rotate_L_shape(input_grid, bounding_box):
    """Rotates an L-shape 90 degrees clockwise within its bounding box."""
    min_row, max_row, min_col, max_col = bounding_box
    input_cropped = np.array(input_grid)[min_row:max_row+1, min_col:max_col+1]

    # Rotate the cropped grid 90 degrees clockwise
    rotated_cropped = np.rot90(input_cropped, k=-1)
    return rotated_cropped.tolist()
    

def reflect_cross_shape(input_grid, bounding_box):
    """Reflects a cross-shape (assumed to be a 2x2 block) within its bounding box."""
    min_row, max_row, min_col, max_col = bounding_box
    input_cropped = np.array(input_grid)[min_row:max_row+1, min_col:max_col+1]
    
    reflected_cropped = np.fliplr(input_cropped) # reflect across the vertical
    return reflected_cropped.tolist()

def is_L_shape(input_grid, bounding_box):
   
    min_row, max_row, min_col, max_col = bounding_box
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    if height == 3 and width == 3:
        return True
    
    return False
    
def is_cross_shape(input_grid, bounding_box):
    min_row, max_row, min_col, max_col = bounding_box
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    if height == 2 and width == 2:
       return True
    return False

def transform(input_grid):
    # 1. Identify the bounding box
    bounding_box = get_bounding_box(input_grid)
    if bounding_box is None:
        return np.zeros_like(input_grid).tolist()  # Handle empty input

    # 2. Examine the shape formed
    if is_L_shape(input_grid, bounding_box):
        # 3. If L-shape, rotate
        transformed_object = rotate_L_shape(input_grid, bounding_box)
    elif is_cross_shape(input_grid, bounding_box):
      # 4. If cross, reflect/rotate 180
        transformed_object = reflect_cross_shape(input_grid, bounding_box)
    else:
        return np.array(input_grid).tolist() # default is do nothing
    
    # 5. Create Output: Same size as input
    output_grid = np.zeros_like(input_grid)
    
    # 6. Render: Place the transformed object into the output grid,
    # maintaining relative position.
    min_row, max_row, min_col, max_col = bounding_box
    row_offset = min_row
    col_offset = min_col
    
    for i in range(len(transformed_object)):
        for j in range(len(transformed_object[0])):
            output_grid[row_offset + i, col_offset + j] = transformed_object[i][j]

    return output_grid.tolist()
```
