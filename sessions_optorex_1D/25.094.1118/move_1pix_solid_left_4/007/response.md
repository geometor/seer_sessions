```python
"""
Transforms the input numpy array by shifting the contiguous block of identical, non-zero digits 
one position to the left. This shift is accomplished by finding the first non-zero digit, 
removing the zero element immediately preceding it (provided the block doesn't start at index 0), 
and appending a zero to the end of the sequence to maintain its original length.
"""

import numpy as np

def find_first_nonzero_index(arr: np.ndarray) -> int:
    """
    Finds the index of the first non-zero element in a 1D numpy array.

    Args:
        arr: The input 1D numpy array.

    Returns:
        The index of the first non-zero element, or -1 if all elements are zero 
        or the array is empty.
    """
    # np.nonzero returns a tuple of arrays, one for each dimension.
    # For a 1D array, it's a tuple with one array containing the indices.
    nonzero_indices = np.nonzero(arr)[0] 
    if len(nonzero_indices) > 0:
        # Return the first index found
        return nonzero_indices[0]
    else:
        # Return -1 if no non-zero elements are found
        return -1 

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the left-shift transformation to the non-zero block in the input array.

    Args:
        input_grid: A 1D numpy array of integers representing the input sequence.

    Returns:
        A 1D numpy array of integers representing the transformed sequence.
    """
    
    # Convert numpy array to a list for easier element removal and appending
    # Work on a copy to avoid modifying the original input array if passed by reference elsewhere
    working_list = input_grid.tolist()
    
    # Find the index of the first non-zero element using the helper function
    first_nonzero_idx = find_first_nonzero_index(input_grid) 

    # Check if a non-zero block was found (index != -1) 
    # AND if it's not already at the beginning (index > 0)
    # This implies there is a preceding zero to remove.
    if first_nonzero_idx > 0:
        # Calculate the index of the zero immediately preceding the block
        preceding_zero_idx = first_nonzero_idx - 1
        
        # Remove the preceding zero element from the list
        # Note: list.pop() modifies the list in-place
        working_list.pop(preceding_zero_idx)
        
        # Append a zero to the end of the list to maintain the original length
        working_list.append(0)

    # If first_nonzero_idx is 0 or -1 (no non-zeros found, or block already at start), 
    # the working_list remains unchanged from the initial copy.
    
    # Convert the potentially modified list back to a numpy array 
    # Ensure the data type is the same as the input grid.
    output_grid = np.array(working_list, dtype=input_grid.dtype)

    # Return the transformed grid
    return output_grid
```