import copy

"""
The transformation rule operates on an 8x8 grid of integers (2, 7, 9). It divides the grid into four quadrants (implicitly) and applies changes based on a condition related to the left half of the input grid.

1.  Check Condition: Determine if the integer '2' is present anywhere in the left half (columns 0-3) of the input grid.
2.  Modify Left Half: Regardless of the condition, fill the entire left half (columns 0-3) of the output grid with the integer '7'.
3.  Modify Right Half (Conditional):
    a.  If '2' was found in the input's left half:
        i.  Copy the top-right quadrant (rows 0-3, columns 4-7) from the input grid to the output grid.
        ii. Fill the bottom-right quadrant (rows 4-7, columns 4-7) of the output grid entirely with the integer '2'.
    b.  If '2' was *not* found in the input's left half:
        i.  Fill the top three rows of the top-right quadrant (rows 0-2, columns 4-7) of the output grid entirely with the integer '9'.
        ii. Copy the fourth row of the top-right quadrant (row 3, columns 4-7) from the input grid to the output grid.
        iii. Copy the entire bottom-right quadrant (rows 4-7, columns 4-7) from the input grid to the output grid.

"""


def check_for_two_in_left_half(grid: list[list[int]]) -> bool:
    """Checks if the value 2 exists in columns 0-3 of the grid."""
    rows = len(grid)
    for r in range(rows):
        for c in range(4):  # Check only columns 0, 1, 2, 3
            if grid[r][c] == 2:
                return True
    return False

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies the transformation rule based on the presence of '2' in the left half."""

    # Initialize output_grid as a deep copy to avoid modifying the original input
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) # Assuming rectangular grid

    # 1. Check the condition
    has_two_left = check_for_two_in_left_half(input_grid)

    # 2. Modify Left Half (always done)
    for r in range(rows):
        for c in range(4): # Columns 0, 1, 2, 3
            output_grid[r][c] = 7

    # 3. Modify Right Half (Conditional)
    if has_two_left:
        # Condition True: '2' was found in left half of input
        # 3.a.i: Top-right quadrant is already copied from input, no change needed here.
        # 3.a.ii: Fill bottom-right quadrant with '2'
        for r in range(4, rows): # Rows 4, 5, 6, 7
            for c in range(4, cols): # Columns 4, 5, 6, 7
                output_grid[r][c] = 2
    else:
        # Condition False: '2' was *not* found in left half of input
        # 3.b.i: Fill top three rows of top-right quadrant with '9'
        for r in range(3): # Rows 0, 1, 2
            for c in range(4, cols): # Columns 4, 5, 6, 7
                output_grid[r][c] = 9
        # 3.b.ii: Row 3 of top-right quadrant is already copied, no change needed.
        # 3.b.iii: Bottom-right quadrant is already copied, no change needed.

    return output_grid