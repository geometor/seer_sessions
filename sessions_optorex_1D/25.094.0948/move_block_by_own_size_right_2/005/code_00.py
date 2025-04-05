import numpy as np

"""
Transformation Rule:
1. Receive the input sequence of 12 integers. Ensure it is treated as a flat, one-dimensional sequence (flatten if necessary).
2. Scan the sequence to locate the single contiguous block of identical non-zero integers.
3. Identify the properties of this block: its non-zero integer value, its length (number of elements), and its starting index (0-based) in the input sequence.
4. Calculate the target starting index for the block in the output sequence: add the block's length to its starting index from the input sequence.
5. Create a new output sequence consisting of 12 zeros.
6. Place the identified block (using its original value and length) into the output sequence, starting at the calculated target starting index. Ensure the block placement respects the sequence boundaries.
7. Return the generated output sequence.
"""

def find_block_properties(grid_arr):
    """
    Finds the contiguous block of identical non-zero numbers in a 1D numpy array.

    Args:
        grid_arr: A 1D numpy array of integers.

    Returns:
        A tuple containing:
        - value: The non-zero value of the block (int). Returns None if no block found.
        - start_index: The starting index of the block (int). Returns -1 if no block found.
        - length: The length of the block (int). Returns 0 if no block found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.where(grid_arr != 0)[0]

    # Handle case where there are no non-zero elements
    if len(non_zero_indices) == 0:
        return None, -1, 0

    # Determine properties of the first non-zero element (start of the assumed block)
    start_index = non_zero_indices[0]
    value = grid_arr[start_index]
    length = 0

    # Iterate through the non-zero indices to find the *contiguous* block starting at start_index
    for i in range(len(non_zero_indices)):
        current_index = non_zero_indices[i]
        # Check if the index is part of the contiguous block and has the correct value
        if current_index == start_index + i and grid_arr[current_index] == value:
            length += 1
        else:
            # Stop counting as soon as the block breaks (non-contiguous or different value)
            # This assumes only one block exists per the problem description.
            break

    return int(value), int(start_index), int(length)

def transform(input_grid):
    """
    Applies the transformation rule to shift the non-zero block right by its length.
    """
    # Step 1: Ensure input is treated as a flat, one-dimensional numpy array
    input_arr = np.array(input_grid).flatten()
    grid_size = len(input_arr) # Typically 12 based on examples

    # Step 2 & 3: Identify the non-zero block properties
    block_value, start_index, block_length = find_block_properties(input_arr)

    # Handle the case where no block is found (should not happen based on examples)
    if block_value is None:
        return np.zeros(grid_size, dtype=int) # Return an array of zeros

    # Step 4: Calculate the target starting index for the output
    # Shift distance is equal to block length
    shift_distance = block_length
    new_start_index = start_index + shift_distance

    # Step 5: Create a new output sequence of zeros
    output_grid = np.zeros(grid_size, dtype=int)

    # Step 6: Place the identified block into the output sequence at the new position
    # Calculate the end index (exclusive) for slicing
    new_end_index = new_start_index + block_length

    # Check boundaries and perform slice assignment
    if new_start_index < grid_size:
        # Ensure the end index doesn't exceed the grid size for slicing
        actual_end_index = min(new_end_index, grid_size)
        output_grid[new_start_index:actual_end_index] = block_value

    # Step 7: Return the generated output sequence as a list (if required by framework)
    # or keep as numpy array depending on expected output type. Let's return list for compatibility.
    return output_grid.tolist()