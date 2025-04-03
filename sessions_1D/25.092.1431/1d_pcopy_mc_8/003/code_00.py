import numpy as np

"""
Transforms the input grid based on identified object lengths.
The input grid is expected to be a single row (either as a list of lists with one inner list, or a flat list).
Objects are contiguous horizontal segments of non-white pixels (value > 0).
Objects of length 3 are copied directly to the output grid at the same position.
Objects of length 1 (single pixels) are expanded into a segment of length 3 
using the same color, starting one position to the left of the original pixel's position.
The output grid is initialized with the background color (white, 0) and has the same dimensions as the input.
Pixel placements respect grid boundaries.
"""

def find_objects_1d(grid_row):
    """
    Finds contiguous non-zero objects in a 1D array (list or numpy array).
    Handles different colors defining separate objects even if adjacent.
    Returns a list of dictionaries, each containing 'color', 'start' index, and 'length'.
    """
    objects = []
    in_object = False
    start_index = -1
    current_color = -1
    
    # Convert to list if it's a numpy array, and add a dummy zero for boundary handling
    grid_row_list = list(grid_row) + [0] 
    
    for i, pixel in enumerate(grid_row_list):
        is_non_zero = pixel != 0
        
        if is_non_zero and not in_object:
            # Start of a new object
            in_object = True
            start_index = i
            current_color = pixel
        elif (not is_non_zero or (is_non_zero and pixel != current_color)) and in_object:
            # End of the current object (found zero OR different non-zero color)
            length = i - start_index
            objects.append({'color': current_color, 'start': start_index, 'length': length})
            in_object = False
            # Check if the current pixel starts a *new* object
            if is_non_zero:
                in_object = True
                start_index = i
                current_color = pixel
        # Cases implicitly handled:
        # - pixel != 0 and in_object and pixel == current_color -> continue current object
        # - pixel == 0 and not in_object -> continue background

    return objects

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    
    Args:
        input_grid (list or list[list] or np.ndarray): A grid representing a single row. 
                                                      Can be list[int], list[list[int]] 
                                                      (with one inner list), or a 1D/2D numpy array.

    Returns:
        list[list[int]]: The transformed grid as a list containing a single list (row).
                         Returns [[ ]] if the input represents an empty row.
    """
    
    # --- Input Validation and Conversion to 1D NumPy Array ---
    original_format_was_2d = False # Flag to return output in list[list] format
    input_flat_np = None

    if isinstance(input_grid, np.ndarray):
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
            input_flat_np = input_grid.flatten()
            original_format_was_2d = True
        elif input_grid.ndim == 1:
            input_flat_np = input_grid
        else:
             raise ValueError(f"Input numpy array must be 1D or have shape (1, N). Got shape {input_grid.shape}")
    elif isinstance(input_grid, list):
        if not input_grid: # Handles empty list []
             input_flat_np = np.array([], dtype=int)
        elif isinstance(input_grid[0], list): # list[list[int]]
             if len(input_grid) == 1:
                 input_flat_np = np.array(input_grid[0], dtype=int)
                 original_format_was_2d = True
             elif len(input_grid) == 0: # Handles [[]] case
                 input_flat_np = np.array([], dtype=int)
                 original_format_was_2d = True
             else:
                 raise ValueError("Input grid as list of lists must contain exactly one inner list (row).")
        elif isinstance(input_grid[0], (int, np.integer)): # list[int]
             input_flat_np = np.array(input_grid, dtype=int)
        elif len(input_grid[0]) == 0 and len(input_grid) == 1 : # Handles [[]] case if not caught above
            input_flat_np = np.array([], dtype=int)
            original_format_was_2d = True
        else:
             # Check for empty list case again, e.g., input was []
             is_empty_list_of_empty = all(isinstance(sublist, list) and not sublist for sublist in input_grid)
             if is_empty_list_of_empty and len(input_grid) == 1: # Handles [[]]
                 input_flat_np = np.array([], dtype=int)
                 original_format_was_2d = True
             elif not input_grid: # Handles []
                 input_flat_np = np.array([], dtype=int)
             else:
                raise ValueError(f"Input list elements must be integers or a single list of integers. Got type: {type(input_grid[0])}")
    else:
         raise TypeError(f"Input grid must be a list or numpy array. Got type: {type(input_grid)}")

    # Handle case of empty input row after processing
    if input_flat_np.size == 0:
        return [[]] # Return format consistent with a single empty row

    grid_width = input_flat_np.shape[0]

    # --- Initialize Output Grid ---
    # Create a 1D numpy array initialized with zeros (background color)
    output_grid_np = np.zeros(grid_width, dtype=int)

    # --- Find Objects in Input ---
    objects = find_objects_1d(input_flat_np) 

    # --- Apply Transformation Rules ---
    for obj in objects:
        color = obj['color']
        start = obj['start']
        length = obj['length']

        if length == 3:
            # Copy object of length 3 directly
            # Calculate end index (exclusive)
            end = start + length 
            # Check bounds rigorously: start must be valid, end must not exceed width
            if 0 <= start < grid_width and end <= grid_width:
                 output_grid_np[start:end] = color
                 
        elif length == 1:
            # Expand object of length 1 to length 3, starting at start - 1
            new_start = start - 1
            # Write the 3 pixels individually, checking bounds for each index
            for i in range(3): 
                idx = new_start + i
                # Check if the target index is within the grid bounds [0, grid_width - 1]
                if 0 <= idx < grid_width:
                    output_grid_np[idx] = color
        # Ignore objects of other lengths if any were found (though examples suggest only 1 and 3 exist)


    # --- Format Output ---
    # Convert the final 1D numpy array back into a list of lists [[...]]
    # This matches the ARC task format expectation.
    return output_grid_np.reshape(1, -1).tolist()
