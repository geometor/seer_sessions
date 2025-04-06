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
    d.  All other digits (including M3 if only 3 unique non-zeros exist, or any beyond M4) map to themselves.
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
    
    # Step 1: Analyze Frequency
    # Flatten the grid to easily count all elements
    flat_grid = grid.flatten()
    # Filter out zeros and count frequencies of the remaining digits
    non_zero_digits = [d for d in flat_grid if d != 0]
    
    # Initialize the transformation map with identity mapping (each digit maps to itself)
    # This handles digits not involved in swaps and the digit 0.
    swap_map = {i: i for i in range(10)}

    # If there are no non-zero digits, the identity map is correct, proceed to apply it
    if non_zero_digits:
        # Count frequency of each non-zero digit
        digit_counts = Counter(non_zero_digits)

        # Step 2: Sort Digits
        # Sort distinct non-zero digits: primary key frequency (desc), secondary key digit value (asc)
        # Items are (digit, count)
        sorted_digits_with_counts = sorted(digit_counts.items(), key=lambda item: (-item[1], item[0]))
        # Extract just the digits in sorted order
        sorted_digits = [item[0] for item in sorted_digits_with_counts] 

        # Step 3 & 4: Determine Swaps and Update Mapping
        num_distinct_digits = len(sorted_digits)

        # Define M1, M2 if they exist
        if num_distinct_digits >= 2:
            M1 = sorted_digits[0]
            M2 = sorted_digits[1]
            # Update map for the first pair swap
            swap_map[M1] = M2
            swap_map[M2] = M1

        # Define M3, M4 if they exist
        if num_distinct_digits >= 4:
            M3 = sorted_digits[2]
            M4 = sorted_digits[3]
            # Update map for the second pair swap
            swap_map[M3] = M4
            swap_map[M4] = M3
            
    # Step 5: Apply Transformation
    # Use the final swap_map to transform each element in the original grid.
    # np.vectorize allows applying the dictionary lookup element-wise.
    output_grid_np = np.vectorize(swap_map.get)(grid)

    # Convert the result back to a standard Python list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid