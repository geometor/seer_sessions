import copy

"""
Identifies a horizontal line of yellow pixels (color 4) in the input grid.
This line acts as a separator.
All pixels in rows above the separator line, and the separator line itself, are copied to the output grid.
All pixels in rows below the separator line are replaced with the background color (white/0) in the output grid.
"""

def find_separator_row(grid: list[list[int]], separator_color: int = 4) -> int:
    """
    Finds the index of the first row that consists entirely of the separator_color.

    Args:
        grid: The input grid (list of lists of integers).
        separator_color: The integer value representing the separator color (default is 4 for yellow).

    Returns:
        The row index of the separator line, or -1 if not found.
    """
    num_rows = len(grid)
    num_cols = len(grid[0]) if num_rows > 0 else 0

    for r in range(num_rows):
        is_separator = True
        if num_cols == 0: # Handle empty grid case, though unlikely in ARC
            is_separator = False
            break
        for c in range(num_cols):
            if grid[r][c] != separator_color:
                is_separator = False
                break
        if is_separator:
            return r
    return -1 # Should not happen based on task description


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: keep content above and including the yellow line,
    replace content below the yellow line with white background.

    Args:
        input_grid: The input grid (list of lists of integers).

    Returns:
        The transformed output grid (list of lists of integers).
    """
    num_rows = len(input_grid)
    if num_rows == 0:
        return []
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return [[] for _ in range(num_rows)] # Return grid of empty rows

    # Deep copy the input grid to initialize the output grid
    # This ensures the upper part is already copied.
    # We will modify the parts below the separator later.
    output_grid = copy.deepcopy(input_grid)

    # 1. Identify the row containing the horizontal yellow (4) line.
    separator_row_index = find_separator_row(input_grid, 4)

    # If no separator found (shouldn't happen based on examples), return original grid
    if separator_row_index == -1:
        # Consider raising an error or returning input based on expected behavior
        print("Warning: Separator row not found.")
        return output_grid

    # 2. (Implicitly done by deep copy) Copy all rows from the input grid,
    #    up to and including the separator row, directly to the output grid.

    # 3. Fill all rows in the output grid *below* the separator row with the background color (white/0).
    background_color = 0
    for r in range(separator_row_index + 1, num_rows):
        for c in range(num_cols):
            output_grid[r][c] = background_color
        # Or more concisely:
        # output_grid[r] = [background_color] * num_cols

    return output_grid