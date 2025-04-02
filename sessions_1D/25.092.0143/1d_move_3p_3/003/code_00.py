import numpy as np

"""
Identifies the single contiguous block of non-white pixels in the input row.
Shifts this block 3 positions to the right, preserving its color and length.
The rest of the row remains white (0). The input grid is assumed to have only one row.
"""

def find_colored_block(row):
    """
    Finds the start index, end index (exclusive), and color of the first
    contiguous non-white block in a 1D numpy array (row).

    Args:
        row (np.ndarray): A 1D numpy array representing the row.

    Returns:
        tuple: (start_index, end_index, color) or None if no block is found.
              Returns None if the input row is empty.
    """
    if row.size == 0:
        return None # Handle empty row case

    start_index = -1
    color = 0
    row_length = len(row)

    for i, pixel in enumerate(row):
        # Found a non-white pixel
        if pixel != 0:
            # If this is the start of a new block
            if start_index == -1:
                start_index = i
                color = pixel
            # If the color changes mid-block (shouldn't happen based on task description)
            elif pixel != color:
                 # Consider the previous block ended at index i
                 # This case implies multiple blocks or changing colors within a block,
                 # which contradicts the observed pattern. We return the first block found.
                 return start_index, i, color
        # Found a white pixel after a block started
        elif start_index != -1:
            # End of the block found at index i
            return start_index, i, color

    # If a block was found and extends to the very end of the row
    if start_index != -1:
        return start_index, row_length, color

    # No non-white block found in the entire row
    return None


def transform(input_grid):
    """
    Shifts the single colored block in a 1xN input grid 3 positions to the right.

    Args:
        input_grid (list[list[int]]): A list containing a single list (the row).

    Returns:
        list[list[int]]: The transformed grid with the block shifted.
    """
    # Convert input to numpy array for easier handling - assuming one row
    # Add error handling for unexpected input format
    if not isinstance(input_grid, list) or not input_grid or not isinstance(input_grid[0], list):
         raise ValueError("Input grid must be a non-empty list of lists.")
         
    if len(input_grid) != 1:
         # According to analysis, input should only have 1 row. Handle defensively.
         # Option 1: Raise error. Option 2: Process only the first row.
         # Choosing Option 2 for now, as it might be closer to ARC's flexibility.
         # print("Warning: Input grid has more than one row. Processing only the first row.")
         pass # Proceed with the first row

    input_row = np.array(input_grid[0], dtype=int)
    row_length = len(input_row)

    # Handle empty row case
    if row_length == 0:
        return [[]] # Return empty grid if input is empty

    # Initialize output row with white (0)
    output_row = np.zeros(row_length, dtype=int)

    # Find the colored block in the input row
    block_info = find_colored_block(input_row)

    # If a colored block was found
    if block_info:
        start_index, end_index, color = block_info
        length = end_index - start_index

        # Calculate the new starting position for the block
        new_start_index = start_index + 3
        # Calculate the new ending position (exclusive)
        new_end_index = new_start_index + length

        # Determine the actual start and end indices within the output row boundaries
        # The start index cannot be negative (though unlikely with right shift)
        # The end index cannot exceed the row length
        actual_start = max(0, new_start_index)
        actual_end = min(row_length, new_end_index)

        # Ensure there's actually a segment to write (actual_start < actual_end)
        if actual_start < actual_end:
             # Place the block (with its original color) into the output row
             # at the calculated new position, respecting boundaries.
             output_row[actual_start:actual_end] = color

    # Convert the output numpy row back to a list
    output_grid = [output_row.tolist()]

    return output_grid