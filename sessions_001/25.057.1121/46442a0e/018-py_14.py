"""
The transformation rule involves creating a border around the input grid. The output grid's dimensions are determined by adding 2 to both the height and width of the input grid. The input grid is placed in the center of the output grid. The border is constructed using the color of the largest contiguous region originating from a corner of the input grid.
"""

import numpy as np

def find_contiguous_region(grid, start_row, start_col):
    """
    Finds a contiguous region of the same color starting from a given cell.

    Args:
        grid: The 2D numpy array representing the grid.
        start_row: The row index of the starting cell.
        start_col: The column index of the starting cell.

    Returns:
        A set of (row, col) tuples representing the contiguous region.
    """
    rows, cols = grid.shape
    color = grid[start_row, start_col]
    region = set()
    stack = [(start_row, start_col)]

    while stack:
        row, col = stack.pop()
        if (row, col) in region:
            continue
        if 0 <= row < rows and 0 <= col < cols and grid[row, col] == color:
            region.add((row, col))
            stack.extend([(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)])

    return region

def transform(input_grid):
    # Get input grid dimensions
    input_height, input_width = input_grid.shape

    # Calculate output grid dimensions
    output_height = input_height + 2
    output_width = input_width + 2

    # Initialize output_grid with zeros
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Copy input grid to the center of the output grid
    output_grid[1:input_height+1, 1:input_width+1] = input_grid

    # Find the border color from the largest contiguous region starting at (0,0)
    border_region = find_contiguous_region(input_grid, 0, 0)
    border_color = input_grid[0, 0]

    # Fill the border of the output grid with the border color
    output_grid[:, 0] = border_color  # Left border
    output_grid[:, -1] = border_color  # Right border
    output_grid[0, :] = border_color  # Top border
    output_grid[-1, :] = border_color  # Bottom border

    return output_grid