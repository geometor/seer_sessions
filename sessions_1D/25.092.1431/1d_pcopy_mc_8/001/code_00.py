import numpy as np

"""
Transforms the input grid based on identified object lengths.
Objects are contiguous horizontal segments of non-white pixels (value > 0).
Objects of length 3 are copied directly to the output grid at the same position.
Objects of length 1 (single pixels) are expanded into a segment of length 3 
using the same color, starting one position to the left of the original pixel's position.
The output grid is initialized with the background color (white, 0).
"""

def find_objects_1d(grid_row):
    """
    Finds contiguous non-zero objects in a 1D array (list or numpy array).
    Returns a list of dictionaries, each containing 'color', 'start' index, and 'length'.
    """
    objects = []
    in_object = False
    start_index = -1
    current_color = -1
    
    # Add a dummy zero at the end to handle objects ending at the grid boundary easily
    grid_row_padded = list(grid_row) + [0] 
    
    for i, pixel in enumerate(grid_row_padded):
        is_non_zero = pixel != 0
        
        if is_non_zero and not in_object:
            # Start of a new object
            in_object = True
            start_index = i
            current_color = pixel
        elif (not is_non_zero or (is_non_zero and pixel != current_color)) and in_object:
            # End of the current object (found zero or different color)
            length = i - start_index
            objects.append({'color': current_color, 'start': start_index, 'length': length})
            in_object = False
            start_index = -1
            current_color = -1
            # If the current pixel is non-zero, it's the start of a new object
            if is_non_zero:
                in_object = True
                start_index = i
                current_color = pixel
        # Case: pixel != 0 and in_object and pixel == current_color -> continue object
        # Case: pixel == 0 and not in_object -> continue background

    return objects

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    
    Args:
        input_grid (list or list of lists): A 1D grid represented as a list 
                                           or a single-row 2D list.

    Returns:
        list or list of lists: The transformed grid in the same format as the input.
    """
    
    # Handle both flat list and list of lists input
    is_list_of_lists = isinstance(input_grid[0], list)
    if is_list_of_lists:
        if len(input_grid) != 1:
             raise ValueError("Input grid must be 1D or a single row 2D array.")
        input_flat = input_grid[0]
    else:
        input_flat = input_grid
        
    input_np = np.array(input_flat, dtype=int)
    grid_width = input_np.shape[0]

    # Initialize output_grid with background color (0)
    output_grid = np.zeros_like(input_np)

    # Find objects in the input grid
    # Use the flat representation for finding objects
    objects = find_objects_1d(input_np) 

    # Apply transformation rules based on objects
    for obj in objects:
        color = obj['color']
        start = obj['start']
        length = obj['length']

        if length == 3:
            # Copy object of length 3 directly
            end = start + length
            # Ensure write operation is within bounds
            if start < grid_width and end <= grid_width:
                 output_grid[start:end] = color
                 
        elif length == 1:
            # Expand object of length 1 to length 3, starting at start - 1
            new_start = start - 1
            # Write the 3 pixels individually, checking bounds for each
            for i in range(3): 
                idx = new_start + i
                # Check if the target index is within the grid bounds
                if 0 <= idx < grid_width:
                    output_grid[idx] = color

    # Return the grid in the original format
    if is_list_of_lists:
        return output_grid.reshape(1, -1).tolist()
    else:
        return output_grid.tolist()
