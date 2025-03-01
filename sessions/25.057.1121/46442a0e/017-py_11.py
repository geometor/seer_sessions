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