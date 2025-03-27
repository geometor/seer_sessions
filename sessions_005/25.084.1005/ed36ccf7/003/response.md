```python
import copy

"""
The transformation rule rotates the input grid 270 degrees clockwise (or 90 degrees counter-clockwise).
The value of the pixel at input grid coordinates (row `r`, column `c`) is moved
to the output grid coordinates (row `W-1-c`, column `r`), where `W` is the width
of the input grid.
"""

def transform(input_grid):
    """
    Rotates the input grid 270 degrees clockwise.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the rotated output grid.
    """
    # Determine the height (H) and width (W) of the input grid.
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        # Handle case of empty rows
        return [[] for _ in range(height)]

    # Create a new output grid with W rows and H columns.
    # Initialize with a placeholder value (e.g., 0)
    output_grid_height = width
    output_grid_width = height
    output_grid = [[0 for _ in range(output_grid_width)] for _ in range(output_grid_height)]

    # Iterate through each row r from 0 to H-1 and each column c from 0 to W-1 in the input grid.
    for r in range(height):
        for c in range(width):
            # Get the pixel value from the input grid.
            value = input_grid[r][c]

            # Calculate the corresponding coordinates (output_r, output_c) in the output grid
            # using the 270-degree clockwise rotation formula.
            output_r = width - 1 - c
            output_c = r

            # Place the pixel value at the calculated position in the output grid.
            output_grid[output_r][output_c] = value

    # Return the fully constructed output grid.
    return output_grid
```