import numpy as np

"""
Shift a contiguous block of non-white pixels two positions to the right within a row.

1. Identify the contiguous sequence of non-white pixels (the "object") in the 
   input row. Note its color, length, and starting index.
2. Create a new output row of the same length as the input row, initially 
   filled entirely with white (0) pixels.
3. Calculate the new starting index for the object by adding 2 to its 
   original starting index.
4. Place the identified object (using its original color and length) into the 
   output row starting at the calculated new index.
"""

def find_object(grid_row):
    """
    Finds the start index, end index (exclusive), color, and length 
    of the first contiguous block of non-white pixels in a 1D array.
    Returns None if no non-white block is found.
    """
    start_index = -1
    object_color = 0
    length = 0
    width = len(grid_row)

    for i, pixel in enumerate(grid_row):
        if pixel != 0: # Found the start of the object
            start_index = i
            object_color = pixel
            break
            
    if start_index == -1: # No non-white pixel found
        return None, None, None, None

    for i in range(start_index, width):
        if grid_row[i] == object_color:
            length += 1
        else: # Found the end of the object
            break
            
    end_index = start_index + length
    return start_index, end_index, object_color, length


def transform(input_grid):
    """
    Shifts a contiguous block of non-white pixels two positions to the right 
    within a single row (1D array).
    """
    # The input is expected to be a 1D array (single row)
    input_row = np.array(input_grid).flatten() 
    row_length = len(input_row)

    # Initialize output_grid as a row of white pixels with the same length
    output_row = np.zeros(row_length, dtype=int)

    # 1. Identify the object
    start_index, end_index, object_color, object_length = find_object(input_row)

    # Check if an object was found
    if start_index is not None:
        # 3. Calculate the new starting index
        new_start_index = start_index + 2
        new_end_index = new_start_index + object_length

        # Ensure the new position is within the bounds of the row
        if new_end_index <= row_length:
             # 4. Place the identified object into the output row at the new position
            output_row[new_start_index:new_end_index] = object_color
        else:
            # Handle cases where the shift goes beyond the grid boundary if necessary
            # In this specific task description, it seems the examples don't cause this,
            # but for robustness, we might clip or handle differently.
            # For now, just place what fits.
            clippable_length = row_length - new_start_index
            if clippable_length > 0:
                 output_row[new_start_index:row_length] = object_color

    # Reshape the output back to the original input grid shape (assuming it was 1xN)
    # This might need adjustment if inputs could be Nx1. However, examples are 1xN.
    output_grid = output_row.reshape(1, -1) # Reshape to 1 row

    return output_grid.tolist() # Return as list of lists
