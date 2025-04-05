import numpy as np
import math
import collections

"""
Transforms an input sequence (likely a 1D NumPy array or 2D with one row) 
based on the following rule:
1. Ensure the input is treated as a 1D sequence.
2. Create a mutable copy of the 1D input sequence for the output.
3. Identify all unique non-zero integer values present in the original 1D input sequence.
4. For each unique non-zero value:
   a. Find the index of its first occurrence in the original input sequence.
   b. Find the index of its last occurrence in the original input sequence.
   c. Modify the output sequence copy: Set all elements from the first index to the last index (inclusive) to this non-zero value.
5. Return the modified output sequence (as a 1D NumPy array).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the sequence filling transformation.

    Args:
        input_grid: A NumPy array representing the input sequence (potentially 1D or 2D with one row).

    Returns:
        A 1D NumPy array representing the transformed output sequence.
    """
    # 1. Ensure the input is treated as a 1D sequence.
    # Flatten the input array to handle both 1D and 2D (1 row) cases.
    input_sequence = input_grid.flatten()

    # 2. Create a mutable copy for the output.
    output_sequence = np.copy(input_sequence)

    # 3. Identify unique non-zero values in the original input sequence.
    # np.unique returns sorted unique elements.
    unique_values = np.unique(input_sequence)
    non_zero_values = unique_values[unique_values != 0]

    # 4. For each unique non-zero value:
    for value in non_zero_values:
        # a. & b. Find first and last indices in the original input sequence.
        # np.where returns a tuple of arrays, one for each dimension. 
        # Since input_sequence is 1D, we take the first element of the tuple.
        indices = np.where(input_sequence == value)[0]
        
        # Check if the value was actually found (it should be)
        if indices.size > 0:
            min_index = np.min(indices)
            max_index = np.max(indices)
            
            # c. Modify the output sequence copy in the identified range.
            # Use array slicing for efficient modification.
            # The slice upper bound is exclusive, so add 1 to max_index.
            output_sequence[min_index : max_index + 1] = value
                
    # 5. Return the fully modified output sequence.
    # Ensure it's returned as a 1D array as per visual examples.
    return output_sequence