import numpy as np

"""
Shift a contiguous block of identical non-zero digits within a 1D NumPy array of 12 integers two positions to the right. The array otherwise consists of zeros.
"""

def find_non_zero_block(arr):
    """
    Finds the start index, end index (inclusive), and value of the first contiguous non-zero block.

    Args:
        arr: 1D NumPy array of integers.

    Returns:
        A tuple (start_index, end_index, block_value) if a block is found,
        otherwise (-1, -1, 0).
    """
    start_index = -1
    end_index = -1
    block_value = 0
    n = len(arr)

    for i, val in enumerate(arr):
        if val != 0:
            # Found the start of a potential block
            if start_index == -1:
                start_index = i
                block_value = val
                end_index = i # Tentatively set end index
                # Look ahead to find the true end of the block
                j = i + 1
                while j < n and arr[j] == block_value:
                    end_index = j
                    j += 1
                # Once the block is found (start, end, value), we can stop searching
                return start_index, end_index, block_value
            
    # If loop completes without finding any non-zero, return defaults
    return start_index, end_index, block_value


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input NumPy array by shifting the non-zero block two positions right.

    Args:
        input_grid: A 1D NumPy array of 12 integers containing a single
                    contiguous block of identical non-zero digits.

    Returns:
        A 1D NumPy array of 12 integers with the block shifted right by 2 positions.
    """
    # Get the size of the input array
    n = len(input_grid)

    # Initialize the output grid with zeros, matching the input size and type
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero block in the input grid
    start_index, end_index, block_value = find_non_zero_block(input_grid)

    # Proceed only if a valid block was found
    if start_index != -1:
        # Calculate the length of the block
        block_length = end_index - start_index + 1

        # Calculate the new starting position for the block (shift right by 2)
        new_start_index = start_index + 2

        # Calculate the new ending position (exclusive for slicing)
        new_end_slice_index = new_start_index + block_length

        # Ensure the new block position is within the grid bounds
        if new_start_index >= 0 and new_end_slice_index <= n:
            # Place the block (represented by its value) into the output grid at the new position
            output_grid[new_start_index:new_end_slice_index] = block_value
        # else: # Optional: Handle cases where the shift goes out of bounds, though not seen in examples
            # print(f"Warning: Shifted block exceeds bounds for input: {input_grid}")
            # pass # Current behavior leaves the output grid as zeros if block shifts out

    # Return the modified grid
    return output_grid