"""
Transforms a 1xN input grid based on the following rules:
1. Identify the single green pixel (3) which acts as a fixed anchor.
2. Identify the contiguous horizontal block of a single color (not white 0 or green 3).
3. In the output grid (same dimensions as input, initially all white 0), place the green anchor pixel at its original position.
4. Reposition the colored block such that its rightmost pixel is immediately to the left of the green anchor pixel.
"""

import numpy as np

def find_green_pixel_col(grid_row):
    """Finds the column index of the green pixel (3) in a 1D row."""
    for col_idx, pixel in enumerate(grid_row):
        if pixel == 3:
            return col_idx
    return -1 # Should not happen based on examples

def find_colored_block_info(grid_row):
    """
    Finds the contiguous block of non-white (0) and non-green (3) pixels in a 1D row.
    Returns the color, length, and original start column index of the block.
    """
    block_color = -1
    start_col = -1
    length = 0
    in_block = False

    for col_idx, pixel in enumerate(grid_row):
        # Check if the pixel is part of the colored block (not 0 and not 3)
        is_block_pixel = (pixel != 0 and pixel != 3)

        if not in_block and is_block_pixel:
            # Start of a new block
            block_color = pixel
            start_col = col_idx
            length = 1
            in_block = True
        elif in_block:
            if is_block_pixel and pixel == block_color:
                # Continue the current block
                length += 1
            else:
                # End of the block (found 0, 3, or different color)
                break # Stop searching once the first block is found and ended

    if start_col != -1:
        return block_color, length, start_col
    else:
        # No block found (should not happen based on examples)
        return -1, 0, -1

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)

    # Ensure it's a 2D array, even if 1xN
    if input_array.ndim == 1:
        input_array = np.array([input_array]) # Reshape to 1xN if needed (though examples are lists of lists)

    # Get grid dimensions (height should be 1, width N)
    height, width = input_array.shape
    if height != 1:
        # This specific solution assumes a 1xN grid based on examples
        raise ValueError(f"Input grid has unexpected height: {height}. Expected 1.")

    # Initialize the output grid with the same dimensions, filled with white (0)
    output_array = np.zeros_like(input_array)

    # Extract the first (and only) row for processing
    input_row = input_array[0]

    # --- Step 1 & 3: Find and place the green anchor pixel ---
    green_col_idx = find_green_pixel_col(input_row)
    if green_col_idx == -1:
         # Handle error: Green pixel not found
         print("Warning: Green pixel (3) not found in input.")
         # Return the empty grid or raise error depending on expected behavior
         return output_array.tolist()

    # Place green pixel in the output grid
    output_array[0, green_col_idx] = 3

    # --- Step 2: Find the colored block ---
    block_color, block_length, _ = find_colored_block_info(input_row)

    # --- Step 4: Calculate position and place the colored block ---
    if block_color != -1 and block_length > 0:
        # Calculate the new starting column for the block in the output grid
        # The end column of the block should be green_col_idx - 1
        # The end column is new_start_col + block_length - 1
        # So, new_start_col + block_length - 1 = green_col_idx - 1
        # Simplified: new_start_col = green_col_idx - block_length
        new_start_col = green_col_idx - block_length

        # Define the end column (exclusive for slicing)
        new_end_col = new_start_col + block_length

        # Check if the placement is valid within grid boundaries
        if new_start_col >= 0 and new_end_col <= width:
            # Place the block in the output grid's first row
            output_array[0, new_start_col:new_end_col] = block_color
        else:
            # Handle case where block placement calculation goes out of bounds
            print(f"Warning: Calculated block placement [{new_start_col}:{new_end_col}] is out of grid bounds [0:{width}].")
            # Depending on strictness, might return partially filled grid or raise error.
            # Current implementation allows partial placement if start is valid but end is not.

    # Convert the output numpy array back to a list of lists format
    output_grid = output_array.tolist()

    return output_grid