```python
"""
Transforms a 1D sequence of digits represented as a NumPy array. 
It identifies the first and last non-zero elements in the sequence. 
All elements located strictly between these first and last non-zero elements are 
changed to 0. Elements outside this range (leading/trailing zeros) and the 
first/last non-zero elements themselves remain unchanged. If the sequence 
contains fewer than two non-zero elements, it is returned unmodified.
"""

import numpy as np
# Note: math library is not required for this implementation.

def find_non_zero_indices(arr: np.ndarray) -> np.ndarray:
  """
  Finds the indices of all non-zero elements in a 1D NumPy array.

  Args:
    arr: A 1D NumPy array of numbers.

  Returns:
    A 1D NumPy array containing the indices of non-zero elements. 
    Returns an empty array if no non-zero elements are found.
  """
  # np.where returns a tuple of arrays, one for each dimension.
  # Since the input is 1D, we access the first element of the tuple.
  indices = np.where(arr != 0)[0]
  return indices

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input 1D NumPy array.

    Args:
      input_grid: A 1D NumPy array of integer digits.

    Returns:
      A 1D NumPy array representing the transformed sequence.
    """
    # 1. Identify Non-Zero Indices: Find indices of all non-zero digits.
    non_zero_indices = find_non_zero_indices(input_grid)

    # 2. Check Boundary Condition: If fewer than two non-zero digits exist,
    #    no "inner" digits need modification. Return a copy of the original.
    if non_zero_indices.size < 2:
        # Return a copy to prevent modification of the original input array outside the function
        return input_grid.copy() 

    # 3. Determine Boundaries: Find the first (min) and last (max) non-zero indices.
    first_nz_idx = np.min(non_zero_indices)
    last_nz_idx = np.max(non_zero_indices)

    # 4. Create Output Sequence: Initialize output_grid as a copy of the input.
    output_grid = input_grid.copy()

    # 5. Modify Inner Digits: 
    #    Select the slice strictly between the first and last non-zero indices.
    #    NumPy slice `start:end` includes `start` but excludes `end`.
    #    So `first_nz_idx + 1` starts *after* the first non-zero index.
    #    `: last_nz_idx` ends *before* the last non-zero index.
    #    Assign 0 to all elements within this slice.
    output_grid[first_nz_idx + 1 : last_nz_idx] = 0

    # 6. Return Output: Return the modified grid.
    return output_grid
```