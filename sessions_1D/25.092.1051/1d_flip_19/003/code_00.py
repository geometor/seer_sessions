import copy

"""
Identifies a contiguous block of non-white pixels (values 1-9) in the first row of the 2D input grid.
Performs a left cyclic shift on the colors within that block (moves the first element to the end).
Returns the modified grid, keeping the white pixels (value 0) and the block's position unchanged.
Assumes the input is a 2D grid (list of lists) and the transformation applies only to the first row.
"""

def find_non_white_block(row):
    """
    Finds the start and end indices of the first contiguous non-white block in a 1D list.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A tuple (start_index, end_index). Returns (-1, -1) if no block is found or the row is empty.
    """
    if not row:
        return -1, -1
        
    start = -1
    end = -1
    in_block = False
    for i, pixel in enumerate(row):
        # Check if pixel is non-white (greater than 0)
        if pixel > 0:  
            if not in_block:
                # Mark the start of a new block
                start = i
                in_block = True
            # Update the end index for the current block
            end = i
        elif in_block:  
            # Found a white pixel after the block started
            # Assuming only one block per row based on examples, so we can stop searching
            break
            
    # Check if a block was ever actually found
    if not in_block:
        return -1, -1
        
    return start, end

def cyclic_shift_left(sequence):
    """
    Performs a left cyclic shift on the sequence (list).
    The first element moves to the end.

    Args:
        sequence: A list of elements.

    Returns:
        A new list with elements cyclically shifted left by one position.
        Returns a copy of the original sequence if its length is 0 or 1.
    """
    # If the sequence has 0 or 1 elements, shifting has no effect
    if len(sequence) <= 1:
        return sequence[:] # Return a copy

    # Create the shifted sequence: take elements from index 1 onwards,
    # then append the original first element (at index 0) to the end.
    shifted = sequence[1:] + [sequence[0]]
    return shifted

def transform(input_grid):
    """
    Transforms the input grid by applying a left cyclic shift to the
    first contiguous non-white block found in the first row.

    Args:
        input_grid: A list of lists of integers representing the 2D input grid.

    Returns:
        A list of lists of integers representing the transformed 2D output grid.
    """
    # Create a deep copy of the input grid to avoid modifying the original
    # This is important as lists are mutable
    output_grid = copy.deepcopy(input_grid)

    # Check if the grid has at least one row
    if not output_grid:
        return output_grid # Return the empty grid if input is empty

    # Target the first row for modifications, as seen in examples
    target_row = output_grid[0]

    # Find the start and end indices of the contiguous non-white block in the target row
    start_index, end_index = find_non_white_block(target_row)

    # Proceed only if a valid block was found (start_index is not -1)
    if start_index != -1:
        # Extract the sub-sequence (the block) from the target row
        # Slicing includes start_index up to (but not including) end_index + 1
        block_sequence = target_row[start_index : end_index + 1]

        # Perform the left cyclic shift on the extracted block sequence
        shifted_block_sequence = cyclic_shift_left(block_sequence)

        # Replace the corresponding segment in the target row (within the output_grid)
        # with the shifted block sequence
        target_row[start_index : end_index + 1] = shifted_block_sequence
        # Note: Since target_row refers to output_grid[0], modifying target_row
        # directly modifies output_grid[0].

    # Return the modified grid
    return output_grid