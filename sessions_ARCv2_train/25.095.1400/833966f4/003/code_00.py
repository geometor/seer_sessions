"""
Transforms an input sequence of numbers by swapping the first two elements and the last two elements.
The input is provided as a single-column grid (list of lists), and the output is returned in the same format.
If the sequence has fewer than 2 elements, it remains unchanged.
If the sequence has 2 or 3 elements, only the first two are swapped.
If the sequence has 4 or more elements, both the first two and the last two pairs are swapped.
Middle elements (between the first and last pairs) remain in their original positions relative to each other.
"""

import math # Not strictly needed for this logic, but included as per standard practice/template.
import copy # Used for creating a mutable copy of the input sequence.

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: swap the first pair and the last pair of elements.

    Args:
        input_grid: A list of lists, where each inner list contains a single integer,
                    representing the input sequence in a single-column format.

    Returns:
        A list of lists in the same single-column format, containing the transformed sequence.
    """

    # --- Input Parsing ---
    # Extract the 1D sequence of numbers from the single-column grid format.
    # e.g., [[9], [0], [1], [6], [8]] becomes [9, 0, 1, 6, 8]
    input_sequence = []
    for row in input_grid:
        if row: # Ensure row is not empty
            input_sequence.append(row[0])
        # Consider handling empty rows differently if required by task variations
        # else: input_sequence.append(None) # Or some placeholder if needed

    # Get the length of the sequence
    n = len(input_sequence)

    # --- Transformation ---
    # Create a mutable copy of the input sequence to modify
    output_sequence = copy.deepcopy(input_sequence) # Use deepcopy for nested structures if needed, though simple list copy() works here

    # Apply conditional swaps based on sequence length
    if n >= 2:
        # Swap the first pair (elements at index 0 and 1)
        output_sequence[0], output_sequence[1] = output_sequence[1], output_sequence[0]

    if n >= 4:
        # Swap the last pair (elements at index n-2 and n-1)
        output_sequence[n-2], output_sequence[n-1] = output_sequence[n-1], output_sequence[n-2]

    # --- Output Formatting ---
    # Convert the transformed 1D sequence back into the single-column grid format.
    # e.g., [0, 9, 1, 8, 6] becomes [[0], [9], [1], [8], [6]]
    output_grid = []
    for num in output_sequence:
        output_grid.append([num])

    return output_grid
