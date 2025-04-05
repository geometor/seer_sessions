```python
"""
Transforms a 1D NumPy array by filling the segment between the first and last 
occurrence of each non-zero digit with that digit.

1. Accept the input, which is a one-dimensional NumPy array of integers.
2. Create a mutable copy of the input array; this copy will serve as the output array.
3. Identify all the unique non-zero integer values present in the original input array.
4. For each unique non-zero value (N) identified:
    a. Find all the indices where N appears in the original input array.
    b. Check if N appears at more than one index.
    c. If N appears more than once:
        i. Determine the smallest index (first_index) among these occurrences.
        ii. Determine the largest index (last_index) among these occurrences.
        iii. Using NumPy array slicing, select the portion of the *output* array 
             starting from the index immediately *after* first_index (first_index + 1) 
             up to, but not including, last_index.
        iv. Assign the value N to all elements within this selected slice of the 
             *output* array.
5. After processing all unique non-zero values, return the modified output array.
"""

import numpy as np

# Helper function to find indices (though np.where is standard)
# def find_indices(arr, value):
#     """Finds all indices of a specific value in a NumPy array."""
#     return np.where(arr == value)[0]

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the fill transformation to the input NumPy array.
    """
    # 2. Create a mutable copy of the input array
    output_grid = np.copy(input_grid)

    # 3. Identify unique non-zero values in the original input array
    # Filter out zero, then find unique values
    non_zero_elements = input_grid[input_grid != 0]
    unique_non_zeros = np.unique(non_zero_elements)

    # 4. Iterate through each unique non-zero value
    for value_to_fill in unique_non_zeros:
        
        # a. Find all indices where this value occurs in the *original* input_grid
        indices = np.where(input_grid == value_to_fill)[0]
        
        # b. Check if the value occurs more than once
        if len(indices) > 1:
            # c.i. Determine the first index (minimum)
            first_index = np.min(indices)
            # c.ii. Determine the last index (maximum)
            last_index = np.max(indices)
            
            # c.iii & c.iv. Fill the range in the output_grid
            # Slice is from index after first up to (not including) last
            if last_index > first_index + 1: # Ensure there's a gap to fill
                 output_grid[first_index + 1 : last_index] = value_to_fill

    # 5. Return the modified output grid
    return output_grid
```