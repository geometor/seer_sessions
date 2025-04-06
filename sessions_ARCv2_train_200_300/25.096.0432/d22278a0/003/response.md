```python
import math

"""
Transforms an input grid based on the nearest non-zero input cell, subject to two conditions:
1. Strict Dominance: The output cell must be strictly closer (using Manhattan distance) 
   to the winning input cell than to any other non-zero input cell. If an output 
   cell is equidistant to two or more input cells, it remains zero.
2. Column Parity: The column index of the output cell must have the same parity 
   (even/odd) as the column index of the strictly closest winning input cell.

Tie-breaking for determining the 'winning' cell among equidistant candidates (before 
the strict dominance check) is done by selecting the cell with the minimum row index, 
and then the minimum column index if rows are also tied.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the nearest neighbor transformation with strict dominance and column parity checks.

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

    # Handle case with no non-zero input cells - return grid of zeros
    if not non_zero_cells:
        return [[0 for _ in range(cols)] for _ in range(rows)]

    # 2. Initialize an output grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # 4. Iterate through each cell (r_out, c_out) in the output grid
    for r_out in range(rows):
        for c_out in range(cols):
            
            # 5a. Calculate distances to all non-zero input cells
            distances = []
            for cell in non_zero_cells:
                r_in, c_in = cell['row'], cell['col']
                dist = abs(r_out - r_in) + abs(c_out - c_in)
                distances.append({'dist': dist, 'cell': cell})

            # 5b. Find the minimum distance
            if not distances: continue # Should not happen if non_zero_cells is not empty
            min_dist = min(d['dist'] for d in distances)

            # 5c. Identify all input cells at the minimum distance
            cells_at_min_dist = [d['cell'] for d in distances if d['dist'] == min_dist]

            # 5e. Strict Dominance Check: Only proceed if exactly one cell is at the minimum distance
            is_strictly_closest = (len(cells_at_min_dist) == 1)

            if is_strictly_closest:
                # 5d. Select the winning input cell (already determined since only one is closest)
                winning_cell = cells_at_min_dist[0]
                v_win, r_win, c_win = winning_cell['value'], winning_cell['row'], winning_cell['col']

                # 5f. Column Parity Check
                parity_match = (c_out % 2 == c_win % 2)

                # 5g. Assign value if both conditions met
                if parity_match:
                    output_grid[r_out][c_out] = v_win
            # 5h. Otherwise (if not strictly closest), leave the output cell as 0 (already initialized)

    # 6. Return the completed output grid
    return output_grid
```