```python
"""
Transforms a 1D NumPy array by filling the segment between the first and last 
occurrence of each non-zero digit with that digit.

1. Create a copy of the input sequence; this copy will be modified to become 
   the output sequence.
2. Identify all the unique non-zero numbers present in the original input sequence.
3. For each unique non-zero number N identified:
    a. Find all the positions (indices) where N appears in the *original* 
       input sequence.
    b. If N appears at two or more distinct positions:
        i. Determine the index of its very first appearance (first_index).
        ii. Determine the index of its very last appearance (last_index).
        iii. If there are any positions strictly between first_index and 
             last_index (i.e., if last_index is greater than first_index + 1):
            iv. Change the value of every element in the *output* sequence 
                located at indices from first_index + 1 up to (but not 
                including) last_index to the value N.
4. After performing this check and potential fill operation for all unique 
   non-zero numbers, return the modified output sequence.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """Applies the fill transformation to the input NumPy array."""
    
    # 1. Create a copy of the input sequence
    output_grid = np.copy(input_grid)

    # 2. Identify unique non-zero numbers in the original input array
    # Filter out zero, then find unique values
    non_zero_elements = input_grid[input_grid != 0]
    unique_non_zeros = np.unique(non_zero_elements)

    # 3. Iterate through each unique non-zero number
    for value_to_fill in unique_non_zeros:
        
        # a. Find all indices where this value occurs in the *original* input_grid
        indices = np.where(input_grid == value_to_fill)[0]
        
        # b. Check if the value occurs more than once
        if len(indices) > 1:
            # i. Determine the first index (minimum)
            first_index = np.min(indices)
            # ii. Determine the last index (maximum)
            last_index = np.max(indices)
            
            # iii. Check if there is a gap between the first and last occurrences
            if last_index > first_index + 1: 
                 # iv. Fill the range in the output_grid
                 # Slice is from index *after* first up to (but not including) last
                 output_grid[first_index + 1 : last_index] = value_to_fill

    # 4. Return the modified output grid
    return output_grid
```