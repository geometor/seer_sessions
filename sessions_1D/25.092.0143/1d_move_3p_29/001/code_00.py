import numpy as np

"""
Identifies a contiguous block of non-white pixels in a 1x10 input grid 
and shifts this block 3 positions to the right in the output grid, 
filling the original position with white pixels.
"""

def find_colored_block(row):
    """
    Finds the first contiguous block of non-white pixels in a row.

    Args:
        row: A list or numpy array representing a single row of the grid.

    Returns:
        A tuple (color, start_index, length) if a block is found,
        otherwise (None, -1, 0).
    """
    start_index = -1
    length = 0
    color = None
    for i, pixel in enumerate(row):
        if pixel != 0:  # Found the start of a block
            color = pixel
            start_index = i
            length = 1
            # Find the end of the block
            for j in range(i + 1, len(row)):
                if row[j] == color:
                    length += 1
                else:
                    break
            break # Found the first block, stop searching
    return color, start_index, length

def transform(input_grid):
    """
    Shifts the contiguous non-white block in a 1x10 grid 3 positions to the right.

    Args:
        input_grid: A numpy array or list of lists representing the 1x10 input grid.

    Returns:
        A numpy array representing the 1x10 output grid with the block shifted.
    """
    # Ensure input is a NumPy array for easier handling
    input_array = np.array(input_grid)

    # Get the single row from the input grid
    # Assuming input is always 1xN
    input_row = input_array[0]
    grid_width = len(input_row)

    # Initialize the output grid with the background color (white, 0)
    # Keep the same dimensions as input
    output_grid = np.zeros_like(input_array)
    output_row = output_grid[0] # Get a reference to the row to modify

    # Find the non-white block in the input row
    color, start_index, length = find_colored_block(input_row)

    # If a block is found, calculate its new position and place it
    if color is not None:
        # Calculate the new starting index
        new_start_index = start_index + 3

        # Ensure the new position is within bounds (although examples suggest it always fits)
        if new_start_index >= 0 and new_start_index + length <= grid_width:
            # Place the block in the output row
            output_row[new_start_index : new_start_index + length] = color
        else:
            # Handle cases where the shift goes out of bounds if necessary
            # Based on examples, this might not be needed, but good practice
            # For now, just place what fits or do nothing if start is out of bounds
            if new_start_index < grid_width:
                 actual_length = min(length, grid_width - new_start_index)
                 if actual_length > 0:
                    output_row[new_start_index : new_start_index + actual_length] = color


    # Return the output grid (as numpy array, can be converted back to list of lists if required)
    return output_grid.tolist() # Convert back to list of lists as per ARC standard
