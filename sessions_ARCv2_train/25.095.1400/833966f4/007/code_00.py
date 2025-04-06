"""
Transforms an input sequence of numbers represented as a single-column grid.
The transformation involves swapping the first two elements if the sequence length is 2 or more,
and swapping the last two elements if the sequence length is 4 or more.
Middle elements remain in their original relative positions.
"""

import math # Included based on template, not used in this specific logic
import copy # Included based on template, list() is sufficient for shallow copy here

# No helper functions needed for this specific transformation logic.

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: swap the first pair and the last pair of elements,
    conditionally based on sequence length.

    Args:
        input_grid: A list of lists, where each inner list contains a single integer,
                    representing the input sequence in a single-column format.

    Returns:
        A list of lists in the same single-column format, containing the transformed sequence.
    """

    # --- Input Parsing ---
    # Extract the 1D sequence of numbers from the single-column grid format.
    input_sequence = []
    for row in input_grid:
        # Assuming each row contains exactly one number and is not empty.
        if row: # Basic check for non-empty row
            input_sequence.append(row[0])
        # Add more robust error handling if input format might vary.

    # Get the length of the sequence
    n = len(input_sequence)

    # --- Transformation ---
    # Create a mutable copy of the input sequence to store the potentially modified output.
    # A shallow copy using list() is sufficient as integers are immutable.
    output_sequence = list(input_sequence)

    # Apply conditional swap for the first pair
    if n >= 2:
        # Swap the elements at index 0 and index 1
        output_sequence[0], output_sequence[1] = output_sequence[1], output_sequence[0]

    # Apply conditional swap for the last pair
    if n >= 4:
        # Swap the elements at index n-2 (second to last) and index n-1 (last)
        output_sequence[n-2], output_sequence[n-1] = output_sequence[n-1], output_sequence[n-2]

    # Elements between index 1 and n-2 (if any) remain untouched in their relative positions
    # because we started with a copy and only modified the ends.

    # --- Output Formatting ---
    # Convert the transformed 1D sequence back into the single-column grid format.
    output_grid = []
    for num in output_sequence:
        output_grid.append([num]) # Create a list containing the single number for each row

    return output_grid