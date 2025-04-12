```python
import math
import collections

"""
Iterate through the input grid row by row, left to right. Collect all non-zero numbers encountered during this scan into a flat list.
"""

def transform(input_grid: list[list[int]]) -> list[int]:
    """
    Transforms a 2D grid of integers into a 1D list containing
    only the non-zero elements from the grid, preserving their
    order as encountered during a row-by-row, left-to-right scan.

    Args:
        input_grid: A list of lists of integers representing the input grid.

    Returns:
        A list of integers containing all non-zero elements from the input grid.
    """
    # Initialize an empty list to store the output sequence
    output_sequence = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Iterate through each cell (number) in the current row
        for cell_value in row:
            # If the value of the current cell is not zero
            if cell_value != 0:
                # Append this value to the output sequence
                output_sequence.append(cell_value)

    # Return the final output sequence
    return output_sequence
```