"""
Transforms an input grid (1xN 2D NumPy array) by rearranging segments within its single row.
1. Extracts the single data row from the input grid.
2. Identifies four segments in the row:
    a. `prefix`: Pixels before the first contiguous block of non-white(0)/non-blue(1) color.
    b. `main_block`: The first contiguous block of identical pixels with a color other than white(0) or blue(1).
    c. `white_pair`: The first occurrence of the sequence [0, 0] (two adjacent white pixels).
    d. `suffix`: Pixels after the `white_pair`.
3. Swaps the positions of `main_block` and `white_pair`.
4. Constructs the output row by concatenating: `prefix`, `white_pair`, `main_block`, `suffix`.
5. Formats the output row back into a 1xN 2D NumPy array.
"""

import numpy as np

def find_main_block(row):
    """
    Finds the first contiguous block of identical pixels in the row with color neither 0 nor 1.
    Returns the start index and end index (inclusive) of the block.
    Returns None, None if no such block is found.
    """
    start_index = -1
    current_start = -1
    current_color = -1

    for i, color in enumerate(row):
        # Check if the color is a potential main block color
        if color != 0 and color != 1:
            # If it's the start of a potential block
            if current_start == -1:
                current_start = i
                current_color = color
            # If it continues the current block
            elif color == current_color:
                continue # Block continues
            # If it's a different non-0/1 color, the previous block ended
            else:
                # Found the first valid block, return its bounds
                return current_start, i - 1
        # If the color is 0 or 1, it ends any current block
        else:
            # If a block was being tracked, it just ended. Return its bounds.
            if current_start != -1:
                return current_start, i - 1
            # Reset tracking if no block was active
            current_start = -1
            current_color = -1

    # Check if a block was running until the end of the row
    if current_start != -1:
         return current_start, len(row) - 1

    # If no block was ever found
    return None, None


def find_white_pair(row):
    """
    Finds the first occurrence of the sequence [0, 0] in the row.
    Returns the start index of the pair.
    Returns None if not found.
    """
    for i in range(len(row) - 1):
        if row[i] == 0 and row[i+1] == 0:
            return i
    return None


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D NumPy array representing the input grid (expected shape 1xN).

    Returns:
        A 2D NumPy array representing the transformed output grid (shape 1xN).
    """
    # Verify input shape is 1xN
    if input_grid.shape[0] != 1:
        print(f"Warning: Expected input grid with 1 row, but got shape {input_grid.shape}")
        # Attempt to proceed assuming the first row is the target, or handle error appropriately
        if input_grid.shape[0] == 0:
             print("Error: Input grid has 0 rows.")
             return input_grid # Or raise error

    # 1. Extract the single data row
    data_row = input_grid[0]

    # 2. Find the main block
    main_block_start, main_block_end = find_main_block(data_row)
    if main_block_start is None:
        print("Error: Main block not found in the data row.")
        return input_grid # Or raise an error

    # 3. Find the white pair [0, 0]
    white_pair_start = find_white_pair(data_row)
    if white_pair_start is None:
         print("Error: White pair [0, 0] not found in the data row.")
         return input_grid # Or raise an error

    # 4. Identify the segments based on the found indices.
    #    Assumption based on examples: structure is prefix, main_block, white_pair, suffix.
    #    We extract based on the start/end indices found.
    prefix = data_row[:main_block_start]
    main_block = data_row[main_block_start : main_block_end + 1]
    # Be careful with slicing for the white_pair to ensure it has length 2
    white_pair = data_row[white_pair_start : white_pair_start + 2]
    suffix = data_row[white_pair_start + 2 :]

    # Optional: Check if the assumption that white_pair immediately follows main_block holds
    if main_block_end + 1 != white_pair_start:
        print(f"Warning: Assumption that white_pair ([0,0] starting at {white_pair_start}) immediately follows main_block (ending at {main_block_end}) might be incorrect for this input.")
        # The current segment extraction logic relies on this structure.
        # If the order could be different (e.g., white_pair before main_block),
        # the segmentation logic would need adjustment. However, proceeding based on examples.

    # 5. Construct the output row by rearranging
    #    Order: prefix, white_pair, main_block, suffix
    # Use np.concatenate for combining numpy arrays
    output_row = np.concatenate([prefix, white_pair, main_block, suffix])

    # 6. Format the output row back into a 2D grid (1xN)
    #    Use reshape or np.array([...])
    output_grid = output_row.reshape(1, -1)
    # Alternative: output_grid = np.array([output_row])

    return output_grid