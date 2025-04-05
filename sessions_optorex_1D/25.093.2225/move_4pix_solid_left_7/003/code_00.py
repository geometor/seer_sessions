import numpy as np

"""
Transforms an input sequence (list or array of 12 integers) by identifying the 
single contiguous block of identical non-zero integers and shifting this block 
4 positions to the left. Positions outside the shifted block in the output 
sequence are filled with zeros. Parts of the block shifted beyond the left 
boundary (index < 0) are discarded.
"""

def find_nonzero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero integers in the sequence.

    Args:
        sequence: A list or NumPy array of integers.

    Returns:
        A tuple containing:
        - value (int): The non-zero value of the block (or 0 if no block found).
        - start_index (int): The starting index of the block (-1 if no block found).
        - length (int): The length of the block (0 if no block found).
    """
    # Convert to NumPy array for efficient searching if it's not already one
    arr = np.array(sequence)
    
    # Find indices of all non-zero elements
    non_zero_indices = np.where(arr != 0)[0]

    # If no non-zero elements, return defaults
    if len(non_zero_indices) == 0:
        return 0, -1, 0

    # Identify the start index and value of the first non-zero element
    start_index = non_zero_indices[0]
    value = arr[start_index]
    length = 0

    # Determine the length of the contiguous block starting from start_index
    for i in range(start_index, len(arr)):
        if arr[i] == value:
            length += 1
        else:
            # Stop counting when the value changes or a zero is encountered
            break
            
    # Basic validation: ensure all found non-zeros belong to this single block
    # This check might be redundant given the problem's constraints but adds robustness.
    if len(non_zero_indices) != length or not np.all(arr[start_index : start_index + length] == value):
         # This case shouldn't happen based on the examples, but good to note.
         # We'll proceed with the found block based on the first non-zero element.
         pass 

    return value, start_index, length


def transform(input_grid):
    """
    Applies the left-shift transformation to the input sequence.

    Args:
        input_grid: A list or array of 12 integers representing the input sequence.

    Returns:
        A list of 12 integers representing the transformed output sequence.
    """
    # Ensure input is a NumPy array for processing
    input_array = np.array(input_grid)
    sequence_length = len(input_array)

    # 1. Initialize an output sequence of the correct length with zeros.
    output_grid = np.zeros(sequence_length, dtype=int)

    # 2. Find the non-zero block in the input sequence.
    block_value, start_index, block_length = find_nonzero_block(input_array)

    # 3. If a block was found, proceed with the shift.
    if start_index != -1:
        # 4. Calculate the target start index in the output sequence.
        new_start_index = start_index - 4

        # 5. Place the block into the output sequence at the new position.
        # Iterate through each position of the block.
        for i in range(block_length):
            # Calculate the index where this part of the block should go in the output.
            output_index = new_start_index + i

            # Check if the calculated output index is within the valid bounds (0 to sequence_length-1).
            if 0 <= output_index < sequence_length:
                # If valid, place the block's value at this position in the output grid.
                output_grid[output_index] = block_value

    # Convert the NumPy array back to a standard Python list for the return value.
    return output_grid.tolist()