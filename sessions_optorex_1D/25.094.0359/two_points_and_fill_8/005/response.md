```python
"""
Transforms an input sequence (numpy array) of integers by identifying the unique non-zero digit (d), finding its first (start_index) and last (end_index) occurrences, and creating an output sequence of the same length where the elements from start_index to end_index (inclusive) are set to d, and all other elements are zero. The output is formatted as a space-separated string.
"""

import numpy as np

def _find_non_zero_info(arr):
    """
    Helper function to find the non-zero digit and its first/last indices.
    
    Args:
        arr (np.ndarray): The input numpy array of integers.

    Returns:
        tuple: (non_zero_digit, start_index, end_index)
               Returns (0, -1, -1) if fewer than two non-zero digits are found.
               Assumes exactly two identical non-zero digits based on problem description.
    """
    # 1. Identify all indices in `input_sequence` where the element is not zero.
    non_zero_indices = np.where(arr != 0)[0]
    
    # 2. Check if at least two non-zero indices are found (as expected from examples).
    if len(non_zero_indices) < 1: # Allow for single non-zero if needed, but examples show 2. If exactly 1, start==end. If 0, return defaults.
        return 0, -1, -1 
        
    # 3. Determine the `non_zero_digit` using the first non-zero index.
    start_index = non_zero_indices[0]
    non_zero_digit = arr[start_index]
    
    # 4. Determine the `start_index` (minimum) and `end_index` (maximum).
    # If only one non-zero element, start_index == end_index.
    end_index = non_zero_indices[-1] 
    
    return non_zero_digit, start_index, end_index

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the transformation rule to the input numpy array.

    Args:
        input_grid (np.ndarray): A 1D numpy array of integers representing the input sequence.

    Returns:
        str: A space-separated string representing the transformed sequence.
    """
    # 1. Accept the input as a numpy array `input_grid`. (Handled by function signature)
    
    # 2. Find the non-zero digit, start index, and end index.
    non_zero_digit, start_index, end_index = _find_non_zero_info(input_grid)
    
    # 3. Get the length of the input sequence.
    n = len(input_grid)
    
    # 4. Create a new sequence, `output_grid`, of the same length, initially filled with zeros.
    output_grid = np.zeros(n, dtype=int)

    # 5. Fill the elements of `output_grid` from `start_index` to `end_index` (inclusive)
    #    with the `non_zero_digit`, only if valid indices were found.
    if start_index != -1: # Check if non-zero elements were found
        # Use numpy slicing for efficient filling
        output_grid[start_index : end_index + 1] = non_zero_digit
        
    # 6. Convert the `output_grid` (numpy array) into a space-separated string.
    output_str = " ".join(map(str, output_grid))
    
    # 7. Return the resulting string.
    return output_str
```