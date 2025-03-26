```python
"""
Rotate the input grid 90 degrees clockwise.
"""

import copy

def transform(input_grid):
    """
    Rotates the input grid 90 degrees clockwise.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The rotated grid.
    """
    # Get the dimensions of the input grid
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize the output grid with swapped dimensions (width becomes height, height becomes width)
    # Fill with a placeholder value (e.g., 0, though it will be overwritten)
    output_grid = [[0 for _ in range(height)] for _ in range(width)]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Calculate the corresponding cell position in the rotated grid
            # For a 90-degree clockwise rotation, input[r][c] goes to output[c][height - 1 - r]
            new_r = c
            new_c = height - 1 - r
            
            # Assign the value from the input grid to the new position in the output grid
            output_grid[new_r][new_c] = input_grid[r][c]

    return output_grid

```