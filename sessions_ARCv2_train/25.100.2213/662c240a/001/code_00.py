import math
import collections

"""
Selects the first 3x3 block from the 9x3 input grid that is not symmetric.
The input grid is treated as three consecutive 3x3 blocks.
A block (matrix) is symmetric if M[i][j] == M[j][i] for all i, j.
The function iterates through the blocks in order and returns the first one
that fails the symmetry test.
"""

def is_symmetric(matrix: list[list[int]]) -> bool:
    """Checks if a 3x3 matrix is symmetric."""
    # A 3x3 matrix M is symmetric if:
    # M[0][1] == M[1][0]
    # M[0][2] == M[2][0]
    # M[1][2] == M[2][1]
    if matrix[0][1] != matrix[1][0]:
        return False
    if matrix[0][2] != matrix[2][0]:
        return False
    if matrix[1][2] != matrix[2][1]:
        return False
    return True

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selects the first non-symmetric 3x3 block from the 9x3 input grid.

    Args:
        input_grid: A list of 9 lists, where each inner list contains 3 integers,
                    representing the 9x3 input grid.

    Returns:
        A list of 3 lists, each containing 3 integers, representing the
        first non-symmetric 3x3 block found.
    """

    # Ensure the input grid has the expected dimensions (9x3)
    if len(input_grid) != 9 or not all(len(row) == 3 for row in input_grid):
        raise ValueError("Input grid must be 9x3.")

    # Divide the 9x3 input grid into three 3x3 blocks
    block1 = input_grid[0:3]
    block2 = input_grid[3:6]
    block3 = input_grid[6:9]

    # Check symmetry for Block 1
    if not is_symmetric(block1):
        return block1 # Return Block 1 if it's not symmetric

    # Check symmetry for Block 2
    if not is_symmetric(block2):
        return block2 # Return Block 2 if it's not symmetric

    # If Block 1 and Block 2 are symmetric, return Block 3
    # (Based on the problem description, the third block is implicitly the result
    # if the first two are symmetric).
    return block3