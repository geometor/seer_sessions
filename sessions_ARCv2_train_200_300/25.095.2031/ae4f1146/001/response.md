```python
import math
import numpy as np

def is_valid_subgrid(subgrid: list[list[int]]) -> bool:
    """
    Checks if a 3x3 subgrid contains only the digits 1 and 8.

    Args:
        subgrid: A 3x3 list of lists representing the subgrid.

    Returns:
        True if the subgrid contains only 1s and 8s, False otherwise.
    """
    for r in range(3):
        for c in range(3):
            if subgrid[r][c] == 0:
                return False
    return True

def extract_subgrid(grid: list[list[int]], start_row: int, start_col: int, size: int = 3) -> list[list[int]]:
    """
    Extracts a subgrid of a given size from the main grid.

    Args:
        grid: The main input grid.
        start_row: The starting row index of the subgrid.
        start_col: The starting column index of the subgrid.
        size: The dimension of the square subgrid (default is 3).

    Returns:
        The extracted subgrid as a list of lists.
    """
    subgrid = []
    for r in range(size):
        subgrid.append(grid[start_row + r][start_col : start_col + size])
    return subgrid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies and extracts the unique 3x3 subgrid within the 9x9 input grid
    that consists solely of the digits 1 and 8.
    """
    input_rows = len(input_grid)
    input_cols = len(input_grid[0])
    subgrid_size = 3

    # Iterate through all possible top-left corners of a 3x3 subgrid
    for r in range(input_rows - subgrid_size + 1):
        for c in range(input_cols - subgrid_size + 1):
            # Extract the current 3x3 subgrid
            current_subgrid = extract_subgrid(input_grid, r, c, subgrid_size)

            # Check if this subgrid contains only 1s and 8s (no 0s)
            if is_valid_subgrid(current_subgrid):
                # If it's the valid subgrid, return it
                return current_subgrid

    # Should not be reached based on the problem description,
    # but return an empty list or raise an error if no such subgrid is found.
    return [] # Or raise ValueError("No valid 3x3 subgrid found")

```