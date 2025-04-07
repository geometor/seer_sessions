```python
"""
Processes each column of the input grid independently. Within each column, iterates from top to bottom. When a non-zero number is encountered, it becomes the 'current fill value'. Subsequent zero cells below it in the same column are filled with this 'current fill value' until another non-zero number is found, which then becomes the new 'current fill value'. Zeros above the first non-zero number in a column remain zero.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Fills zero cells downwards in each column with the value of the nearest non-zero cell above it.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Handle empty input grid case
    if not input_grid or not input_grid[0]:
        return []

    # Get grid dimensions
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Initialize output_grid as a deep copy to avoid modifying the original input
    output_grid = copy.deepcopy(input_grid)

    # Iterate through each column
    for j in range(num_cols):
        # Initialize the value to fill downwards for the current column
        current_fill_value = 0

        # Iterate through each row in the current column
        for i in range(num_rows):
            # Check the value in the original input grid
            if input_grid[i][j] != 0:
                # Update the fill value if a non-zero number is found
                current_fill_value = input_grid[i][j]
                # The output grid already has this non-zero value from the deepcopy
            else:
                # If the current cell is zero and we have a fill value
                if current_fill_value != 0:
                    # Fill the corresponding cell in the output grid
                    output_grid[i][j] = current_fill_value

    # Return the transformed grid
    return output_grid
```