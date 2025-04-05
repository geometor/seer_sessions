"""
Identifies a contiguous subsequence composed entirely of non-zero integers 
within the input sequence. Creates a new sequence of the same length 
initialized with zeros. Calculates a new starting index for the non-zero 
subsequence by adding 4 to its original starting index. Places the 
identified non-zero subsequence into the output sequence beginning at the 
new starting index, handling potential boundary conditions. Outputs the 
modified sequence as a standard Python list.
"""

# No external libraries needed for this logic

# Helper function to find the contiguous non-zero block
def find_non_zero_block(sequence):
    """
    Finds the start index and content of the first contiguous non-zero block.

    Args:
        sequence: A list of numbers.

    Returns:
        A tuple (start_index, block_content).
        Returns (-1, []) if no non-zero block is found.
    """
    start_index = -1
    non_zero_block = []
    in_block = False
    for i, val in enumerate(sequence):
        # If we find a non-zero value
        if val != 0:
            # If this is the start of the block, record the index
            if not in_block:
                start_index = i
                in_block = True
            # Append the value to our block content
            non_zero_block.append(val)
        # If we encounter a zero *after* the block has started
        elif in_block:
            # The block has ended
            return start_index, non_zero_block
            
    # If we reached the end of the sequence and a block was active, return it
    if in_block:
        return start_index, non_zero_block
        
    # If no non-zero value was ever found
    return -1, []

def transform(input_grid):
    """
    Transforms the input sequence by shifting the non-zero block right by 4.
    """
    # Ensure input is a list (in case it's a numpy array from test harness)
    input_list = list(input_grid) 
    
    # Determine the size of the input sequence
    grid_size = len(input_list)
    
    # Initialize output_grid with all zeros, same size as input
    output_grid = [0] * grid_size

    # Identify the non-zero block and its start index
    start_index, non_zero_block = find_non_zero_block(input_list)

    # Proceed only if a non-zero block was actually found
    if start_index != -1:
        # Calculate the new starting index by shifting 4 positions to the right
        new_start_index = start_index + 4
        
        # Determine the length of the non-zero block
        block_len = len(non_zero_block)

        # Place the non-zero block into the output grid at the new position
        # Iterate through the elements of the found block
        for i in range(block_len):
            # Calculate the corresponding index in the output grid
            output_index = new_start_index + i
            
            # Check if the calculated index is within the bounds of the output grid
            if 0 <= output_index < grid_size:
                 # Place the element from the non-zero block into the output grid
                 output_grid[output_index] = non_zero_block[i]
            # else: If the shift would place elements outside the grid, they are ignored (truncated)

    # Return the resulting output grid (as a standard list)
    return output_grid