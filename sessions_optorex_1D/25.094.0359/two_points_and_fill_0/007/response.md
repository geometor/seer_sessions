```python
"""
Transforms a 1D NumPy array by identifying the unique non-zero integer value, 
finding the minimum and maximum indices of its occurrences, and filling the segment 
of the array between these minimum and maximum indices (inclusive) with that 
non-zero value. If the non-zero value appears less than twice, or if there isn't 
exactly one unique non-zero value, the original array is returned unchanged.
"""

import numpy as np

def find_unique_non_zero_and_indices(input_grid: np.ndarray):
    """
    Finds the unique non-zero value and all its indices in the grid.

    Args:
        input_grid: The input 1D NumPy array.

    Returns:
        A tuple (non_zero_value, indices_array) if exactly one unique non-zero 
        value exists and it appears at least once. Otherwise, returns (None, None).
        indices_array is a 1D NumPy array of indices.
    """
    # Find unique values and filter out zero
    unique_values = np.unique(input_grid)
    non_zero_values = unique_values[unique_values != 0]

    # Check if exactly one unique non-zero value exists
    if len(non_zero_values) == 1:
        non_zero_val = non_zero_values[0]
        # Find all indices of this non-zero value
        indices = np.where(input_grid == non_zero_val)[0]
        # Check if it appears at least once
        if len(indices) > 0:
            return non_zero_val, indices
        else:
             # Should not happen if non_zero_values had length 1, but safety check
             return None, None
    else:
        # If zero or more than one unique non-zero value found
        return None, None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the fill transformation based on the identified non-zero value segment.
    
    Args:
        input_grid: A 1D NumPy array containing integers.
                    Expected to contain mostly zeros and occurrences of a single 
                    non-zero integer value.

    Returns:
        The transformed 1D NumPy array. Returns a copy of the input if 
        transformation conditions are not met (e.g., less than two occurrences 
        of the non-zero value).
    """
    
    # 1. & 2. Identify the unique non-zero value and find all its indices.
    non_zero_val, indices = find_unique_non_zero_and_indices(input_grid)

    # Initialize output_grid as a copy of the input
    # This handles the case where conditions are not met - the copy is returned.
    output_grid = np.copy(input_grid)

    # 3. & 4. Check if a unique non-zero value was found and occurred at least twice.
    if non_zero_val is not None and indices is not None and len(indices) >= 2:
        # 5. Determine the start (min index) and end (max index) of the segment.
        start_index = np.min(indices)
        end_index = np.max(indices)

        # 6. Create a copy (already done).
        # 7. & 8. Fill the segment in the output grid with the non-zero value.
        # NumPy slicing [start:end+1] includes the element at end_index.
        output_grid[start_index : end_index + 1] = non_zero_val
    
    # 9. Return the potentially modified sequence.
    return output_grid
```