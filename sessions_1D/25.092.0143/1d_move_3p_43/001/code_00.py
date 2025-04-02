import numpy as np

"""
Transformation Rule:
1. Identify the single contiguous block of non-white pixels within the input row.
2. Note its color, its starting position (index), and its length.
3. Create a new output row of the same length as the input row, initially filled entirely with white pixels (0).
4. Calculate the new starting position for the block by adding 3 to its original starting position.
5. Place the identified block (with its original color and length) into the new output row, starting at the calculated new position.
"""

def find_non_white_block(row):
    """
    Finds the start index, end index, color, and length of the first 
    contiguous non-white block in a 1D array.
    
    Args:
        row (np.array): The 1D input array.

    Returns:
        tuple: (start_index, end_index, color, length) or None if no block found.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) == 0:
        return None  # No non-white pixels found

    start_index = non_white_indices[0]
    block_color = row[start_index]
    
    # Find where the block ends (either end of array or different color)
    end_index = start_index
    for i in range(start_index + 1, len(row)):
        if row[i] == block_color:
            end_index = i
        else:
            break # End of contiguous block of this color
            
    # Verify contiguity - check if all indices between start and end are non-white
    # This is implicitly handled by the problem description stating *one* contiguous block
    # but we can double check if needed. In this case, we assume the examples are representative.
            
    length = end_index - start_index + 1
    
    return start_index, end_index, block_color, length

def transform(input_grid):
    """
    Shifts the single contiguous block of non-white pixels 3 positions to the right.

    Args:
        input_grid (list): A list containing a single list representing the input row.

    Returns:
        list: A list containing a single list representing the transformed output row.
    """
    # Ensure input is a NumPy array for easier processing
    # Since the input is given as list of lists (even for 1 row), access the first element
    input_row = np.array(input_grid[0]) 
    
    # Find the non-white block details
    block_info = find_non_white_block(input_row)
    
    if block_info is None:
        # If no block found, return the input as is (or an empty grid based on specs)
        # Based on examples, there's always a block. Return copy of input filled with white.
        return [[0] * len(input_row)] 

    start_index, end_index, block_color, length = block_info
    
    # Initialize output_grid as a row of white pixels with the same length
    output_row = np.zeros_like(input_row)
    
    # Calculate the new starting position
    new_start_index = start_index + 3
    new_end_index = new_start_index + length -1 # Calculate where the block will end

    # Ensure the new block stays within the bounds of the grid
    if new_end_index < len(output_row):
        # Place the block in the new position
        output_row[new_start_index : new_end_index + 1] = block_color
    else:
        # Handle cases where the block might go out of bounds (though not in examples)
        # For now, let's assume it fits based on the examples. If it overflows,
        # we might need to clip it or handle it differently based on task requirements.
        # Clipping implementation:
        effective_end_index = min(new_end_index, len(output_row) - 1)
        effective_length = effective_end_index - new_start_index + 1
        if effective_length > 0:
             output_row[new_start_index : effective_end_index + 1] = block_color

    # Convert the NumPy array back to the required list-of-lists format
    return [output_row.tolist()]