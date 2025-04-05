import numpy as np

"""
Transforms a 1-dimensional NumPy array of integers by identifying a specific 
'content block' and shifting it. The content block is defined as the 
contiguous segment of the input array starting at the index of the first 
non-zero element and ending at the index of the last non-zero element. 
This block is then shifted 4 positions to the left. If shifting by 4 
positions would move the start of the block before index 0, the block is 
placed starting at index 0 instead. The output array is initialized with 
zeros, and the shifted content block overwrites the zeros at its new position. 
If the input array contains only zeros, the output array is also all zeros 
of the same shape.
"""

def _find_content_block_indices(input_grid: np.ndarray) -> tuple[int | None, int | None]:
    """
    Finds the start and end indices of the block containing all non-zero elements 
    in a 1D NumPy array.

    Args:
        input_grid: The 1D input NumPy array.

    Returns:
        A tuple containing the start index (first non-zero) and end index 
        (last non-zero) of the content block. Returns (None, None) if no 
        non-zero elements are found.
    """
    # Find indices where elements are not zero. np.nonzero returns a tuple of arrays,
    # one for each dimension. For 1D, we access the first element.
    non_zero_indices = np.nonzero(input_grid)[0] 

    # Check if any non-zero elements were found
    if non_zero_indices.size == 0:
        # No non-zero elements, return None for both start and end
        return None, None
    else:
        # Find the minimum index among non-zero elements (start of the block)
        start_index = np.min(non_zero_indices)
        # Find the maximum index among non-zero elements (end of the block)
        end_index = np.max(non_zero_indices)
        return start_index, end_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the block shifting transformation to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array containing the transformed sequence of integers.
    """
    
    # 1. Identify the start and end indices of the content block
    start_index_input, end_index_input = _find_content_block_indices(input_grid)

    # 2. Handle the case where the input array contains only zeros
    if start_index_input is None:
        # If no non-zero elements were found, return an array of zeros 
        # with the same shape and data type as the input.
        return np.zeros_like(input_grid)

    # 3. Extract the content block (sub-array) from the input array
    # The slice includes the element at end_index_input.
    content_block = input_grid[start_index_input : end_index_input + 1]
    block_len = len(content_block) # Get the length of the extracted block

    # 4. Calculate the target starting index for the block in the output array.
    # Shift left by 4, but ensure the index doesn't go below 0.
    output_start_index = max(0, start_index_input - 4)

    # 5. Initialize the output array with zeros, matching the input's shape and type.
    output_grid = np.zeros_like(input_grid)

    # 6. Calculate the end index for placing the block in the output array.
    # The slice end index is exclusive.
    output_end_index = output_start_index + block_len

    # 7. Place the extracted content block into the initialized output array
    # using slicing. The elements of content_block overwrite the zeros
    # in the corresponding segment of output_grid.
    # NumPy slicing handles assignment correctly.
    output_grid[output_start_index:output_end_index] = content_block

    # 8. Return the resulting transformed array
    return output_grid