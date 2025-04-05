```python
import numpy as np
import copy

"""
Identifies the single non-zero digit ('fill_value') present exactly twice in the input 1D NumPy array. 
Fills the array elements strictly between the first and second occurrences of the 'fill_value' with the 'fill_value' itself. 
Elements outside this range, including the original positions of the 'fill_value', remain unchanged.
"""

def find_non_zero_value(grid: np.ndarray):
    """Finds the first non-zero value encountered in the 1D array."""
    # Get all non-zero elements
    non_zero_elements = grid[grid != 0]
    # If there are any non-zero elements, return the first one
    if non_zero_elements.size > 0:
        return non_zero_elements[0]
    # Otherwise, return None (or 0, though None is clearer for 'not found')
    return None 

def find_value_indices(grid: np.ndarray, value):
    """Finds all indices where a specific value occurs in the 1D array."""
    # np.where returns a tuple of arrays (one for each dimension); for 1D, we need the first element
    indices = np.where(grid == value)[0]
    return indices

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input NumPy array by filling elements between the two occurrences 
    of a unique non-zero digit with that digit.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the transformation applied.
    """
    # 1. Create a modifiable copy of the input sequence (NumPy array).
    output_grid = np.copy(input_grid)

    # 2. Identify the unique non-zero integer (fill_value).
    fill_value = find_non_zero_value(output_grid)

    # 3. If no non-zero value exists, return the original sequence copy.
    if fill_value is None:
        return output_grid

    # 4. Find all indices where the fill_value occurs.
    indices = find_value_indices(output_grid, fill_value)

    # 5. Check if exactly two occurrences were found (as per problem description).
    if indices.size == 2:
        # 6. Get the first (idx1) and second (idx2) indices.
        # NumPy's where guarantees sorted indices for 1D arrays.
        idx1 = indices[0]
        idx2 = indices[1]

        # 7. Check if idx1 < idx2 (should always be true if size is 2).
        # Fill the segment strictly between idx1 and idx2 using slicing.
        if idx1 < idx2:
            # The slice output_grid[idx1 + 1 : idx2] selects elements from index idx1+1 up to (not including) idx2.
            output_grid[idx1 + 1 : idx2] = fill_value

    # 8. Return the modified output grid.
    return output_grid
```