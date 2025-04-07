"""
Transforms an input grid by identifying the most frequent non-zero number within it 
and replacing all other non-zero numbers with this most frequent number. 
Zeroes remain unchanged.
"""

import numpy as np
from collections import Counter

def _count_non_zero_frequencies(grid):
    """Counts the frequency of each non-zero number in the grid."""
    # Flatten the grid to easily iterate through all elements
    flat_grid = grid.flatten()
    # Filter out zeros
    non_zeros = [num for num in flat_grid if num != 0]
    # Count frequencies using Counter
    if not non_zeros:
        return None # Return None if there are no non-zero numbers
    return Counter(non_zeros)

def _find_most_frequent_number(freq_map):
    """Finds the number with the highest frequency in the frequency map."""
    if not freq_map:
        return None # No non-zero numbers found
    # Find the element with the highest count
    # most_common(1) returns a list of tuples [(element, count)]
    most_common_item = freq_map.most_common(1)
    if not most_common_item:
         return None # Should not happen if freq_map is not empty, but safe check
    return most_common_item[0][0]

def transform(input_grid):
    """
    Applies the transformation rule: replaces all non-zero elements with the
    most frequent non-zero element found in the input grid.
    """
    # Convert input to a NumPy array for easier manipulation
    input_np = np.array(input_grid)
    
    # 1. Count the frequency of each unique non-zero number
    freq_map = _count_non_zero_frequencies(input_np)

    # Handle the case where there are no non-zero numbers
    if freq_map is None:
        return input_grid # Return the original grid if no non-zeros

    # 2. Determine the most frequent non-zero number (target number)
    target_number = _find_most_frequent_number(freq_map)

    # Handle edge case again (shouldn't be needed if freq_map check is done)
    if target_number is None:
         return input_grid

    # 3. Create the output grid, initialized as a copy of the input
    #    Or initialize with zeros and fill non-zeros
    output_grid = np.zeros_like(input_np) # Initialize with zeros

    # 4. Iterate through the input grid and apply the replacement rule
    rows, cols = input_np.shape
    for r in range(rows):
        for c in range(cols):
            # If the input cell is non-zero, replace it with the target number
            if input_np[r, c] != 0:
                output_grid[r, c] = target_number
            # Else: leave it as zero (already handled by initialization)

    # Convert back to list of lists if necessary for the environment
    return output_grid.tolist()
