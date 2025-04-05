import numpy as np
from collections import Counter

"""
Transforms an input 1D NumPy array of single-digit integers based on the 
contiguity of the dominant non-zero digit.

1. Identifies the single dominant non-zero digit in the input array. If 
   only zeros are present, returns an array of zeros.
2. Finds all contiguous blocks (runs) of this dominant digit within the input.
3. Creates an output array of the same shape as the input, initialized with zeros.
4. Copies the dominant digit into the output array only for those positions 
   that belong to an input block of length 2 or greater.
5. Isolated occurrences (blocks of length 1) of the dominant digit are 
   effectively replaced by zero in the output.
6. Zeros in the input are preserved as zeros in the output (due to 
   initialization and selective copying).
"""

def find_dominant_digit(arr):
    """
    Finds the single non-zero digit present in the array.
    Returns the dominant digit, or 0 if none exists or if only zeros are present.
    Handles the (unseen in examples) case of multiple distinct non-zero digits
    by returning the most frequent one, or the smallest if frequencies are equal.

    Args:
        arr (np.ndarray): The input 1D NumPy array of integers.

    Returns:
        int: The dominant non-zero digit, or 0.
    """
    # Filter out zeros
    non_zeros = arr[arr != 0]

    # Handle case where the array contains only zeros
    if non_zeros.size == 0:
        return 0

    # Count occurrences of each non-zero digit
    counts = Counter(non_zeros)

    # If only one type of non-zero digit exists
    if len(counts) == 1:
        return list(counts.keys())[0]

    # If multiple non-zero digits exist (handling robustness, though not seen in examples)
    # Find the highest frequency
    max_freq = 0
    for digit in counts:
        if counts[digit] > max_freq:
            max_freq = counts[digit]

    # Get all digits with the highest frequency
    most_frequent_digits = [digit for digit in counts if counts[digit] == max_freq]

    # Return the smallest digit among the most frequent ones
    return min(most_frequent_digits)


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input NumPy array.

    Args:
        input_grid (np.ndarray): A 1D NumPy array of single-digit integers.

    Returns:
        np.ndarray: The transformed 1D NumPy array.
    """
    # Ensure input is a NumPy array (it should be based on the environment)
    # Handle potential non-1D arrays gracefully if necessary, though examples are 1D
    if input_grid.ndim != 1:
        # This case isn't expected based on examples, but provides robustness
        # For now, raise an error or return input, depending on desired behavior
        # Raising an error is safer if the assumption is strictly 1D input.
        raise ValueError("Input grid must be a 1D array")

    input_list = input_grid # Use the numpy array directly
    n = len(input_list)

    # Identify the dominant non-zero digit
    dominant_digit = find_dominant_digit(input_list)

    # If there's no dominant digit (input is all zeros), return an array of zeros
    if dominant_digit == 0:
        return np.zeros_like(input_list)

    # Initialize the output array with zeros, same shape as input
    output_grid = np.zeros_like(input_list)

    # Iterate through the input array to find blocks of the dominant digit
    i = 0
    while i < n:
        # Check if the current element is the dominant digit
        if input_list[i] == dominant_digit:
            # Found the start of a potential block
            block_start = i
            j = i
            # Find the end of the contiguous block of the dominant digit
            while j < n and input_list[j] == dominant_digit:
                j += 1
            block_end = j - 1 # Inclusive end index of the block
            block_length = block_end - block_start + 1

            # Check if the block length meets the criterion (>= 2)
            if block_length >= 2:
                # If yes, assign the dominant digit to the corresponding slice in the output array
                output_grid[block_start:block_end + 1] = dominant_digit

            # Move the main index 'i' past the processed block
            i = j
        else:
            # If the current element is not the dominant digit, just move to the next element
            i += 1

    return output_grid