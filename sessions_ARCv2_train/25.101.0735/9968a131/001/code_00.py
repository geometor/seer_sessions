"""
Transforms an input grid of digits by performing a right cyclic shift on rows with odd indices (1, 3, 5, ...) and keeping rows with even indices (0, 2, 4, ...) unchanged.
"""

import collections

def _right_cyclic_shift(row: list[int]) -> list[int]:
    """Performs a right cyclic shift on a list by one position."""
    if not row:
        return []
    # Convert row to deque for efficient rotation
    deque_row = collections.deque(row)
    # Rotate right by 1 position
    deque_row.rotate(1)
    # Convert back to list
    return list(deque_row)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a transformation to the input grid based on row index.

    Args:
        input_grid: A list of lists representing the input grid of digits.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Initialize output_grid as an empty list
    output_grid = []

    # Iterate through each row of the input grid with its index
    for i, row in enumerate(input_grid):
        # Check if the row index is even or odd
        if i % 2 == 0:
            # If the index is even, append the original row to the output grid
            output_grid.append(row[:]) # Use a copy to avoid modifying original if needed later
        else:
            # If the index is odd, perform a right cyclic shift on the row
            shifted_row = _right_cyclic_shift(row)
            # Append the shifted row to the output grid
            output_grid.append(shifted_row)

    # Return the completed output grid
    return output_grid