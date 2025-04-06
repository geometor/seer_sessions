```python
import numpy as np

"""
Iterate through each row of the input grid. For the current row, reverse the horizontal order of its elements. Construct the output grid by placing each reversed row at the same row index as its corresponding original row in the input grid.
"""

def reverse_row(row: list[int]) -> list[int]:
    """Reverses the order of elements in a list."""
    return row[::-1]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by reversing each row horizontally.

    Args:
        input_grid: A list of lists representing the input 2D grid of integers.

    Returns:
        A list of lists representing the output 2D grid with each row reversed.
    """
    # Initialize an empty list to store the transformed rows
    output_grid = []

    # Iterate through each row of the input grid
    for row in input_grid:
        # Reverse the current row
        reversed_row = reverse_row(row)
        # Append the reversed row to the output grid
        output_grid.append(reversed_row)

    # Return the fully transformed grid
    return output_grid
```