"""
Identifies the single contiguous block of non-white (non-zero) pixels in the input row (a 1D grid). 
Creates a new row of the same length filled with white (0) pixels. 
Places the identified block into the new row, starting 2 positions further to the right than its original starting position.
"""

# No external libraries needed for this task.

def find_color_block(row):
    """
    Finds the start index and the pixel values of the first contiguous block 
    of non-zero pixels in a 1D list (row). Assumes only one such block exists.

    Args:
        row (list): A list of integers representing a row of pixels.

    Returns:
        tuple: A tuple containing:
            - start_index (int): The starting index of the block (-1 if not found).
            - block (list): A list containing the pixel values of the block. Returns 
                            an empty list if no block is found.
    """
    start_index = -1
    block = []
    in_block = False
    for i, pixel in enumerate(row):
        if pixel != 0:  # Non-white pixel found
            if not in_block:
                start_index = i  # Mark the start of the block
                in_block = True
            block.append(pixel) # Add pixel to the block
        elif in_block:
            # Found a white pixel after the block started, meaning the block has ended
            break 
            # Since we assume only one block, we can stop searching.
    
    # If the loop finishes and we were still in a block (block reaches the end of the row)
    # the current start_index and block are correct.
    # If the loop finishes and we never entered a block, start_index remains -1 and block is [].

    return start_index, block

def transform(input_grid):
    """
    Transforms the input grid by shifting the color block.

    Args:
        input_grid (list of lists): A list containing a single list, which 
                                     represents the 1D row of pixels. 
                                     Example: [[0, 0, 3, 3, 3, 0]]

    Returns:
        list of lists: The transformed grid in the same format as the input, 
                       with the color block shifted right by 2 positions.
                       Example: [[0, 0, 0, 0, 3, 3, 3]]
    """
    # --- Input Processing ---
    # Expecting input like [[...]], extract the inner list which is the row
    if not input_grid or not isinstance(input_grid[0], list):
        # Basic validation, return empty if format is unexpected
        return [] 
    input_row = input_grid[0]
    row_length = len(input_row)

    # --- Initialization ---
    # Create the output row, initialized with the background color (white/0)
    output_row = [0] * row_length

    # --- Core Logic ---
    # 1. Identify the contiguous block of non-white pixels and its start index
    start_index, color_block = find_color_block(input_row)

    # 2. Check if a block was actually found
    if start_index != -1: # A block was found if start_index is not -1
        # 3. Calculate the new starting position for the block (shift right by 2)
        new_start_index = start_index + 2

        # 4. Copy the identified block to the new position in the output row
        # Iterate through the pixels of the found block using enumeration for index
        for i, pixel_value in enumerate(color_block):
            # Calculate the target index in the output row
            target_index = new_start_index + i
            
            # Ensure the target index is within the bounds of the output row
            # before attempting to write to it.
            if 0 <= target_index < row_length:
                output_row[target_index] = pixel_value
            # If the target_index goes out of bounds (block shifted off the edge), 
            # those pixels are simply not placed, effectively clipping the block.

    # --- Output Formatting ---
    # Return the transformed row wrapped in a list to match ARC grid format
    output_grid = [output_row]
    return output_grid
