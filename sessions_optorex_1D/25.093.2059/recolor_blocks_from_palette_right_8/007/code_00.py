"""
Transforms a 1D NumPy array of integers based on the following rule:
1. Identify all non-zero numbers in the input array, maintaining their relative order. This forms the 'replacement pool'.
2. Identify all contiguous blocks within the input array that consist solely of the number '5' and have a length of two or more. These are 'target blocks'.
3. Create a copy of the input array.
4. Iterate through the identified target blocks, ordered by their starting position. For the k-th target block (0-indexed), replace all elements within that block's range in the copied array with the value from the replacement pool at index (k modulo N), where N is the total number of values in the replacement pool.
5. If the replacement pool is empty or no target blocks are found, return the original array unchanged (as a copy).
6. Numbers in the input array that are 0, single 5s, or non-zero numbers not part of a target block remain in their original positions in the output array.
"""

import numpy as np

def get_replacement_pool(input_array: np.ndarray) -> list[int]:
    """
    Extracts all non-zero elements from a NumPy array, preserving order.

    Args:
      input_array: A 1D NumPy array of integers.

    Returns:
      A list containing all non-zero elements from the input sequence.
    """
    # Use boolean indexing to select elements that are not equal to 0
    # Convert the resulting NumPy array to a standard Python list
    return input_array[input_array != 0].tolist()

def find_target_blocks(input_array: np.ndarray) -> list[tuple[int, int]]:
    """
    Identifies contiguous blocks of two or more 5s in a NumPy array.

    Args:
      input_array: A 1D NumPy array of integers.

    Returns:
      A list of tuples, where each tuple is (start_index, end_index)
      inclusive for a block of 5s with length >= 2. Returns an empty list
      if no such blocks are found.
    """
    blocks = []
    in_block = False
    start_index = -1
    count = 0
    # Iterate through the array to find start and end points of blocks of 5s
    for i, num in enumerate(input_array):
        if num == 5:
            if not in_block:
                # Potential start of a block
                in_block = True
                start_index = i
                count = 1
            else:
                # Continuing an existing block
                count += 1
        elif num != 5:
            # Element is not 5, check if we were in a block
            if in_block:
                # Check if the block we just exited was long enough (>= 2)
                if count >= 2:
                    blocks.append((start_index, i - 1)) # i is the first non-5
                # Reset block tracking regardless of length
                in_block = False
                start_index = -1
                count = 0
    # After the loop, check if the array ended while inside a valid block
    if in_block and count >= 2:
        blocks.append((start_index, len(input_array) - 1))
    return blocks

def transform(input_array: np.ndarray) -> np.ndarray:
    """Applies the transformation rule to the input NumPy array."""

    # Step 1: Identify the pool of values for replacement (all non-zeros)
    replacement_pool = get_replacement_pool(input_array)

    # Step 2: Identify the target blocks (sequences of '55' or longer)
    target_blocks = find_target_blocks(input_array)

    # Step 3: Initialize the output array as a copy of the input
    output_array = np.copy(input_array)

    # Step 4: Check if replacements are possible/necessary
    num_replacements = len(replacement_pool)
    if num_replacements == 0 or not target_blocks:
        # If no non-zero numbers exist or no target blocks found, return the unmodified copy
        return output_array

    # Step 5: Iterate through target blocks and apply replacements
    for block_index, (start, end) in enumerate(target_blocks):
        # Determine the replacement value, cycling through the replacement pool
        # Use modulo operator for cycling based on the block's order (block_index)
        pool_index = block_index % num_replacements
        current_replacement_value = replacement_pool[pool_index]

        # Replace all elements within the current target block's range [start, end]
        # Use NumPy slicing for efficient assignment
        output_array[start : end + 1] = current_replacement_value

    # Step 6: Return the modified array
    return output_array