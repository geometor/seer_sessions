"""
Transforms an input NumPy array of digits based on the following rule:
1. Identify all non-zero digits in the input array.
2. Count the frequency of each unique non-zero digit.
3. Determine the non-zero digit with the highest frequency (the "dominant non-zero digit"). If no non-zero digits exist, the original array is returned.
4. Create a new output array.
5. For each element in the input array:
    a. If the element is 0, keep it as 0 in the output array.
    b. If the element is non-zero, replace it with the dominant non-zero digit in the output array.
The resulting array is the output.
"""

import numpy as np
from collections import Counter

def find_most_frequent_non_zero(input_array):
    """
    Finds the most frequent non-zero digit in a NumPy array.
    Returns None if no non-zero digits are present.
    """
    # Filter out zero elements
    non_zeros = input_array[input_array != 0]
    
    # Check if there are any non-zero elements
    if non_zeros.size == 0:
        return None # No non-zero digits found
    
    # Count frequencies of non-zero elements
    counts = Counter(non_zeros)
    
    # Find the element with the maximum count
    # counts.most_common(1) returns a list like [(element, count)]
    dominant_digit = counts.most_common(1)[0][0] 
    
    return dominant_digit

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input numpy array (grid).
    
    Args:
        input_grid: A 1D NumPy array of single-digit integers.

    Returns:
        A 1D NumPy array representing the transformed grid.
    """
    
    # Find the dominant non-zero digit in the input grid
    dominant_digit = find_most_frequent_non_zero(input_grid)

    # If there are no non-zero digits (dominant_digit is None), 
    # return the original grid as no transformation is needed.
    if dominant_digit is None:
        return input_grid # Return original grid

    # Create the output grid using np.where for conditional replacement.
    # Condition: input_grid == 0
    # If True (element is 0), keep it as 0.
    # If False (element is non-zero), replace it with dominant_digit.
    output_grid = np.where(input_grid == 0, 0, dominant_digit)

    # Return the transformed grid
    return output_grid