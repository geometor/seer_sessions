import numpy as np
from collections import Counter

"""
Transforms a 2D grid of digits by swapping pairs of non-zero digits based on their frequency.

The transformation logic identifies the four most frequent non-zero digits in the input grid.
The most frequent digit is swapped with the second most frequent digit.
The third most frequent digit is swapped with the fourth most frequent digit.
If there are fewer than four distinct non-zero digits, swaps are performed only for existing pairs (e.g., if only two non-zero digits exist, they swap; if three exist, only the top two swap).
The digit '0' always remains unchanged.
Digits that are not part of the determined swap pairs also remain unchanged.
Ties in frequency are broken by the numerical value of the digit (lower value first).
"""

def transform(input_grid):
    """
    Applies a frequency-based digit swapping transformation to the input grid.

    Args:
        input_grid (list of list of int): A 2D list representing the input grid of digits.

    Returns:
        list of list of int: A 2D list representing the transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # Flatten the grid and count frequencies of non-zero digits
    flat_grid = grid.flatten()
    non_zero_digits = [d for d in flat_grid if d != 0]
    
    if not non_zero_digits:
        # If no non-zero digits, return the original grid
        return input_grid

    # Count frequency of each non-zero digit
    digit_counts = Counter(non_zero_digits)

    # Sort distinct non-zero digits by frequency (descending) and then by digit value (ascending for ties)
    # Items are (digit, count)
    sorted_digits = sorted(digit_counts.items(), key=lambda item: (-item[1], item[0]))

    # Initialize the swap map with 0 mapping to 0
    swap_map = {0: 0}
    # Add all unique non-zero digits initially mapping to themselves
    for digit in digit_counts.keys():
        swap_map[digit] = digit

    # Determine swap pairs based on sorted frequency
    num_distinct_digits = len(sorted_digits)

    # Pair 1: Swap the top two most frequent digits (if at least two exist)
    if num_distinct_digits >= 2:
        digit1 = sorted_digits[0][0]
        digit2 = sorted_digits[1][0]
        swap_map[digit1] = digit2
        swap_map[digit2] = digit1

    # Pair 2: Swap the third and fourth most frequent digits (if at least four exist)
    if num_distinct_digits >= 4:
        digit3 = sorted_digits[2][0]
        digit4 = sorted_digits[3][0]
        swap_map[digit3] = digit4
        swap_map[digit4] = digit3

    # Initialize the output grid with the same shape as the input
    output_grid_np = np.zeros_like(grid)

    # Apply the transformation using the swap map
    for r in range(rows):
        for c in range(cols):
            input_digit = grid[r, c]
            # Use the swap map to find the output digit. 
            # If a digit wasn't in the non_zero counts (e.g., appeared 0 times)
            # or wasn't part of a swap pair, it defaults to itself via the initial map setup.
            output_grid_np[r, c] = swap_map.get(input_digit, input_digit) 

    # Convert the result back to a list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid
