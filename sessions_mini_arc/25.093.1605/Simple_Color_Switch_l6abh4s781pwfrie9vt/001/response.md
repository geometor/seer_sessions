```python
import copy

"""
Reverses the vertical order of the rows in the input grid.
The top row becomes the bottom row, the second row becomes the second-to-last row, and so on,
while the content of each row remains unchanged.
"""

def transform(input_grid):
    """
    Reverses the order of rows in a 2D list (grid).

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A new list of lists representing the grid with rows reversed.
    """
    # Create a new list containing the rows of the input grid in reverse order
    # Slicing with [::-1] creates a reversed copy of the list.
    output_grid = input_grid[::-1]

    # Return the grid with reversed row order
    return output_grid

```