```python
import copy

"""
Iterate through each cell of the input grid.
If the cell's value is 5, change it to 8 in the output grid.
If the cell's value is 8, change it to 5 in the output grid.
Otherwise, keep the original value.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by swapping the values 5 and 8.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A new 2D list of integers representing the transformed grid where
        all 5s are replaced by 8s and all 8s are replaced by 5s.
    """

    # Get the dimensions of the grid
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])

    # Initialize output_grid as a copy of the input to preserve original dimensions and non-target values
    # Or initialize an empty list to build the output grid
    output_grid = []

    # Iterate through each row of the input grid
    for r in range(rows):
        # Initialize a new row for the output grid
        new_row = []
        # Iterate through each cell in the current row
        for c in range(cols):
            # Get the value of the current cell
            cell_value = input_grid[r][c]

            # Apply the transformation rules
            if cell_value == 5:
                # If the value is 5, change it to 8
                new_row.append(8)
            elif cell_value == 8:
                # If the value is 8, change it to 5
                new_row.append(5)
            else:
                # Otherwise, keep the original value
                new_row.append(cell_value)
        # Add the processed row to the output grid
        output_grid.append(new_row)

    # Return the resulting grid
    return output_grid
```