"""
Transforms an input 2D grid of single-digit integers based on the horizontal
contiguity of the dominant non-zero digit within each row.

1.  The transformation is applied independently to each row of the input grid.
2.  Within a row:
    a.  Identify the single non-zero digit present (the "dominant digit"). 
        If the row contains only zeros, the output row is all zeros.
    b.  Find all contiguous horizontal blocks (runs) of this dominant digit.
    c.  Create an output row initialized with zeros, having the same length.
    d.  Copy the dominant digit into the output row only for those positions 
        that belong to an input block of length 2 or greater.
    e.  Isolated occurrences (blocks of length 1) of the dominant digit are 
        effectively replaced by zero in the output row.
    f.  Zeros in the input row are preserved as zeros in the output row.
3.  Assemble the processed rows into the final output grid.
"""

import numpy as np
from collections import Counter

def find_dominant_digit(arr_1d):
    """
    Finds the single non-zero digit present in a 1D array.
    Returns the dominant digit, or 0 if none exists or if only zeros are present.
    Handles the (unseen in examples) case of multiple distinct non-zero digits
    by returning the most frequent one, or the smallest if frequencies are equal.

    Args:
        arr_1d (np.ndarray): The input 1D NumPy array of integers.

    Returns:
        int: The dominant non-zero digit, or 0.
    """
    # Filter out zeros
    non_zeros = arr_1d[arr_1d != 0]

    # Handle case where the array contains only zeros
    if non_zeros.size == 0:
        return 0

    # Count occurrences of each non-zero digit
    counts = Counter(non_zeros)

    # If only one type of non-zero digit exists
    if len(counts) == 1:
        return list(counts.keys())[0]

    # If multiple non-zero digits exist (handling robustness)
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
    # Initialize output_grid with the same shape as input, filled with zeros
    output_grid = np.zeros_like(input_grid)
    num_rows, num_cols = input_grid.shape

    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row
        input_row = input_grid[r, :]

        # Identify the dominant non-zero digit for this row
        dominant_digit = find_dominant_digit(input_row)

        # If the row is all zeros or no single dominant digit can be determined based on rules,
        # the output row remains zeros (already initialized), so skip to the next row.
        if dominant_digit == 0:
            continue

        # Iterate through the columns of the current row to find blocks
        c = 0
        while c < num_cols:
            # Check if the current element is the dominant digit
            if input_row[c] == dominant_digit:
                # Found the start of a potential block
                block_start_col = c
                j = c
                # Find the end of the contiguous horizontal block of the dominant digit
                while j < num_cols and input_row[j] == dominant_digit:
                    j += 1
                block_end_col = j - 1 # Inclusive end column index of the block
                block_length = block_end_col - block_start_col + 1

                # Check if the block length meets the criterion (>= 2)
                if block_length >= 2:
                    # If yes, assign the dominant digit to the corresponding slice in the output grid row
                    output_grid[r, block_start_col : block_end_col + 1] = dominant_digit

                # Move the main column index 'c' past the processed block
                c = j
            else:
                # If the current element is not the dominant digit, just move to the next column
                c += 1
                
    # Return the transformed grid
    return output_grid