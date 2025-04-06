"""
1. Identify all cells in the input grid that do not contain the value '1' (foreground cells).
2. Determine the bounding box (min/max row and column) enclosing all foreground cells.
3. If no foreground cells are found, return an empty grid.
4. Extract the subgrid defined by the bounding box from the input grid.
5. Create the output grid by replacing all '1's in the extracted subgrid with '0's, keeping other values unchanged.
"""

import math

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Extracts the non-background elements ('1' is background) within their bounding box
    and replaces the background elements within that box with '0'.
    """
    foreground_coords = []
    num_rows = len(input_grid)
    if num_rows == 0:
        return [] # Handle empty input grid
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return [] # Handle empty row

    background_value = 1 # Assuming '1' is always the background based on examples

    # 1. Identify foreground cells and their coordinates
    for r in range(num_rows):
        for c in range(num_cols):
            if input_grid[r][c] != background_value:
                foreground_coords.append((r, c))

    # 3. If no foreground cells are found, return an empty grid.
    if not foreground_coords:
        return []

    # 2. Determine the bounding box
    min_row = num_rows
    max_row = -1
    min_col = num_cols
    max_col = -1
    for r, c in foreground_coords:
        min_row = min(min_row, r)
        max_row = max(max_row, r)
        min_col = min(min_col, c)
        max_col = max(max_col, c)

    # 4 & 5. Extract the subgrid and replace background with 0 simultaneously
    output_grid = []
    for r in range(min_row, max_row + 1):
        new_row = []
        for c in range(min_col, max_col + 1):
            cell_value = input_grid[r][c]
            # Replace background value with 0, keep others
            new_row.append(0 if cell_value == background_value else cell_value)
        output_grid.append(new_row)

    return output_grid