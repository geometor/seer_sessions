import copy

"""
Takes a 3x3 input grid of integers and rotates it by 180 degrees to produce the output grid.
The element at index (row, col) in the input moves to index (2-row, 2-col) in the output.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rotates a 3x3 grid of integers by 180 degrees.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A new 3x3 list of lists representing the grid rotated by 180 degrees.
    """
    # Assuming a 3x3 grid based on the examples and description
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Initialize the output grid with the same dimensions, filled with zeros
    # Using copy.deepcopy ensures the output grid is independent, though for integers,
    # initializing with zeros and then filling is also safe.
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Calculate the new position after a 180-degree rotation
            # For a grid of height H and width W, the new position is (H-1-r, W-1-c)
            # In our 3x3 case, H=3 and W=3, so it's (3-1-r, 3-1-c) = (2-r, 2-c)
            new_r = rows - 1 - r
            new_c = cols - 1 - c

            # Place the element from the input grid into the calculated position in the output grid
            output_grid[new_r][new_c] = input_grid[r][c]

    # Return the transformed grid
    return output_grid
