import numpy as np

"""
Transforms a 1-dimensional NumPy array of integers.
The transformation identifies the first non-zero element in the input array. 
A content block is defined starting from this first non-zero element. 
The length of this block is the minimum of 8 and the remaining length of the 
array from the starting element. This content block is then shifted 4 positions 
to the left. If shifting by 4 positions would move the start of the block before 
index 0, the block is placed starting at index 0 instead. The output array is 
initialized with zeros, and the shifted content block is placed into it. 
If the input array contains only zeros, the output array is also all zeros 
of the same shape.
"""

def _find_first_non_zero_index(input_grid: np.ndarray) -> int | None:
    """
    Finds the index of the first non-zero element in a 1D NumPy array.

    Args:
        input_grid: The 1D input NumPy array.

    Returns:
        The index of the first non-zero element, or None if all elements are zero.
    """
    # Find indices of all non-zero elements. np.nonzero returns a tuple of arrays,
    # one for each dimension. For 1D, we take the first element of the tuple.
    non_zero_indices = np.nonzero(input_grid)[0]

    # If the array of non-zero indices is empty, it means all elements were zero.
    if non_zero_indices.size == 0:
        return None
    else:
        # Otherwise, the first non-zero index is the minimum of these indices.
        return np.min(non_zero_indices)

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the defined block shifting transformation to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array containing the transformed sequence of integers.
    """
    # Get the total length of the input sequence (number of elements)
    n = input_grid.shape[0]

    # Find the index of the first non-zero element using the helper function
    start_index_input = _find_first_non_zero_index(input_grid)

    # Handle the case where the input array contains only zeros
    if start_index_input is None:
        # If no non-zero element is found, return an array of zeros
        # with the same shape and data type as the input array.
        return np.zeros_like(input_grid)

    # Calculate the length of the content block based on the rules:
    # It's the minimum of 8, or the number of elements remaining in the array
    # starting from the first non-zero element.
    block_len = min(8, n - start_index_input)

    # Extract the content block (sub-array) from the input array using slicing.
    # The slice starts at start_index_input and extends for block_len elements.
    content_block = input_grid[start_index_input : start_index_input + block_len]

    # Calculate the target starting index for the block in the output array.
    # The rule is to shift left by 4 positions (subtract 4 from start_index_input),
    # but ensure the resulting index is not negative (use max with 0).
    output_start_index = max(0, start_index_input - 4)

    # Initialize the output array with zeros. It should have the same shape
    # and data type as the input array.
    output_grid = np.zeros_like(input_grid)

    # Calculate the end index for placing the block in the output array.
    # The slice end index is exclusive, so it's the start index plus the length.
    output_end_index = output_start_index + block_len

    # Place the extracted content block into the initialized output array
    # using slicing. The elements of content_block replace the zeros
    # in the corresponding segment of output_grid.
    output_grid[output_start_index:output_end_index] = content_block

    # Return the resulting transformed array
    return output_grid