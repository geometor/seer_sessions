"""
Transforms an input 1D NumPy array of integers based on the following rules:
1. Identify all non-zero elements in the input array.
2. If non-zero elements exist, find the non-zero element that appears most frequently (the dominant_non_zero_number).
3. Create an output array where:
    a. Elements that were 0 in the input remain 0.
    b. Elements that were non-zero in the input are replaced by the dominant_non_zero_number.
4. If the input array contains only zeros, the output array is an identical copy.
"""

import numpy as np
from collections import Counter

def find_dominant_non_zero(input_array: np.ndarray):
    """
    Finds the most frequent non-zero number in a NumPy array.

    Args:
        input_array: A 1D NumPy array of integers.

    Returns:
        The most frequent non-zero integer, or None if no non-zero numbers are present.
    """
    # Filter out zero elements using NumPy boolean indexing
    non_zeros = input_array[input_array != 0]

    # If no non-zero numbers exist, return None
    if non_zeros.size == 0:
        return None

    # Count occurrences of each non-zero number
    # Counter works directly on NumPy arrays (or lists derived from them)
    counts = Counter(non_zeros)

    # Find the number with the highest frequency
    # most_common(1) returns a list like [(element, count)]
    dominant_non_zero_number = counts.most_common(1)[0][0]
    
    # Ensure the return type is a standard Python int if necessary, 
    # though numpy types often work fine. Let's keep it as is for now.
    return dominant_non_zero_number 

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.
    Replaces non-zero elements with the most frequent non-zero element,
    keeping zero elements as they are.

    Args:
        input_grid: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array with the transformation applied.
    """
    # Find the dominant non-zero number in the input array
    dominant_num = find_dominant_non_zero(input_grid)

    # Handle the case where the input array contains only zeros
    if dominant_num is None:
        # Return an identical copy of the input array
        output_grid = np.copy(input_grid)
    else:
        # Create the output array using np.where
        # Condition: input_grid == 0
        # If True (element is 0), keep the value 0
        # If False (element is non-zero), replace with dominant_num
        output_grid = np.where(input_grid == 0, 0, dominant_num)

    return output_grid