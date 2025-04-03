"""
Identify the single maroon (9) pixel (pivot) and the contiguous block of non-white, non-maroon pixels (object) in the input 1D grid. Move the object from one side of the pivot to the other, maintaining a one-pixel white (0) separation, while keeping the pivot stationary. Fill the original location of the object with white pixels.
"""

import numpy as np

def find_pivot(grid_1d):
    """Finds the index and color of the pivot pixel (maroon, 9)."""
    for i, pixel in enumerate(grid_1d):
        if pixel == 9:
            return i, pixel
    return -1, -1 # Should not happen based on examples

def find_movable_object(grid_1d, pivot_index):
    """Finds the start index, end index, color, and length of the movable object."""
    object_color = -1
    start_index = -1
    end_index = -1
    in_object = False

    for i, pixel in enumerate(grid_1d):
        if pixel != 0 and pixel != 9: # Found a non-background, non-pivot pixel
            if not in_object:
                object_color = pixel
                start_index = i
                in_object = True
            end_index = i # Keep updating end index while in the object
        elif in_object: # Exited the object
            break

    if start_index != -1:
        length = end_index - start_index + 1
        return start_index, end_index, object_color, length
    else:
        return -1, -1, -1, 0 # Object not found

def transform(input_grid):
    """
    Moves a contiguous block of colored pixels from one side of a stationary 
    maroon (9) pixel to the other side, maintaining a one-pixel separation.
    """
    # Assuming input_grid is a list of lists, even for 1D cases (e.g., [[0, 0, 3,...]])
    # Convert to a 1D numpy array for easier processing
    grid_1d = np.array(input_grid[0])
    grid_length = len(grid_1d)

    # Initialize output_grid as a 1D array of zeros (white)
    output_grid_1d = np.zeros(grid_length, dtype=int)

    # 1. Identify the pivot point (maroon pixel)
    pivot_index, pivot_color = find_pivot(grid_1d)
    if pivot_index == -1:
         # Handle error: pivot not found (though examples guarantee it)
         return input_grid # Or raise an error

    # 2. Identify the movable object
    obj_start, obj_end, obj_color, obj_length = find_movable_object(grid_1d, pivot_index)
    if obj_start == -1:
        # Handle error: object not found
        return input_grid # Or raise an error

    # 3. Place the pivot pixel in the output grid
    output_grid_1d[pivot_index] = pivot_color

    # 4. Determine relative position and calculate new position
    if obj_end < pivot_index: # Object is to the left of the pivot
        # 5. Calculate new starting position to the right of the pivot
        new_start_index = pivot_index + 2 # +1 for pivot, +1 for gap
    else: # Object is to the right of the pivot
        # 5. Calculate new starting position to the left of the pivot
        new_start_index = pivot_index - 1 - obj_length # -1 for pivot, -1 for gap start calculation

    # Ensure new position is within bounds (although not strictly needed by examples)
    new_end_index = new_start_index + obj_length - 1
    if 0 <= new_start_index < grid_length and 0 <= new_end_index < grid_length:
         # 6. Place the movable object in the output grid at the new location
         output_grid_1d[new_start_index : new_end_index + 1] = obj_color
    else:
        # Handle case where object goes out of bounds (optional based on task constraints)
        print(f"Warning: Object placement out of bounds: {new_start_index}-{new_end_index}")
        # Decide how to handle: truncate? error? return original?
        # For now, just proceed, potentially causing numpy errors if indexes are invalid

    # Convert back to list of lists format for ARC
    output_grid = [output_grid_1d.tolist()]

    return output_grid