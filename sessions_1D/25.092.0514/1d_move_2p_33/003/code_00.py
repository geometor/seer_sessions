import collections

def find_colored_block(row):
    """
    Finds the start index, end index (inclusive), and color 
    of the first contiguous non-zero block in a 1D list.

    Args:
        row: A list representing a row of the grid.

    Returns:
        A tuple (start_index, end_index, color). 
        Returns (None, None, None) if no non-zero block is found.
    """
    start_index = -1
    end_index = -1
    color = 0
    in_block = False
    for i, pixel in enumerate(row):
        # Ensure pixel is treated as an integer
        try:
            p_val = int(pixel)
        except (ValueError, TypeError):
            p_val = 0 # Treat non-integer values as background

        # If we find a non-zero pixel and haven't started a block yet
        if p_val != 0 and not in_block:
            start_index = i  # Mark the start
            color = p_val    # Record the color
            in_block = True  # Set flag indicating we are in a block
            end_index = i    # Update end_index (for single-pixel blocks)
        # If we find a non-zero pixel and are already in a block
        elif p_val != 0 and in_block:
            if p_val == color: # Continue the block if the color is the same
                end_index = i # Update the end index
            else: # Found a different color, end the current block search
                 break 
        # If we find a zero pixel and were previously in a block
        elif p_val == 0 and in_block:
            break  # The block has ended, stop searching

    # If no block was ever started
    if start_index == -1:
        return None, None, None

    return start_index, end_index, color

def transform(input_grid):
    """
    Identifies a single contiguous block of non-white pixels in the input row 
    (assumed to be 1xN) and shifts it two positions to the right in the output grid. 
    The background remains white (0), and the grid dimensions are preserved.
    Uses standard Python lists.
    """
    
    # --- Input Validation and Setup ---
    # Check if input_grid is valid and has at least one row
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0]:
        return [] # Return empty for invalid input
        
    # Assume the grid is 1D (one row) based on examples
    input_row = list(input_grid[0]) # Ensure it's a list
    height = 1 
    width = len(input_row)
    background_color = 0

    # Initialize output grid (as a list) with background color
    output_row = [background_color] * width

    # --- Find the colored block ---
    start_index, end_index, block_color = find_colored_block(input_row)

    # --- Apply Transformation ---
    # If a block was found
    if start_index is not None:
        # Calculate the length of the block
        block_length = end_index - start_index + 1

        # Calculate the starting index for the shifted block (shift right by 2)
        new_start_index = start_index + 2

        # Place the block into the output row at the new position
        for i in range(block_length):
            current_output_index = new_start_index + i
            
            # Ensure the index is within the grid bounds before writing
            if 0 <= current_output_index < width:
                output_row[current_output_index] = block_color

    # --- Format Output ---
    # Return the result as a list of lists (grid format)
    output_grid = [output_row]
    return output_grid