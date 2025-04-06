import math

"""
Transforms an input grid based on the nearest non-zero input cell, with a column parity constraint.

1.  Find all non-zero cells in the input grid, storing their value, row, and column.
2.  Initialize an output grid of the same dimensions as the input, filled with zeros.
3.  For each cell (r_out, c_out) in the output grid:
    a. Calculate the Manhattan distance to every non-zero input cell (v, r_in, c_in).
    b. Find the minimum Manhattan distance.
    c. Identify all input cells that have this minimum distance.
    d. Apply tie-breaking: Among the closest input cells, select the one with the smallest row index (r_in). If there's still a tie, select the one with the smallest column index (c_in). Let this winning input cell be (v*, r*_in, c*_in).
    e. Check if the output cell's column index (c_out) has the same parity (even/odd) as the winning input cell's column index (c*_in).
    f. If the parities match (c_out % 2 == c*_in % 2), set the output cell's value to v*. Otherwise, leave it as 0.
4. Return the completed output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the nearest neighbor transformation with column parity check.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)]

    # 1. Find all non-zero cells in the input grid
    non_zero_cells = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] != 0:
                non_zero_cells.append({'value': input_grid[r][c], 'row': r, 'col': c})

    # Handle case with no non-zero input cells
    if not non_zero_cells:
        return [[0 for _ in range(cols)] for _ in range(rows)]

    # 2. Initialize an output grid
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # 3. Iterate through each cell in the output grid
    for r_out in range(rows):
        for c_out in range(cols):
            min_dist = float('inf')
            closest_cells = []

            # 3a. Calculate Manhattan distance to every non-zero input cell
            for cell in non_zero_cells:
                r_in, c_in = cell['row'], cell['col']
                dist = abs(r_out - r_in) + abs(c_out - c_in)

                # 3b & 3c. Find minimum distance and identify closest cells
                if dist < min_dist:
                    min_dist = dist
                    closest_cells = [cell]
                elif dist == min_dist:
                    closest_cells.append(cell)

            # 3d. Apply tie-breaking (sort by row, then column)
            # Sorting key uses a tuple: (row, column)
            closest_cells.sort(key=lambda x: (x['row'], x['col']))
            winning_cell = closest_cells[0]
            v_win, r_win, c_win = winning_cell['value'], winning_cell['row'], winning_cell['col']

            # 3e. Check column parity
            if c_out % 2 == c_win % 2:
                 # 3f. If parities match, assign value
                 output_grid[r_out][c_out] = v_win
            # else: leave as 0 (already initialized)


    # 4. Return the completed output grid
    return output_grid