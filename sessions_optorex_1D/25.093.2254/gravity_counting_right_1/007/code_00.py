"""
Transforms a 1-dimensional NumPy array of integers into a space-separated 
binary string. The transformation counts the non-zero elements in the input 
array. The output string starts with that many '1's, followed by '0's to 
match the original array length, with elements separated by spaces.
"""

import numpy as np
import math # Although math isn't used, included as per template instruction

# No specific helper functions needed beyond numpy's capabilities for this logic

def transform(input_array: np.ndarray) -> str:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_array: A 1D NumPy array of integers.

    Returns:
        A string containing space-separated binary digits ('1' or '0') 
        based on the transformation rule.
    """
    # Ensure input is a NumPy array (basic check, although type hint exists)
    if not isinstance(input_array, np.ndarray):
        raise TypeError(f"Input must be a NumPy array, got {type(input_array)}")
        
    # 1. Determine the total number of elements (L)
    total_length = input_array.size

    # 2. Count non-zero elements (N) using numpy's efficient function
    non_zero_count = np.count_nonzero(input_array)

    # 3. Create the list of '1's based on the non-zero count
    output_ones = ['1'] * non_zero_count

    # 4. Create the list of '0's for the remaining length
    output_zeros = ['0'] * (total_length - non_zero_count)

    # 5. Combine the lists to form the final sequence
    output_list = output_ones + output_zeros

    # 6. Join the elements with spaces to form the final output string
    output_str = " ".join(output_list)

    # 7. Return the result
    return output_str