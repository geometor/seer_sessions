import copy

"""
Rotate the input grid 90 degrees counter-clockwise to produce the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rotates a square 2D list (grid) 90 degrees counter-clockwise.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the grid rotated 90 degrees counter-clockwise.
    """

    # Ensure the input is not empty
    if not input_grid or not input_grid[0]:
        return []

    # Get the dimensions of the grid (assuming square)
    n = len(input_grid)

    # Initialize the output grid with the same dimensions, filled with a placeholder (e.g., 0)
    # Using deepcopy to ensure inner lists are independent copies if needed later,
    # though here we'll overwrite everything. A list comprehension is cleaner.
    output_grid = [[0 for _ in range(n)] for _ in range(n)]

    # Perform the 90-degree counter-clockwise rotation
    # For each element at input_grid[row][col], its new position in the output_grid
    # will be output_grid[n - 1 - col][row].
    for r in range(n):
        for c in range(n):
            new_row = n - 1 - c
            new_col = r
            output_grid[new_row][new_col] = input_grid[r][c]

    # Return the rotated grid
    return output_grid
