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
        # Ensure length is positive
        if block_length > 0:
            return {'color': block_color, 'start': block_start, 'end': block_end, 'length': block_length}
        else:
             # This might happen if block starts and immediately ends due to 0 or 9
             print(f"Warning: Detected block with non-positive length at start {block_start}, end {block_end}. Investigate.")
             return None
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
    indices = np.where(row == marker_color)[0]
    if len(indices) > 0:
        return indices[0] # Return the first occurrence
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
    if not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
        print("Warning: Unexpected input grid format. Returning input.")
        return input_grid # Return input as is if format is wrong

    input_row = np.array(input_grid[0])
    grid_length = len(input_row)

    # --- Initialize Output Grid ---
    # Create a new output grid of the same size, filled with background color 0
    output_row = np.zeros_like(input_row)

    # --- Identify Elements ---
    # Find the contiguous block of non-white, non-maroon pixels
    block_info = find_colored_block(input_row)
    if not block_info:
        print("Error: Colored block not found.")
        # Return an empty grid in the expected list-of-lists format
        return [output_row.tolist()]

    # Find the single maroon marker pixel
    marker_index = find_marker_pixel(input_row)
    if marker_index == -1:
        print("Error: Marker pixel not found.")
        return [output_row.tolist()]

    # --- Calculate Geometry ---
    # Calculate the size of the gap (number of 0s) between block end and marker start
    # G = M - E_block - 1
    gap_size = marker_index - block_info['end'] - 1
    if gap_size < 0:
        # This implies overlap or adjacency, which contradicts example patterns
        print("Warning: Gap size is negative or zero, input structure might be unexpected.")
        # Proceed assuming minimum possible gap if needed, or adjust based on task rules
        gap_size = max(0, gap_size) # Treat unexpected overlap as zero gap for calculation

    # --- Construct Output Grid ---
    # 1. Place the marker pixel (color 9) at its original index M
    # Bounds check (should be intrinsically ok as M comes from input)
    if 0 <= marker_index < grid_length:
        output_row[marker_index] = 9
    else:
        # This case should be logically impossible if marker_index was found correctly
        print(f"Error: Marker index {marker_index} out of bounds.")
        return [np.zeros_like(input_row).tolist()] # Return empty grid

    # 2. Calculate the starting index for the colored block in the output grid
    # Output_S_block = M + G + 1
    block_output_start = marker_index + gap_size + 1

    # 3. Calculate the ending index (exclusive) for the colored block
    block_output_end_exclusive = block_output_start + block_info['length']

    # 4. Place the colored block (color C, length L) into the output grid
    # Perform bounds check to prevent errors if rearranged block exceeds grid limits
    if block_output_start >= grid_length:
        # Block starts outside the grid, nothing to place
         print(f"Warning: Calculated block start {block_output_start} is outside grid bounds {grid_length}.")
    elif block_output_end_exclusive > grid_length:
        # Block partially fits, place the part that does
        print(f"Warning: Calculated block end {block_output_end_exclusive} exceeds grid bounds {grid_length}. Truncating.")
        output_row[block_output_start : grid_length] = block_info['color']
    else:
        # Block fits entirely
        output_row[block_output_start : block_output_end_exclusive] = block_info['color']


    # --- Format and Return Output ---
    # Return the transformed row in the expected list-of-lists format
    return [output_row.tolist()]