import copy

"""
Transforms an input square grid (N x N) into an output grid (2N x 2N) using a specific pattern involving row swapping, value inversion, and tiling.

1.  Determine the primary non-zero digit `P` present in the input grid.
2.  Create a temporary base grid (N x N) based on the input:
    *   If N >= 2, the first row of the base grid is the second row of the input, and the second row of the base grid is the first row of the input.
    *   If N < 2, the base grid starts as a copy of the input grid.
    *   For all rows in the base grid starting from index 2 (if N >= 2), modify the corresponding input row: replace every 0 with `P` and every `P` with 0. Place this modified row into the base grid at the same index.
3.  Construct an intermediate grid (N x 2N) by horizontally duplicating each row of the temporary base grid (concatenate each row with itself).
4.  Construct the final output grid (2N x 2N) by vertically duplicating the intermediate grid (stack the intermediate grid on top of itself).
"""

def find_primary_non_zero(grid: list[list[int]]) -> int | None:
    """Finds the first non-zero digit encountered in the grid."""
    for row in grid:
        for cell in row:
            if cell != 0:
                return cell
    return None # Or potentially raise an error if a non-zero must exist

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A square list of lists representing the N x N input grid.

    Returns:
        A list of lists representing the 2N x 2N output grid.
    """
    n = len(input_grid)
    if n == 0:
        return []

    # --- Step 1: Find the primary non-zero digit ---
    primary_non_zero = find_primary_non_zero(input_grid)
    # If all zeros, the inversion step won't work as expected,
    # but based on examples, there's always a non-zero.
    # If primary_non_zero is None and n >= 2, the inversion below might need adjustment.
    # For now, assume it's always found based on examples.
    if primary_non_zero is None and n > 0 : # Handle all zero case gracefully - treat as P=0 for inversion?
        primary_non_zero = 0 # If grid is all zeros, inversion does nothing.

    # --- Step 2: Create the temporary base grid (N x N) ---
    modified_base_grid = [[0] * n for _ in range(n)] # Initialize with zeros

    # Handle row swapping for N >= 2
    if n >= 2:
        modified_base_grid[0] = copy.deepcopy(input_grid[1])
        modified_base_grid[1] = copy.deepcopy(input_grid[0])
    elif n == 1: # Handle N=1 case
         modified_base_grid[0] = copy.deepcopy(input_grid[0])


    # Handle rows from index 2 onwards with value inversion
    for i in range(2, n):
        processed_row = []
        input_row = input_grid[i]
        for val in input_row:
            if val == 0:
                processed_row.append(primary_non_zero)
            elif val == primary_non_zero:
                processed_row.append(0)
            else:
                # Assuming only 0 and the primary non-zero exist based on examples
                # If other numbers could exist, rule needs clarification
                processed_row.append(val) # Keep other values unchanged? Or default to 0?
        modified_base_grid[i] = processed_row

    # --- Step 3: Construct the intermediate grid (N x 2N) ---
    # Horizontally duplicate each row of the modified_base_grid
    tiled_rows_grid = []
    for i in range(n):
        row = modified_base_grid[i]
        doubled_row = row + row
        tiled_rows_grid.append(doubled_row)

    # --- Step 4: Construct the final output grid (2N x 2N) ---
    # Vertically duplicate the tiled_rows_grid
    output_grid = tiled_rows_grid + tiled_rows_grid

    return output_grid