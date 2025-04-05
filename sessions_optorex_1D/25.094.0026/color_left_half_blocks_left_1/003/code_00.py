"""
Transforms a sequence (NumPy array) of 0s and 2s by selectively replacing some 2s with 8s.
The replacement rule depends on the length (L) of contiguous blocks of 2s found in the input:
- If L = 1: The 2 remains unchanged.
- If L = 2 or L = 3: The last 2 in the block becomes 8 in the output.
- If L >= 4: The last two 2s in the block become 8s in the output.
0s remain unchanged in their positions.
"""

import numpy as np # Import numpy for array operations

# Helper function to find contiguous blocks of a specific value
def find_blocks(data_array, value):
    """
    Identifies contiguous blocks of a specified value in a NumPy array.

    Args:
        data_array: The NumPy array to search within (e.g., np.array([0, 2, 2, 0, 2])).
        value: The value to search for blocks of (e.g., 2).

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains 'start' (index) and 'length' of the block.
        e.g., [{'start': 1, 'length': 2}, {'start': 4, 'length': 1}]
    """
    blocks = []
    i = 0
    n = len(data_array)
    while i < n:
        # Check if the current element matches the target value
        if data_array[i] == value:
            start_index = i
            j = i
            # Find the end of the contiguous block
            while j < n and data_array[j] == value:
                j += 1
            # Calculate the length of the block
            length = j - start_index
            # Record the block's start index and length
            blocks.append({'start': start_index, 'length': length})
            # Move the main index past the found block
            i = j
        else:
            # Move to the next element if it doesn't match the target value
            i += 1
    return blocks

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.
    """
    # 1. Initialize output_grid as a copy of the input_grid.
    # We modify this copy, leaving the original input_grid unchanged.
    output_grid = input_grid.copy()

    # 2. Find all contiguous blocks of the number 2 in the input grid.
    # Example: np.array([0, 0, 2, 2, 0, 2, 2, 2, 0]) -> [{'start': 2, 'length': 2}, {'start': 5, 'length': 3}]
    blocks_of_twos = find_blocks(input_grid, 2)

    # 3. Iterate through each found block of 2s and apply transformation rules to the output_grid.
    for block in blocks_of_twos:
        start_index = block['start']
        length = block['length']
        # Calculate the index of the last element in the block
        last_element_index = start_index + length - 1

        # Apply rule: If block length is 2 or 3, change the last element to 8 in the output grid.
        if length == 2 or length == 3:
            # Check bounds just in case, though find_blocks should ensure validity.
            if 0 <= last_element_index < len(output_grid):
                output_grid[last_element_index] = 8

        # Apply rule: If block length is 4 or more, change the last two elements to 8 in the output grid.
        elif length >= 4:
            # Change the last element if index is valid
            if 0 <= last_element_index < len(output_grid):
                output_grid[last_element_index] = 8
            # Change the second-to-last element if index is valid
            second_last_element_index = last_element_index - 1
            if 0 <= second_last_element_index < len(output_grid):
                output_grid[second_last_element_index] = 8

        # No action is needed if length is 1, as the corresponding element
        # in output_grid already holds the original value (2).

    # 4. Return the modified output grid.
    return output_grid