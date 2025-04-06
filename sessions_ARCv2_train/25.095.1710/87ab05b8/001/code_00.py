import copy

"""
Transforms a 4x4 input grid based on quadrant analysis.
The output grid's top half (top-left and top-right 2x2 quadrants) is always filled with the digit 6.
The output grid's bottom-left 2x2 quadrant is filled with the digit 2 if the digit 2 is present anywhere within the input grid's bottom-left 2x2 quadrant; otherwise, it's filled with 6.
The output grid's bottom-right 2x2 quadrant is filled with the digit 2 if the digit 2 is present anywhere within the input grid's bottom-right 2x2 quadrant; otherwise, it's filled with 6.
"""

def check_quadrant_for_digit(grid: list[list[int]], start_row: int, start_col: int, target_digit: int) -> bool:
    """
    Checks if a target digit exists within a specified 2x2 quadrant of the grid.

    Args:
        grid: The input grid (list of lists).
        start_row: The starting row index of the quadrant.
        start_col: The starting column index of the quadrant.
        target_digit: The digit to search for.

    Returns:
        True if the target digit is found in the quadrant, False otherwise.
    """
    for r in range(start_row, start_row + 2):
        for c in range(start_col, start_col + 2):
            if grid[r][c] == target_digit:
                return True
    return False

def fill_quadrant(grid: list[list[int]], start_row: int, start_col: int, fill_value: int):
    """
    Fills a specified 2x2 quadrant of the grid with a given value.

    Args:
        grid: The grid to modify (list of lists).
        start_row: The starting row index of the quadrant.
        start_col: The starting column index of the quadrant.
        fill_value: The value to fill the quadrant with.
    """
    for r in range(start_row, start_row + 2):
        for c in range(start_col, start_col + 2):
            grid[r][c] = fill_value


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the quadrant-based transformation rule to the input grid.
    """
    # Initialize output_grid (can start with a copy or create a new one)
    # Creating a new grid filled with a default value (e.g., 0 or 6)
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)] # Initialize with 0s

    background_digit = 6
    target_digit = 2

    # 1 & 2. Fill the top-left and top-right quadrants with the background digit (6)
    fill_quadrant(output_grid, 0, 0, background_digit) # Top-left
    fill_quadrant(output_grid, 0, 2, background_digit) # Top-right

    # 3. Check the input grid's bottom-left quadrant for the target digit (2)
    contains_target_bl = check_quadrant_for_digit(input_grid, 2, 0, target_digit)

    # 4. Fill the output grid's bottom-left quadrant based on the check
    fill_value_bl = target_digit if contains_target_bl else background_digit
    fill_quadrant(output_grid, 2, 0, fill_value_bl)

    # 5. Check the input grid's bottom-right quadrant for the target digit (2)
    contains_target_br = check_quadrant_for_digit(input_grid, 2, 2, target_digit)

    # 6. Fill the output grid's bottom-right quadrant based on the check
    fill_value_br = target_digit if contains_target_br else background_digit
    fill_quadrant(output_grid, 2, 2, fill_value_br)

    return output_grid