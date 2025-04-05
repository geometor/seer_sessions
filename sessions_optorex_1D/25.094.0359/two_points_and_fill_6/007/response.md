```python
"""
Transforms a 1D NumPy array by filling the segment between the first and last 
occurrence of each non-zero digit with that digit's value.

1. Prepare Output: Create an exact, modifiable copy of the input sequence. 
   This copy will store the results of the transformation.
2. Find Unique Markers: Identify all the distinct non-zero integer values 
   present in the *original* input sequence.
3. Iterate Through Markers: Process each unique non-zero value (N) identified 
   in the previous step one by one. For each N:
    a. Locate All Occurrences: Find every index position where N appears in 
       the *original* input sequence.
    b. Check Minimum Occurrences: Verify if N was found at two or more distinct 
       index positions. If not, proceed to the next unique non-zero value.
    c. Determine Boundaries: If N occurred at least twice, identify the index 
       of its very first appearance (first_index) and the index of its very 
       last appearance (last_index).
    d. Check for Gap: Determine if there is a gap between these boundaries by 
       checking if last_index is strictly greater than first_index + 1.
    e. Fill the Gap: If a gap exists (i.e., last_index > first_index + 1), 
       modify the *output sequence copy*: For every index position i starting 
       from first_index + 1 up to, but not including, last_index, set the 
       value at position i in the output sequence to N.
4. Return Result: Once all unique non-zero values from the original input 
   have been processed according to step 3, the transformation is complete. 
   Return the final modified output sequence.
"""

import numpy as np

# Helper function to find indices (could use np.where directly, but encapsulates logic)
def find_indices(arr, value):
    """Finds all indices of a specific value in a NumPy array."""
    return np.where(arr == value)[0]

def transform(input_grid: np.ndarray) -> np.ndarray:
    # 1. Prepare Output: Create a modifiable copy of the input sequence.
    output_grid = np.copy(input_grid)

    # 2. Find Unique Markers: Identify distinct non-zero values in the original input.
    # Filter out zero, then find unique values
    non_zero_elements = input_grid[input_grid != 0]
    unique_non_zeros = np.unique(non_zero_elements)

    # 3. Iterate Through Markers: Process each unique non-zero value.
    for value_to_fill in unique_non_zeros:
        
        # a. Locate All Occurrences: Find indices in the *original* input.
        indices = find_indices(input_grid, value_to_fill)
        
        # b. Check Minimum Occurrences: Need at least two occurrences.
        if len(indices) > 1:
            # c. Determine Boundaries: Find the first and last index.
            first_index = np.min(indices)
            last_index = np.max(indices)
            
            # d. Check for Gap: Ensure there's space between first and last.
            if last_index > first_index + 1: 
                 # e. Fill the Gap: Modify the *output* sequence.
                 # Slice is from index *after* first up to (but not including) last.
                 output_grid[first_index + 1 : last_index] = value_to_fill

    # 4. Return Result: Return the modified sequence.
    return output_grid
```