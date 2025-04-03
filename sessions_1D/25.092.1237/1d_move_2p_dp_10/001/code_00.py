import numpy as np

"""
Reposition a contiguous block of a non-white, non-maroon color (the 'object') 
within a 1D array. The object's rightmost pixel is moved to be immediately 
to the left of a single maroon (9) pixel (the 'target_marker'). The object's 
color and length are preserved. The target_marker's position is preserved. 
All other positions in the array are filled with the background color (white, 0).
"""

def find_contiguous_object(arr):
    """Finds the first contiguous block of non-zero, non-9 color."""
    start_index = -1
    obj_color = -1
    for i, pixel in enumerate(arr):
        # Start of a potential object
        if pixel != 0 and pixel != 9 and start_index == -1:
            start_index = i
            obj_color = pixel
        # End of the object (different color or background/target)
        elif start_index != -1 and (pixel == 0 or pixel == 9 or pixel != obj_color):
            end_index = i - 1
            length = end_index - start_index + 1
            return start_index, end_index, obj_color, length
        # Case where object goes to the end of the array
        elif start_index != -1 and i == len(arr) - 1 and pixel == obj_color:
            end_index = i
            length = end_index - start_index + 1
            return start_index, end_index, obj_color, length
    # If no object found or object doesn't end properly (shouldn't happen based on examples)
    return -1, -1, -1, 0

def find_target_marker(arr, target_color=9):
    """Finds the index of the target marker color."""
    for i, pixel in enumerate(arr):
        if pixel == target_color:
            return i
    return -1 # Target marker not found

def transform(input_grid):
    """
    Applies the transformation rule to the input 1D array.
    """
    # Ensure input is treated as a 1D list or array
    input_arr = np.array(input_grid).flatten().tolist()
    arr_len = len(input_arr)
    
    # Initialize output grid with background color (0)
    output_arr = [0] * arr_len

    # Find the contiguous object (non-white, non-maroon)
    obj_start, obj_end, obj_color, obj_length = find_contiguous_object(input_arr)
    
    # Find the target marker (maroon, 9)
    target_index = find_target_marker(input_arr, 9)

    # Check if both object and target were found
    if obj_length > 0 and target_index != -1:
        # Place the target marker in the output array
        output_arr[target_index] = 9

        # Calculate the new position for the object
        # New end index is right before the target marker
        new_obj_end_index = target_index - 1
        # New start index is calculated based on the length
        new_obj_start_index = new_obj_end_index - obj_length + 1

        # Place the object in the output array at its new position
        # Ensure indices are valid before writing
        if new_obj_start_index >= 0 and new_obj_end_index < arr_len:
            for i in range(new_obj_start_index, new_obj_end_index + 1):
                output_arr[i] = obj_color
        else:
            # Handle cases where the object might go out of bounds (though not expected from examples)
            # For now, we'll assume it fits based on the problem constraints.
            # If it doesn't fit, the current implementation leaves those parts as background.
             for i in range(max(0, new_obj_start_index), min(arr_len, new_obj_end_index + 1)):
                 output_arr[i] = obj_color


    # If object or target not found (shouldn't happen based on examples), 
    # return the initialized background grid or handle error appropriately.
    # For now, it returns the grid potentially partially filled if one component was found.

    # The task description implies input/output are grids, even if 1D.
    # Return as a list of lists (1 row) to maintain grid structure if needed later.
    # However, since examples are flat lists, returning a flat list is more direct.
    # Let's return the flat list based on example format.
    return output_arr 