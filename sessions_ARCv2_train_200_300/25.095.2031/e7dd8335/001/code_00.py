"""
Transforms an input grid by changing the value of cells from 1 to 2 if they belong to the lower half of the vertical extent of the shape formed by all 1s.

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all row indices in the input grid that contain at least one cell with the value `1`.
3.  If no rows contain `1`, return the copied grid.
4.  Determine the minimum (`min_row`) and maximum (`max_row`) row indices of the shape.
5.  Calculate the vertical height of the shape: `height = max_row - min_row + 1`.
6.  Calculate the midpoint row index: `midpoint_row = min_row + (height // 2)`. Note: Integer division ensures the lower half includes the middle row if the height is odd.
7.  Iterate through each cell of the input grid.
8.  If a cell's value is `1` and its row index is greater than or equal to `midpoint_row`, change the corresponding cell's value in the output grid to `2`.
9.  Return the modified output grid.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Ensure the input is not empty
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # 1. Initialize the output grid as a deep copy of the input grid.
    output_grid = copy.deepcopy(input_grid)

    # 2. Identify all row indices containing at least one '1'.
    shape_rows = []
    for r in range(rows):
        if 1 in input_grid[r]:
            shape_rows.append(r)

    # 3. If no '1's are found, return the original grid copy.
    if not shape_rows:
        return output_grid

    # 4. Determine the minimum and maximum row indices of the shape.
    min_row = min(shape_rows)
    max_row = max(shape_rows)

    # 5. Calculate the vertical height of the shape.
    height = max_row - min_row + 1

    # 6. Calculate the midpoint row index.
    # Cells at or below this row index are considered in the lower half.
    midpoint_row = min_row + (height // 2)

    # 7. Iterate through each cell of the input grid.
    for r in range(rows):
        for c in range(cols):
            # 8. Check if the cell value is 1 and its row is in the lower half.
            if input_grid[r][c] == 1 and r >= midpoint_row:
                # 9. Update the value in the output grid to 2.
                output_grid[r][c] = 2

    # 10. Return the final output grid.
    return output_grid