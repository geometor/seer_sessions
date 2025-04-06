import copy

"""
Accept a 4x4 input grid containing integers from 0 to 4.
Identify the locations (row and column indices) of all cells containing 0.
Determine the appropriate number (from {1, 2, 3, 4}) to place in each empty cell
such that the final grid is a Latin Square:
- Every row contains each number from 1 to 4 exactly once.
- Every column contains each number from 1 to 4 exactly once.
The non-zero numbers in the input act as fixed constraints.
Return the completed 4x4 grid.
This is achieved using a backtracking algorithm.
"""

def find_empty(grid: list[list[int]]) -> tuple[int, int] | None:
    """Finds the row and column index of the next empty cell (value 0).

    Args:
        grid: The current state of the 4x4 grid.

    Returns:
        A tuple (row, col) if an empty cell is found, otherwise None.
    """
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0:
                return (r, c)
    return None  # No empty cells left

def is_valid_placement(grid: list[list[int]], r: int, c: int, num: int) -> bool:
    """Checks if placing 'num' at grid[r][c] violates Latin Square rules.

    Args:
        grid: The current state of the 4x4 grid.
        r: The row index to check.
        c: The column index to check.
        num: The number (1-4) to potentially place.

    Returns:
        True if placing the number is valid according to row and column constraints,
        False otherwise.
    """
    # Check row constraint: ensure 'num' is not already in the row
    for col_check in range(4):
        if grid[r][col_check] == num:
            return False
    # Check column constraint: ensure 'num' is not already in the column
    for row_check in range(4):
        if grid[row_check][c] == num:
            return False
    return True

def solve_latin_square(grid: list[list[int]]) -> bool:
    """Recursive backtracking function to fill the grid.

    Args:
        grid: The grid to be solved (modified in-place).

    Returns:
        True if a solution is found, False otherwise.
    """
    # Find the next empty cell
    find = find_empty(grid)
    if not find:
        return True  # Grid is full, solution found
    else:
        r, c = find

    # Try filling the empty cell with numbers 1 to 4
    for num in range(1, 5):
        # Check if placing 'num' at (r, c) is valid
        if is_valid_placement(grid, r, c, num):
            # Place the number
            grid[r][c] = num

            # Recursively try to solve the rest of the grid
            if solve_latin_square(grid):
                return True  # Solution found down this path

            # If recursion failed, backtrack: reset the cell and try the next number
            grid[r][c] = 0

    # If no number from 1-4 worked for this cell, return False to trigger backtracking
    return False


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Create a deep copy of the input grid to work with, preserving the original
    output_grid = copy.deepcopy(input_grid)

    # Use the backtracking solver to fill the empty cells (0s) in the copied grid
    # The function modifies output_grid in-place
    solved = solve_latin_square(output_grid)

    # Although the examples guarantee a solution, in a general case,
    # one might check if 'solved' is True before returning.
    # For this specific task based on examples, we assume a solution exists.
    # if not solved:
    #     # Handle cases where no solution exists if necessary
    #     # For this problem, assume input always leads to a valid solution
    #     pass

    # Return the completed grid
    return output_grid