import numpy as np
import math # Retained import, although floor division // is used instead of math.floor

"""
Transforms the input grid by translating the single non-white object 
horizontally to the left. The amount of shift depends on the horizontal gaps 
to the left and right of the object's bounding box and the object's width. 
The vertical position remains unchanged.

Rule:
1. Find the single non-white object and its bounding box.
2. Calculate the horizontal gap before the object (`gap_before` = distance from left edge to object's left edge).
3. Calculate the horizontal gap after the object (`gap_after` = distance from object's right edge to right edge).
4. Calculate the object's width (`obj_width`).
5. Determine the horizontal shift amount (`shift_left_amount`):
    - If `gap_before <= gap_after`: `shift_left_amount = gap_before`.
    - If `gap_before > gap_after`:
        - If `gap_before <= obj_width`: `shift_left_amount = gap_before`.
        - Else (`gap_before > obj_width`): `shift_left_amount = (gap_before + 1) // 2`.
6. Create an output grid and place the object pixels shifted left by `shift_left_amount`.
"""

def find_object_pixels(grid):
    """
    Identifies all non-background (non-zero) pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains (row, column, color) 
              for a non-background pixel. Returns an empty list if no object is found.
    """
    object_pixels = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0: # Assuming 0 is the background color (white)
                object_pixels.append((r, c, color))
    return object_pixels

def calculate_bounding_box(object_pixels):
    """
    Calculates the minimum and maximum row and column indices 
    of the bounding box containing the object pixels.

    Args:
        object_pixels (list): A list of (row, column, color) tuples.

    Returns:
        dict: A dictionary containing 'min_row', 'min_col', 'max_row', 'max_col', 
              or None if object_pixels is empty.
    """
    if not object_pixels:
        return None
    
    rows = [r for r, c, color in object_pixels]
    cols = [c for r, c, color in object_pixels]
    
    return {
        'min_row': min(rows),
        'min_col': min(cols),
        'max_row': max(rows),
        'max_col': max(cols)
    }

def transform(input_grid):
    """
    Applies the horizontal shift transformation to the input grid.

    Args:
        input_grid (list or np.array): The input grid represented as a list of lists or numpy array.

    Returns:
        np.array: The transformed output grid as a numpy array.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize the output grid with the background color (white, 0).
    output_grid = np.zeros_like(input_grid_np)

    # Identify all non-white pixels forming the object.
    object_pixels = find_object_pixels(input_grid_np)

    # If no object is found, return the empty grid
    if not object_pixels:
        return output_grid

    # Determine the bounding box of the object.
    bbox = calculate_bounding_box(object_pixels)
    min_col = bbox['min_col']
    max_col = bbox['max_col']
    
    # Calculate the horizontal gap before the object.
    gap_before = min_col

    # Calculate the horizontal gap after the object.
    gap_after = width - 1 - max_col
    
    # Calculate the object's width.
    obj_width = max_col - min_col + 1

    # Determine the horizontal shift amount (shift_left_amount) based on the derived rule.
    shift_left_amount = 0
    if gap_before <= gap_after:
        # If gap before is less than or equal to gap after, shift left by gap_before.
        shift_left_amount = gap_before 
    else: # gap_before > gap_after
        # If gap before is greater than gap after, check against object width.
        if gap_before <= obj_width:
            # If gap before is also less than or equal to object width, shift left by gap_before.
             shift_left_amount = gap_before
        else: # gap_before > obj_width
            # If gap before is greater than object width, shift left by floor((gap_before + 1) / 2).
            shift_left_amount = (gap_before + 1) // 2 # Integer division provides floor

    # Apply the shift to each object pixel and place it in the output grid.
    for r, c, color in object_pixels:
        # Calculate its new column index by shifting left.
        new_c = c - shift_left_amount
        # The row index remains unchanged.
        new_r = r
        
        # Ensure the new coordinates are within the grid bounds.
        # This check is important to prevent errors if calculation leads outside bounds.
        if 0 <= new_r < height and 0 <= new_c < width:
             # Set the pixel at the new coordinates in the output grid.
            output_grid[new_r, new_c] = color

    # Return the completed output grid.
    return output_grid