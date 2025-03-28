```python
import numpy as np

"""
Transforms a grid by applying a shear transformation to the single non-white 
object. The object is shifted left, with the amount of horizontal shift 
decreasing for rows further down the object, relative to the object's top row.

Rule:
1. Find the single non-white object and its bounding box (min_row, min_col, max_row, max_col).
2. Calculate the horizontal gap before the object (`gap_before` = min_col).
3. Calculate the horizontal gap after the object (`gap_after` = grid_width - 1 - max_col).
4. Determine the maximum horizontal shift applied to the top row of the object: `max_shift = min(gap_before, gap_after * 2)`.
5. For each object pixel at input position (r, c) with color 'color':
    a. Calculate the row offset: `row_offset = r - min_row`.
    b. Calculate the horizontal shift for this row: `h_shift = max(0, max_shift - row_offset)`.
    c. Calculate the new column: `new_c = c - h_shift`.
    d. The new row is `new_r = r`.
    e. Place the `color` at `(new_r, new_c)` in the output grid.
"""

def find_object_pixels_and_bbox(grid):
    """
    Identifies all non-background (non-zero) pixels and their bounding box.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: A tuple containing:
            - list: A list of tuples (row, column, color) for non-background pixels.
            - dict: Bounding box {'min_row', 'min_col', 'max_row', 'max_col'}, 
                    or None if no object found.
            Returns ([], None) if no object is found.
    """
    object_pixels = []
    min_row, min_col = float('inf'), float('inf')
    max_row, max_col = float('-inf'), float('-inf')
    has_object = False
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0: # Assuming 0 is the background color (white)
                object_pixels.append((r, c, color))
                min_row = min(min_row, r)
                min_col = min(min_col, c)
                max_row = max(max_row, r)
                max_col = max(max_col, c)
                has_object = True

    if not has_object:
        return [], None
        
    bbox = {
        'min_row': min_row,
        'min_col': min_col,
        'max_row': max_row,
        'max_col': max_col
    }
    return object_pixels, bbox

def transform(input_grid):
    """
    Applies the shear transformation to the input grid.

    Args:
        input_grid (list or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize the output grid with the background color (white, 0).
    output_grid = np.zeros_like(input_grid_np)

    # 1. Find the single non-white object and its bounding box.
    object_pixels, bbox = find_object_pixels_and_bbox(input_grid_np)

    # If no object is found, return the empty grid
    if not bbox:
        return output_grid

    # Extract bounding box properties
    min_row = bbox['min_row']
    min_col = bbox['min_col']
    max_col = bbox['max_col']
    
    # 2. Calculate the horizontal gap before the object.
    gap_before = min_col

    # 3. Calculate the horizontal gap after the object.
    gap_after = width - 1 - max_col
    
    # 4. Determine the maximum horizontal shift amount for the top row.
    max_shift = min(gap_before, gap_after * 2)

    # 5. Iterate through each object pixel and apply the shear transformation.
    for r, c, color in object_pixels:
        # 5a. Calculate the row offset from the top of the object.
        row_offset = r - min_row
        
        # 5b. Calculate the horizontal shift for this specific pixel's row.
        # Ensure shift is non-negative.
        h_shift = max(0, max_shift - row_offset)
        
        # 5c. Calculate the pixel's new column in the output grid.
        new_c = c - h_shift
        
        # 5d. The pixel's row remains unchanged.
        new_r = r
        
        # 5e. Place the color at the new coordinates in the output grid, 
        # ensuring it's within bounds.
        if 0 <= new_r < height and 0 <= new_c < width:
            output_grid[new_r, new_c] = color

    # Return the completed output grid.
    return output_grid
```