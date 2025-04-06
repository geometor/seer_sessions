"""
Transforms an input 3x3 grid by rotating it 180 degrees.
The element at input_grid[i][j] is moved to output_grid[2-i][2-j].
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rotates a 3x3 input grid by 180 degrees.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 3x3 list of lists representing the 180-degree rotated grid.
    """
    # Assuming a 3x3 grid based on examples
    rows = 3
    cols = 3

    # Initialize output_grid with zeros or copy structure
    # Using deepcopy is safer if elements were mutable, but zeros work for ints
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)] 

    # Perform transformations: iterate through input grid
    for i in range(rows):
        for j in range(cols):
            # Calculate the new position after 180-degree rotation
            new_i = rows - 1 - i # 2 - i for a 3x3 grid
            new_j = cols - 1 - j # 2 - j for a 3x3 grid

            # Assign the value from the input grid to the new position in the output grid
            output_grid[new_i][new_j] = input_grid[i][j]

    return output_grid