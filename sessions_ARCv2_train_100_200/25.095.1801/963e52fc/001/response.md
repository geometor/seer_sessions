```python
import copy

"""
The transformation takes an input grid and produces an output grid with the same height but double the width. Each row in the output grid is created by concatenating the corresponding row from the input grid with itself.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by duplicating each row horizontally.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A new list of lists representing the transformed grid where each
        row is duplicated horizontally.
    """
    # Initialize an empty list to store the rows of the output grid
    output_grid = []

    # Iterate through each row in the input grid
    for row in input_grid:
        # Create a new row by concatenating the current input row with itself
        # This effectively doubles the width of the row by repeating its content
        new_row = row + row
        # Append the newly created row to the output grid
        output_grid.append(new_row)

    # Return the completed output grid
    return output_grid

```