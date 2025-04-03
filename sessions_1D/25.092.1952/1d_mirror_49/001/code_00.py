import numpy as np
import copy

"""
Identifies a single maroon (9) pixel which acts as a fixed pivot point.
Identifies a single contiguous block (object) of a non-white, non-maroon color.
Calculates the gap (number of white pixels) between the object and the maroon pivot.
Moves the object to the opposite side of the maroon pivot, maintaining the same gap size.
The output grid has the same dimensions, with the maroon pivot in its original position and the object relocated.
"""

def find_pixel_index(grid_1d, color):
    """Finds the index of the first occurrence of a specific color."""
    for idx, pixel in enumerate(grid_1d):
        if pixel == color:
            return idx
    return -1 # Should not happen based on problem description

def find_object_details(grid_1d, ignore_colors=(0, 9)):
    """Finds the details (color, start_idx, end_idx) of the first contiguous object."""
    start_idx = -1
    object_color = -1
    for idx, pixel in enumerate(grid_1d):
        if pixel not in ignore_colors:
            if start_idx == -1:
                start_idx = idx
                object_color = pixel
            # Continue if the pixel is part of the current object
            elif pixel != object_color:
                # Found the end of the object (previous index)
                 return object_color, start_idx, idx - 1
        elif start_idx != -1:
             # Found the end of the object (previous index) because color changed back
            return object_color, start_idx, idx - 1

    # Handle case where object goes to the end of the grid
    if start_idx != -1:
        return object_color, start_idx, len(grid_1d) - 1
        
    return None, -1, -1 # Should not happen

def transform(input_grid):
    """
    Transforms the input grid by moving the colored object to the opposite side
    of the maroon pivot, preserving the gap size.
    """
    # Ensure input is a 1D list or array
    if isinstance(input_grid, list) and len(input_grid) > 0 and isinstance(input_grid[0], list):
         grid_1d = np.array(input_grid[0], dtype=int)
    elif isinstance(input_grid, list):
         grid_1d = np.array(input_grid, dtype=int) # Handle if input is already 1D list
    else:
         grid_1d = np.array(input_grid, dtype=int) # Assume numpy array or similar

    # Find the maroon pivot pixel's index
    maroon_index = find_pixel_index(grid_1d, 9)
    if maroon_index == -1:
        # Handle error: Maroon pixel not found (though guaranteed by examples)
        return input_grid # Or raise an error

    # Find the object's details
    object_color, object_start_idx, object_end_idx = find_object_details(grid_1d)
    if object_color is None:
        # Handle error: Object not found (though guaranteed by examples)
        return input_grid # Or raise an error

    object_length = object_end_idx - object_start_idx + 1

    # Determine if object is left or right of maroon pixel and calculate gap
    gap_size = 0
    object_on_left = False
    if object_end_idx < maroon_index:
        object_on_left = True
        gap_size = maroon_index - object_end_idx - 1
    else: # object_start_idx > maroon_index
        object_on_left = False
        gap_size = object_start_idx - maroon_index - 1

    # Initialize output_grid with background color (white)
    output_grid_1d = np.zeros_like(grid_1d)

    # Place the maroon pivot in the output
    output_grid_1d[maroon_index] = 9

    # Calculate new position for the object
    new_start_idx = -1
    if object_on_left:
        # Move object to the right
        new_start_idx = maroon_index + gap_size + 1
    else:
        # Move object to the left
        new_end_idx = maroon_index - gap_size - 1
        new_start_idx = new_end_idx - object_length + 1

    # Ensure new position is valid within bounds (optional check, should be ok if logic is correct)
    new_end_idx = new_start_idx + object_length - 1
    if new_start_idx >= 0 and new_end_idx < len(output_grid_1d):
        # Place the object in the output grid
        output_grid_1d[new_start_idx : new_end_idx + 1] = object_color
    else:
        # Handle error: New position is out of bounds (indicates logic error or unexpected input)
        print(f"Warning: Calculated new position [{new_start_idx}, {new_end_idx}] is out of bounds for grid size {len(output_grid_1d)}.")
        # Fallback or raise error depending on desired robustness
        return input_grid


    # Return in the same format as input examples (simple list)
    return output_grid_1d.tolist()