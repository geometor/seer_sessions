"""
Transforms an input grid by applying a right circular shift to the elements of 
odd-indexed rows, while leaving even-indexed rows unchanged.
"""

import collections

def _right_circular_shift(row: list[int]) -> list[int]:
    """
    Performs a right circular shift on the elements of a list by one position.
    The last element moves to the first position.
    Example: [a, b, c, d] -> [d, a, b, c]
    """
    if not row:  # Handle empty rows
        return []
    # Using deque for efficient rotation (though slicing is also fine for lists)
    # deque = collections.deque(row)
    # deque.rotate(1) # Positive rotates right
    # return list(deque)
    
    # Alternative using slicing:
    return [row[-1]] + row[:-1]


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Processes a 2D grid of integers. Rows with odd indices undergo a right
    circular shift of their elements. Rows with even indices remain unchanged.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Initialize an empty list to store the rows of the output grid
    output_grid = []

    # Iterate through each row of the input grid, keeping track of the row index
    for i, row in enumerate(input_grid):
        # Check if the current row index is odd
        if i % 2 != 0:
            # If the index is odd, perform a right circular shift on the row
            shifted_row = _right_circular_shift(row)
            # Append the shifted row to the output grid
            output_grid.append(shifted_row)
        else:
            # If the index is even, copy the row directly to the output grid
            # We append a copy to avoid modifying the original input if it's mutable elsewhere
            output_grid.append(row[:]) # Use slicing for a shallow copy

    # Return the completed output grid
    return output_grid
