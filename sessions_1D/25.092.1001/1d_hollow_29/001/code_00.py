import numpy as np

def find_non_white_block(row):
    """
    Finds the start and end indices of the first contiguous non-white block in a 1D array.

    Args:
        row (np.array): A 1D numpy array representing a row of pixels.

    Returns:
        tuple: A tuple containing the start index and end index of the block.
               Returns (-1, -1) if no non-white block is found.
    """
    start_index = -1
    end_index = -1
    # Iterate through the row to find the first non-white pixel
    for i, pixel in enumerate(row):
        if pixel != 0:
            start_index = i
            break  # Found the start, exit the loop

    # If no start was found, there's no block
    if start_index == -1:
        return -1, -1

    # Find the end of the block by continuing from the start index
    # The end index will be the index of the last non-white pixel in the sequence
    end_index = start_index
    for i in range(start_index + 1, len(row)):
        if row[i] != 0:
            end_index = i
        else:
            # Stop as soon as a white pixel is encountered after the block started
            break

    return start_index, end_index

def transform(input_grid):
    """
    Identifies a contiguous block of non-white pixels in a single-row grid.
    Changes the interior pixels of this block to white (0), preserving only the
    first and last pixels of the original block. Background pixels outside the
    block remain unchanged.
    """
    # Convert input grid (list of lists) to a NumPy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Check if the input grid is indeed a single row
    if input_array.shape[0] != 1:
        # This function is designed for 1xN grids as per the examples.
        # If the input shape is different, return it unchanged or raise an error.
        # For this task, based on examples, we assume 1xN.
        # Returning unchanged might be safer if unexpected inputs occur.
        return input_grid

    # Extract the single row
    row = input_array[0]

    # Find the start and end indices of the non-white block
    start_index, end_index = find_non_white_block(row)

    # Initialize the output grid as a copy of the input grid
    output_array = input_array.copy()

    # Check if a valid block was found (start_index != -1)
    # and if the block has interior pixels (length > 2, which means end_index > start_index + 1)
    if start_index != -1 and end_index > start_index + 1:
        # Iterate through the interior indices of the block
        # The range is from the pixel *after* the start to the pixel *before* the end
        for i in range(start_index + 1, end_index):
            # Change the interior pixels to white (0) in the output array
            output_array[0, i] = 0
            
    # If the block length is 1 (start_index == end_index) or 2 (end_index == start_index + 1),
    # there are no interior pixels, so the loop range(start_index + 1, end_index) is empty,
    # and the output_array remains a copy of input_array, which is the correct behavior.
    # If no block is found (start_index == -1), the output_array also remains a copy.

    # Convert the NumPy array back to a list of lists for the required output format
    output_grid = output_array.tolist()
    return output_grid
