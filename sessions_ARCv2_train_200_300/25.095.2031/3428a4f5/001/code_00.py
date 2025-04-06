import numpy as np

"""
1. Locate Separator: Scan the input grid row by row to find the row composed entirely of the integer 4. This is the separator row.
2. Extract Sub-grids:
    * Define the "Top Sub-grid" as all rows in the input grid preceding the separator row.
    * Define the "Bottom Sub-grid" as all rows in the input grid following the separator row.
3. Initialize Output: Create a new grid (the "Output Grid") with the same number of rows and columns as the Top Sub-grid (or Bottom Sub-grid).
4. Compare and Populate: Iterate through each cell position, identified by its row index `r` and column index `c`, within the dimensions of the sub-grids.
    * For each position (`r`, `c`):
        * Retrieve the value from the Top Sub-grid at (`r`, `c`). Let this be `value_top`.
        * Retrieve the value from the Bottom Sub-grid at (`r`, `c`). Let this be `value_bottom`.
        * Compare `value_top` and `value_bottom`.
        * If `value_top` is identical to `value_bottom`, set the cell value in the Output Grid at position (`r`, `c`) to 0.
        * If `value_top` is different from `value_bottom`, set the cell value in the Output Grid at position (`r`, `c`) to 3.
5. Finalize: Once all cell positions have been processed, the populated Output Grid is the final result.
"""


def find_separator_index(grid: list[list[int]]) -> int:
    """Finds the index of the row containing only the value 4."""
    for r, row in enumerate(grid):
        if all(cell == 4 for cell in row):
            return r
    return -1 # Should not happen based on problem description

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by comparing elements above and below a separator row.
    """

    # 1. Locate Separator
    separator_index = find_separator_index(input_grid)

    # 2. Extract Sub-grids
    top_subgrid = input_grid[:separator_index]
    bottom_subgrid = input_grid[separator_index + 1:]

    # Ensure subgrids are not empty and have the same dimensions
    if not top_subgrid or not bottom_subgrid:
        raise ValueError("Input grid does not contain valid top and bottom subgrids.")
    if len(top_subgrid) != len(bottom_subgrid) or len(top_subgrid[0]) != len(bottom_subgrid[0]):
         raise ValueError("Top and bottom subgrids have different dimensions.")

    num_rows = len(top_subgrid)
    num_cols = len(top_subgrid[0])

    # 3. Initialize Output grid
    # Create a grid of the correct size, initialized with zeros
    output_grid = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

    # 4. Compare and Populate
    for r in range(num_rows):
        for c in range(num_cols):
            value_top = top_subgrid[r][c]
            value_bottom = bottom_subgrid[r][c]

            # Compare values and assign to output grid
            if value_top == value_bottom:
                output_grid[r][c] = 0
            else:
                output_grid[r][c] = 3

    # 5. Finalize and return
    return output_grid