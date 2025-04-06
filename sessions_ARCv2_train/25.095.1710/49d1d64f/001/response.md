```python
import math
import collections

"""
Transforms an input grid of numbers by adding a border. 
The top and bottom border rows are created by padding the first and last input rows respectively with zeros at the beginning and end. 
Each original input row is transformed into a new row by padding it with its own first element at the beginning and its own last element at the end.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies border padding to the input grid according to the specified rules.

    Args:
        input_grid: A list of lists representing the 2D integer input grid.

    Returns:
        A list of lists representing the transformed 2D integer output grid
        with border padding.
    """
    # Initialize the list to store the rows of the output grid
    output_grid = []

    # Handle empty input grid case
    if not input_grid or not input_grid[0]:
        return [] # Or handle as appropriate, maybe return [[0,0],[0,0]]? 
                   # Based on examples, input is never empty.

    # Get the first and last rows of the input grid
    first_input_row = input_grid[0]
    last_input_row = input_grid[-1]

    # Create the top border row: [0] + first_input_row + [0]
    top_border_row = [0] + first_input_row + [0]
    output_grid.append(top_border_row)

    # Iterate through each row of the input grid to create the middle rows
    for input_row in input_grid:
        # Get the first and last element of the current input row
        first_element = input_row[0]
        last_element = input_row[-1]

        # Create the output middle row: [first_element] + input_row + [last_element]
        output_middle_row = [first_element] + input_row + [last_element]
        output_grid.append(output_middle_row)

    # Create the bottom border row: [0] + last_input_row + [0]
    bottom_border_row = [0] + last_input_row + [0]
    output_grid.append(bottom_border_row)

    # Return the completely assembled output grid
    return output_grid

```