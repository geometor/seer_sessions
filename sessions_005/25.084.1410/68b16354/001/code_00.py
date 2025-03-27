"""
Reverses the order of the rows in the input grid to produce the output grid.
The row at index i in the input grid becomes the row at index height - 1 - i
in the output grid, where height is the total number of rows.
"""

import copy

def transform(input_grid):
    """
    Vertically flips the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A new 2D list representing the vertically flipped grid.
    """
    # Create a new list containing the rows of the input grid in reverse order.
    # Slicing [::-1] creates a shallow copy with the elements reversed.
    # Since the elements are lists (rows), and we are not modifying the rows themselves,
    # a shallow copy is sufficient. If we needed to modify elements within the rows,
    # a deep copy might be necessary.
    output_grid = input_grid[::-1]

    # Return the new grid with reversed row order
    return output_grid
