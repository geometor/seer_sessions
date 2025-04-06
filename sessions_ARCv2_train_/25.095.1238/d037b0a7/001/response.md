```python
"""
Transforms an input grid by propagating the last seen non-zero value downwards within each column. 
Zeros below a non-zero number in a column are replaced by that number until another non-zero number is encountered in that column.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the downward propagation transformation to the input grid.

    Args:
        input_grid: A 2D list representing the input grid of integers.

    Returns:
        A 2D list representing the transformed grid.
    """
    # Ensure the input is not empty
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # This ensures original non-zero values are preserved unless overwritten
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each column
    for c in range(width):
        # Initialize the last non-zero value seen in this column
        last_non_zero_value = 0

        # Iterate through each row within the current column, from top to bottom
        for r in range(height):
            # Get the value from the original input grid for reference
            input_value = input_grid[r][c]

            # If the input value is non-zero, update the last seen non-zero value
            if input_value != 0:
                last_non_zero_value = input_value
                # Ensure the output grid has this non-zero value (already true from copy, but explicit)
                output_grid[r][c] = input_value
            # If the input value is zero AND we have previously seen a non-zero value in this column
            elif last_non_zero_value != 0:
                # Update the corresponding cell in the output grid with the last non-zero value
                output_grid[r][c] = last_non_zero_value
            # If the input value is zero and no non-zero value has been seen yet in this column,
            # the output remains zero (as initialized by the copy).

    # Return the fully transformed grid
    return output_grid

```