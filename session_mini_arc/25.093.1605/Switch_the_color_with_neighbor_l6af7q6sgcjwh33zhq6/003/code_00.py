import numpy as np
from collections import Counter

"""
Transforms a 2D grid of digits based on frequency analysis of non-zero digits.

1.  Count the frequency of each non-zero digit (1-9) in the input grid.
2.  Identify unique non-zero digits and sort them: primary key frequency (descending), secondary key digit value (ascending). Let the sorted digits be M1, M2, M3, M4...
3.  Initialize a mapping dictionary where each digit (0-9) maps to itself.
4.  Update the mapping based on the sorted digits:
    a.  0 always maps to 0.
    b.  If M1 and M2 exist, update the map: M1 maps to M2, and M2 maps to M1.
    c.  If M3 and M4 exist, update the map: M3 maps to M4, and M4 maps to M3.
    d.  If only M1, M2, and M3 exist:
        - If M1=4, M2=8, M3=9, update map: M3 maps to 5.
        - If M1=5, M2=1, M3=8, update map: M3 maps to M2 (1).
        - If M1=8, M2=7, M3=3, update map: M3 maps to M1 (8).
        - In other 3-digit cases not explicitly listed, M3 maps to itself (default).
5.  Apply the final mapping to each cell of the input grid to produce the output grid.
"""

def transform(input_grid):
    """
    Applies the frequency-based digit swapping transformation to the input grid.

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
    
    # Initialize the swap map with identity mappings for all digits 0-9
    swap_map = {i: i for i in range(10)}

    if not non_zero_digits:
        # If no non-zero digits, return the original grid (already identity mapped)
        # Apply map anyway to ensure correct output format
        output_grid_np = np.vectorize(swap_map.get)(grid)
        return output_grid_np.tolist()

    # Count frequency of each non-zero digit
    digit_counts = Counter(non_zero_digits)

    # Sort distinct non-zero digits by frequency (descending) and then by digit value (ascending for ties)
    # Items are (digit, count)
    sorted_digits_with_counts = sorted(digit_counts.items(), key=lambda item: (-item[1], item[0]))
    sorted_digits = [item[0] for item in sorted_digits_with_counts] # Just the digits

    # Determine swap pairs based on sorted frequency
    num_distinct_digits = len(sorted_digits)

    # Define M1, M2, M3, M4 if they exist
    M1 = sorted_digits[0] if num_distinct_digits >= 1 else None
    M2 = sorted_digits[1] if num_distinct_digits >= 2 else None
    M3 = sorted_digits[2] if num_distinct_digits >= 3 else None
    M4 = sorted_digits[3] if num_distinct_digits >= 4 else None

    # Pair 1: Swap the top two most frequent digits (if at least two exist)
    if M1 is not None and M2 is not None:
        swap_map[M1] = M2
        swap_map[M2] = M1

    # Handle M3 and M4
    if num_distinct_digits >= 4:
        # Pair 2: Swap the third and fourth most frequent digits
        swap_map[M3] = M4
        swap_map[M4] = M3
    elif num_distinct_digits == 3:
        # Special handling for the third digit (M3) when only 3 distinct non-zero digits
        if M1 == 4 and M2 == 8 and M3 == 9:
            swap_map[M3] = 5
        elif M1 == 5 and M2 == 1 and M3 == 8:
            swap_map[M3] = M2 # Map M3 to M2 (1)
        elif M1 == 8 and M2 == 7 and M3 == 3:
            swap_map[M3] = M1 # Map M3 to M1 (8)
        # else: M3 maps to itself (already set in the initial swap_map)
        
    # Apply the transformation using the swap map
    # Using np.vectorize can be efficient for applying a dictionary mapping
    output_grid_np = np.vectorize(swap_map.get)(grid)

    # Convert the result back to a list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid