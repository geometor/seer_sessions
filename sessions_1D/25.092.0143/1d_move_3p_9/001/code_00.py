import numpy as np

def find_colored_block(row):
    """
    Finds the first contiguous block of non-white pixels in a row.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A tuple (start_index, end_index, color, length) if a block is found,
        otherwise None. Returns -1 for start/end index if no block found.
    """
    start_index = -1
    end_index = -1
    color = 0
    length = 0
    in_block = False

    for i, pixel in enumerate(row):
        if pixel != 0 and not in_block:  # Start of a block
            start_index = i
            color = pixel
            in_block = True
            length = 1
        elif pixel == color and in_block:  # Continuing the block
            length += 1
        elif pixel != color and in_block:  # End of the block
            end_index = i - 1
            break  # Found the first block, stop searching

    # Handle case where block extends to the end of the row
    if in_block and end_index == -1:
        end_index = len(row) - 1

    if start_index != -1:
        return start_index, end_index, color, length
    else:
        return -1, -1, 0, 0 # No block found

def transform(input_grid):
    """
    Shifts the first contiguous horizontal block of non-white pixels 
    3 positions to the right within a single-row grid.

    Args:
        input_grid: A list containing a single list of integers (the input row).

    Returns:
        A list containing a single list of integers (the transformed row).
    """
    # Input is expected to be a list containing one row
    input_row = input_grid[0]
    height = 1
    width = len(input_row)
    background_color = 0 # white

    # Initialize output grid with background color
    output_row = [background_color] * width

    # Find the colored block in the input row
    start_index, end_index, block_color, block_length = find_colored_block(input_row)

    # If a block was found, shift it
    if start_index != -1:
        # Calculate the new starting position
        new_start_index = start_index + 3

        # Place the block in the output row at the new position
        # Ensure the block stays within the grid boundaries
        for i in range(block_length):
            current_output_index = new_start_index + i
            if 0 <= current_output_index < width:
                 output_row[current_output_index] = block_color

    # Return the output grid in the expected format (list of lists)
    return [output_row]
