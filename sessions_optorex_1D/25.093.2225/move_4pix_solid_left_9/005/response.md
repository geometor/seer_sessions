```python
"""
Transforms a 1D NumPy array by identifying the single contiguous block of
identical non-zero digits and shifting this block exactly 4 positions to the left.
The output array has the same size as the input, with positions outside the
shifted block filled with zeros. If the shift causes the block to extend beyond
the left boundary (index < 0), those elements are clipped.
"""

import numpy as np

def _find_block_details(input_grid: np.ndarray) -> tuple:
    """
    Finds the value, start index, and length of the unique non_zero_block.

    Args:
        input_grid: The 1D input NumPy array.

    Returns:
        A tuple (block_value, start_index, block_length).
        Returns (0, -1, 0) if no non-zero block is found.
    """
    # Find indices of non-zero elements
    non_zero_indices = np.where(input_grid != 0)[0]

    # If no non-zero elements exist
    if len(non_zero_indices) == 0:
        return 0, -1, 0 # Return placeholder values

    # Identify the start of the block and its value
    start_index = non_zero_indices[0]
    block_value = input_grid[start_index]

    # Calculate the length of the contiguous block
    block_length = 0
    for i in range(start_index, len(input_grid)):
        if input_grid[i] == block_value:
            block_length += 1
        else:
            # Stop counting when the value changes or a zero is encountered
            break

    return block_value, start_index, block_length


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block shifting transformation.

    Args:
        input_grid: A 1D NumPy array representing the input sequence.

    Returns:
        A 1D NumPy array representing the transformed sequence.
    """
    # Get the length of the input sequence
    n = len(input_grid)
    # Define the fixed shift amount
    shift_amount = 4

    # Initialize the output grid as a NumPy array of zeros with the same size and type
    output_grid = np.zeros_like(input_grid)

    # Find the details of the non-zero block in the input
    block_value, input_start_index, block_length = _find_block_details(input_grid)

    # Proceed only if a non-zero block was actually found
    if block_length > 0:
        # Calculate the target starting index for the block in the output grid
        output_start_index = input_start_index - shift_amount

        # Iterate through the positions within the block's length
        for i in range(block_length):
            # Calculate the target index in the output sequence
            current_output_index = output_start_index + i

            # Check if the target index is within the valid bounds (0 to n-1)
            # This handles the clipping automatically.
            if 0 <= current_output_index < n:
                # Place the block's value at the valid target index
                output_grid[current_output_index] = block_value

    # Return the generated output grid
    return output_grid
```