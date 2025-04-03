import numpy as np

"""
Transforms a 1D grid (represented as a list containing one list) by rearranging
two key elements: a contiguous block of a single color (not white 0, not maroon 9)
and a single maroon pixel (9), separated by a gap of white pixels.

The transformation rule is:
1. Identify the contiguous colored block (color C, length L, end index E_block)
   and the single maroon pixel (index M) in the input row.
2. Calculate the gap size (G) between them in the input: G = M - E_block - 1.
3. Create an output row of the same size, initialized to white (0).
4. Place the maroon pixel (9) in the output row at its original index (M).
5. Calculate the starting index for the colored block in the output:
   Output_S_block = M + G + 1.
6. Place the colored block (color C, length L) into the output row, starting at
   index Output_S_block and ending at Output_S_block + L - 1.
7. Return the output row enclosed in a list.
"""

def find_colored_block(row):
    """
    Finds the first contiguous block of non-white (0), non-maroon (9) color
    in a single row.

    Args:
        row: A numpy array representing the row.

    Returns:
        A dictionary containing 'color', 'start', 'end', and 'length' of the block,
        or None if no such block is found.
    """
    block_color = -1
    block_start = -1
    block_end = -1
    in_block = False
    row_len = len(row)

    for i, pixel in enumerate(row):
        # Check for non-background, non-marker color
        if pixel != 0 and pixel != 9:
            if not in_block:
                # Start of a new potential block
                block_start = i
                block_color = pixel
                in_block = True
            # Check if the block continues or ends
            # Block ends if we reach the end of the row or the next pixel is different
            if i + 1 == row_len or row[i+1] != block_color:
                block_end = i
                break # Found the end of the block
        elif in_block:
            # If we were in a block and encounter 0 or 9, the block just ended at the previous index
            block_end = i - 1
            break

    if block_start != -1 and block_end != -1:
        block_length = block_end - block_start + 1
        return {'color': block_color, 'start': block_start, 'end': block_end, 'length': block_length}
    else:
        # This case should not happen based on the task's example structure
        return None

def find_marker_pixel(row, marker_color=9):
    """
    Finds the index of the first pixel with the marker_color in a single row.

    Args:
        row: A numpy array representing the row.
        marker_color: The color value to search for (default is 9).

    Returns:
        The index of the marker pixel, or -1 if not found.
    """
    for i, pixel in enumerate(row):
        if pixel == marker_color:
            return i
    # This case should not happen based on the task's example structure
    return -1

def transform(input_grid):
    """
    Applies the rearrangement transformation to the input grid.

    Args:
        input_grid: A list containing a single list of integers
                    representing the 1D input grid.

    Returns:
        A list containing a single list of integers
        representing the transformed 1D output grid.
    """
    # --- Input Validation and Preparation ---
    # Expecting input like [[...row data...]]
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
        # If input format is unexpected, return it unchanged or raise an error.
        # Based on ARC, we assume valid input format matching examples.
        # For robustness, one might add more specific error handling.
        print("Warning: Unexpected input grid format.")
        return input_grid # Return input as is

    input_row = np.array(input_grid[0])
    grid_length = len(input_row)

    # Initialize output grid with background color (white, 0)
    output_row = np.zeros_like(input_row)

    # --- Identify Elements ---
    # Find the colored block details
    block_info = find_colored_block(input_row)
    if not block_info:
        # Handle error: block not found (shouldn't happen in this task)
        print("Error: Colored block not found.")
        # Return an empty grid in the expected list-of-lists format
        return [output_row.tolist()]

    # Find the marker pixel index
    marker_index = find_marker_pixel(input_row)
    if marker_index == -1:
        # Handle error: marker not found (shouldn't happen in this task)
        print("Error: Marker pixel not found.")
        return [output_row.tolist()]

    # --- Calculate Geometry ---
    # Calculate the gap size between the block end and the marker start in the input
    # Assumes block is always before marker in input as per examples
    gap_size = marker_index - block_info['end'] - 1
    if gap_size < 0:
        # This would mean the marker is before or adjacent to the block, unexpected
        print("Warning: Gap size is negative or zero, unexpected input order or adjacency.")
        # Decide how to handle: maybe return error, or proceed assuming gap is 0
        gap_size = max(0, gap_size) # Treat unexpected overlap as zero gap

    # --- Construct Output ---
    # Place the marker pixel (color 9) at its original index
    # Check bounds just in case, though marker_index comes from the input row itself
    if 0 <= marker_index < grid_length:
        output_row[marker_index] = 9
    else:
        # This state should be logically impossible if marker_index was found correctly
        print(f"Error: Marker index {marker_index} out of bounds.")
        return [np.zeros_like(input_row).tolist()]

    # Calculate the starting position for the colored block in the output grid
    # Output block starts after marker (at M) + gap (of size G)
    block_output_start = marker_index + gap_size + 1

    # Calculate the ending position (exclusive) for the colored block in the output grid
    block_output_end_exclusive = block_output_start + block_info['length']

    # Place the colored block in the output grid, checking bounds
    # Ensure the calculated slice is valid for the output row dimensions
    if 0 <= block_output_start < grid_length and block_output_end_exclusive <= grid_length:
        output_row[block_output_start : block_output_end_exclusive] = block_info['color']
    else:
        # Handle case where the rearranged block would go out of bounds
        print(f"Warning: Calculated block position [{block_output_start}:{block_output_end_exclusive}] might be out of bounds for grid length {grid_length}. Clamping.")
        # Place only the part of the block that fits, starting from block_output_start
        actual_end = min(block_output_end_exclusive, grid_length)
        if block_output_start < grid_length:
             # Calculate how many elements to actually copy
             elements_to_copy = actual_end - block_output_start
             if elements_to_copy > 0:
                  output_row[block_output_start : actual_end] = block_info['color']


    # Return the transformed row in the expected list-of-lists format
    return [output_row.tolist()]