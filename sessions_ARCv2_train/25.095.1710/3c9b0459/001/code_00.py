import copy

"""
Rotates the input 3x3 grid by 180 degrees to produce the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rotates a 3x3 grid of integers by 180 degrees.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A new 3x3 list of lists representing the grid rotated by 180 degrees.
    """

    # Get the dimensions (assuming a square grid, specifically 3x3 based on examples)
    rows = len(input_grid)
    cols = len(input_grid[0]) # Assumes at least one row

    # Initialize output_grid with the same dimensions, filled with a placeholder (e.g., 0)
    # Using deepcopy might be simpler if just modifying in place isn't desired, 
    # but creating a new grid explicitly shows the mapping.
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Perform transformations: Iterate through each element of the input grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the new position after a 180-degree rotation
            # For an element at (r, c), the new position is (rows - 1 - r, cols - 1 - c)
            new_r = rows - 1 - r
            new_c = cols - 1 - c

            # Place the element from the input grid into the calculated position in the output grid
            output_grid[new_r][new_c] = input_grid[r][c]

    return output_grid