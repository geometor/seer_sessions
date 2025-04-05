```python
import numpy as np

"""
Transformation Rule: Given a sequence of digits as a 1D NumPy array, find the index 'i' of the first non-zero digit. 
If no non-zero digit exists (the sequence contains only zeros), return the sequence unchanged. 
Otherwise, create a new sequence of the same length where:
1. Digits before index 'i' remain the same.
2. The digit at index 'i' becomes 0.
3. Digits from index 'i' up to the second-to-last digit of the original sequence are shifted one position to the right, occupying indices 'i+1' through the end of the new sequence. The original last digit is effectively discarded.
"""

def find_first_non_zero_index(arr: np.ndarray) -> int:
    """
    Finds the index of the first non-zero element in a 1D numpy array.
    
    Args:
        arr: The input 1D NumPy array.

    Returns:
        The index (integer >= 0) of the first non-zero element. 
        Returns -1 if all elements are zero or the array is empty.
    """
    # np.nonzero returns a tuple of arrays, one for each dimension.
    # For a 1D array, we access the first element of the tuple ([0]).
    non_zero_indices = np.nonzero(arr)[0] 
    
    # Check if the resulting array of indices is non-empty
    if non_zero_indices.size > 0:
        # Return the first index found
        return non_zero_indices[0]
    else:
        # Indicate no non-zero element found
        return -1

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input numpy array sequence.

    Args:
      input_grid: A 1D NumPy array containing single digits.

    Returns:
      A 1D NumPy array containing the transformed sequence.
    """
    
    # Get the length of the input array
    n = input_grid.size
    
    # Handle empty input array case
    if n == 0:
        return np.copy(input_grid) # Return an empty array copy

    # Find the index of the first non-zero digit
    first_nz_index = find_first_non_zero_index(input_grid)

    # If all digits are zero (index is -1), return a copy of the original array
    if first_nz_index == -1:
        return np.copy(input_grid)

    # --- Apply the transformation ---
    
    # Create the output array, initialized as a copy of the input for simplicity
    # Alternatively, could initialize with zeros: output_grid = np.zeros_like(input_grid)
    # and then copy the prefix: output_grid[:first_nz_index] = input_grid[:first_nz_index]
    output_grid = np.copy(input_grid) 

    # 1. Elements before index 'i' are already correct due to the initial copy.
    #    (Or would be copied if starting with zeros).
    
    # 2. Set the element at the first non-zero index to 0
    output_grid[first_nz_index] = 0

    # 3. Shift elements from the original input (starting at the first non-zero index 'i'
    #    up to, but not including, the last element) into the output grid starting 
    #    at index 'i+1'.
    # Check if there are elements to shift (i.e., if 'i' is not the last index)
    if first_nz_index < n - 1:
        # Source slice: input_grid[first_nz_index] to input_grid[n-2]
        source_slice = input_grid[first_nz_index : n - 1]
        # Destination slice: output_grid[first_nz_index + 1] to output_grid[n-1]
        output_grid[first_nz_index + 1 : n] = source_slice

    # If first_nz_index == n - 1 (last element was the first non-zero),
    # the slices in step 3 become empty, correctly handling the edge case.
    # output_grid[n:n] = input_grid[n-1:n-1] which does nothing.

    return output_grid
```