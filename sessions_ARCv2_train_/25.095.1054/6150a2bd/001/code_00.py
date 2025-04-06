import copy

"""
Rotate the input 3x3 grid by 180 degrees to produce the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rotates a 3x3 grid of integers by 180 degrees.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A new 3x3 list of lists representing the input grid rotated by 180 degrees.
    """
    # Assuming the input is always 3x3 based on the examples
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Validate if the grid is 3x3 (optional but good practice for robustness)
    # if rows != 3 or cols != 3:
    #     raise ValueError("Input grid must be 3x3")

    # Initialize the output grid with the same dimensions, filled with zeros or copied
    # Using deepcopy ensures we don't modify the original structure if we filled it differently
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)] 
    # Alternatively: output_grid = copy.deepcopy(input_grid) and then overwrite

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the new position after a 180-degree rotation
            # For a grid of size N x M, the new position (r', c') for an element at (r, c)
            # after a 180-degree rotation is (N-1-r, M-1-c).
            # In our 3x3 case (N=3, M=3), this simplifies to (2-r, 2-c).
            new_r = rows - 1 - r
            new_c = cols - 1 - c

            # Assign the value from the input grid's current cell (r, c)
            # to the calculated new cell (new_r, new_c) in the output grid.
            output_grid[new_r][new_c] = input_grid[r][c]

    # Return the newly created and populated output grid
    return output_grid