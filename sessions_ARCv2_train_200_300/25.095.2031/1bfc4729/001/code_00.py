import copy

"""
Transform a 10x10 grid based on the locations and values of two non-zero numbers.

1. Identify the two non-zero cells in the 10x10 input grid. Let the cell with the
   smaller row index have value `C1` and row index `R1`. Let the cell with the
   larger row index have value `C2` and row index `R2`.
2. Create a new 10x10 output grid, initially filled with zeros.
3. Define the top region as rows 0 through `R1 + 2`.
4. Define the bottom region as rows `R1 + 3` through 9.
5. Process the top region (rows `r` from 0 to `R1 + 2`):
   - If the current row `r` is equal to `R1` or `R1 - 2`, fill the entire row `r`
     of the output grid with the value `C1`.
   - Otherwise (for other rows in the top region), set the cell at `(r, 0)` and
     the cell at `(r, 9)` of the output grid to the value `C1`.
6. Process the bottom region (rows `r` from `R1 + 3` to 9):
   - If the current row `r` is equal to `R2` or `R2 + 2`, fill the entire row `r`
     of the output grid with the value `C2`.
   - Otherwise (for other rows in the bottom region), set the cell at `(r, 0)` and
     the cell at `(r, 9)` of the output grid to the value `C2`.
7. Return the completed output grid.
"""

def find_non_zero_cells(grid: list[list[int]]) -> list[tuple[int, int, int]]:
    """Finds all non-zero cells and returns their row, column, and value."""
    non_zero = []
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0:
                non_zero.append((r, c, grid[r][c]))
    return non_zero

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation rule to the input grid.
    """
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Ensure grid is 10x10 as per observed examples
    if rows != 10 or cols != 10:
        # Or handle differently, maybe raise ValueError?
        # For now, return input if size is unexpected.
        print(f"Warning: Input grid size is {rows}x{cols}, expected 10x10.")
        return copy.deepcopy(input_grid)

    # 1. Identify the two non-zero cells
    non_zero_cells = find_non_zero_cells(input_grid)

    # Expect exactly two non-zero cells based on examples
    if len(non_zero_cells) != 2:
         print(f"Warning: Found {len(non_zero_cells)} non-zero cells, expected 2.")
         return copy.deepcopy(input_grid) # Return original if assumption fails

    # Sort by row index to find C1/R1 (upper) and C2/R2 (lower)
    non_zero_cells.sort(key=lambda x: x[0])
    r1, _, c1_val = non_zero_cells[0]
    r2, _, c2_val = non_zero_cells[1]

    # 2. Create a new 10x10 output grid, initially filled with zeros.
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # 3. Define the top region boundary (implicit in the loop below)
    # 4. Define the bottom region boundary (implicit in the loop below)

    # 5. Process the top region (rows r from 0 to R1 + 2)
    # Ensure R1 + 2 does not exceed grid bounds
    top_region_end_row = min(r1 + 2, rows - 1)
    for r in range(top_region_end_row + 1):
        # Check boundary conditions for filled rows (R1-2)
        if r == r1 or (r1 >= 2 and r == r1 - 2):
             # Fill the entire row with C1
            output_grid[r] = [c1_val] * cols
        else:
            # Set only the border columns to C1
            output_grid[r][0] = c1_val
            output_grid[r][cols - 1] = c1_val

    # 6. Process the bottom region (rows r from R1 + 3 to 9)
    bottom_region_start_row = r1 + 3
    # Check boundary conditions for filled rows (R2+2)
    fill_row_r2_plus_2 = -1 # Initialize to invalid row
    if r2 <= rows - 3: # Ensure R2+2 is within bounds
        fill_row_r2_plus_2 = r2 + 2

    for r in range(bottom_region_start_row, rows):
        if r == r2 or r == fill_row_r2_plus_2:
             # Fill the entire row with C2
            output_grid[r] = [c2_val] * cols
        else:
            # Set only the border columns to C2
            output_grid[r][0] = c2_val
            output_grid[r][cols - 1] = c2_val

    # 7. Return the completed output grid.
    return output_grid