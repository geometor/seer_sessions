import numpy as np
import math # Although math is not used, it's available per instructions

"""
Reorders the elements of an input NumPy array (treated as a 1D sequence)
such that all zero elements are moved to the beginning of the sequence,
followed by all non-zero elements. The relative order of the non-zero
elements is preserved from the original input array.
"""

def partition_by_zero(sequence):
    """
    Separates elements of a sequence into zeros and non-zeros, preserving
    the relative order of non-zeros.

    Args:
        sequence: A list or 1D NumPy array of numbers.

    Returns:
        A tuple containing two lists: (list_of_zeros, list_of_non_zeros).
    """
    # Use list comprehensions to efficiently filter elements while preserving order
    zeros_list = [num for num in sequence if num == 0]
    non_zeros_list = [num for num in sequence if num != 0]
    
    return zeros_list, non_zeros_list

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the zero-partitioning transformation to the input NumPy array.

    Args:
        input_grid: A 1D NumPy array containing integers.

    Returns:
        A 1D NumPy array containing the reordered integers.
    """

    # 1. Treat the input NumPy array as a sequence (it's expected to be 1D based on examples)
    #    Convert to list to easily use list comprehensions if preferred, or operate directly
    #    Here, we'll use the helper function which works on sequences.
    input_sequence = input_grid.tolist() # Convert to list for the helper

    # 2. Partition the sequence into zeros and non-zeros using the helper function
    #    This helper ensures the relative order of non-zeros is maintained.
    zeros_list, non_zeros_list = partition_by_zero(input_sequence)

    # 3. Concatenate the lists: zeros first, then non-zeros
    #    This creates the desired ordered sequence as a Python list.
    ordered_list = zeros_list + non_zeros_list

    # 4. Convert the ordered list back into a NumPy array
    #    Ensure the data type matches the original input grid's dtype.
    output_grid = np.array(ordered_list, dtype=input_grid.dtype)

    # 5. Return the resulting NumPy array
    return output_grid