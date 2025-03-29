import numpy as np

"""
Transforms the input grid based on a conditional replacement rule operating on a 3x3 partitioned structure.

1.  Identifies a 3x3 subgrid structure within the input grid. The structure is defined by horizontal and vertical lines of a single, non-background color (the 'separator color').
2.  Extracts the pattern 'C' from the central subgrid (at index 1, 1).
3.  Identifies the single primary color 'P' present within pattern C, excluding the background color (assumed to be 0) and the separator color. This color 'P' acts as the 'trigger color'.
4.  If the central subgrid C does not contain exactly one such primary color P (e.g., it's empty, contains only background/separator, or multiple colors), the function returns the original input grid unchanged.
5.  Creates a copy of the input grid to serve as the output grid.
6.  Iterates through the subgrids in the top two rows of the 3x3 structure (row indices 0 and 1).
7.  For each subgrid at index (r, c) in these top two rows, it examines the subgrid directly below it, at index (r+1, c).
8.  If any pixel within the subgrid below (r+1, c) matches the trigger color P, the content of the current subgrid (r, c) in the output grid is replaced entirely by the central pattern C.
9.  If the subgrid below (r+1, c) does not contain the trigger color P, the content of the current subgrid (r, c) remains unchanged in the output grid.
10. Subgrids in the bottom row (row index 2) are never modified.
11. Returns the potentially modified output grid.
"""

def _find_grid_structure(grid):
    """
    Identifies the separator color, subgrid dimensions, and boundaries.
    Assumes a 3x3 grid separated by single-pixel lines of a uniform color.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        tuple: (separator_color, subgrid_h, subgrid_w, boundaries, background_color)
               boundaries is a 3x3 list of tuples (r_start, r_end, c_start, c_end).
               Returns (None, -1, -1, None, -1) if structure is not found or invalid.
    """
    rows, cols = grid.shape
    separator_color = -1
    separator_rows = []
    separator_cols = []
    background_color = 0 # Standard ARC background

    # Find potential separator color and rows by checking for monochromatic rows
    # not matching the background color.
    for r in range(rows):
        unique_colors = np.unique(grid[r, :])
        if len(unique_colors) == 1 and unique_colors[0] != background_color:
            # Assign the first such color found as the potential separator color
            if separator_color == -1:
                separator_color = unique_colors[0]
            # If the row color matches the potential separator color, add its index
            if unique_colors[0] == separator_color:
                 separator_rows.append(r)

    # If no separator color found from rows, or separator color is invalid, fail.
    if separator_color == -1:
        return None, -1, -1, None, background_color

    # Find potential separator columns matching the determined separator color
    for c in range(cols):
        unique_colors = np.unique(grid[:, c])
        if len(unique_colors) == 1 and unique_colors[0] == separator_color:
             separator_cols.append(c)

    # Expect exactly 2 separator rows and 2 separator columns for a 3x3 grid
    if len(separator_rows) != 2 or len(separator_cols) != 2:
        return None, -1, -1, None, background_color

    # Determine subgrid dimensions from the first separator lines
    subgrid_h = separator_rows[0]
    subgrid_w = separator_cols[0]
    
    # Check for positive dimensions
    if subgrid_h <= 0 or subgrid_w <= 0:
         return None, -1, -1, None, background_color

    # Verify that the second separator lines are positioned correctly for uniform subgrids
    if separator_rows[1] != 2 * subgrid_h + 1 or separator_cols[1] != 2 * subgrid_w + 1:
        return None, -1, -1, None, background_color

    # Verify overall grid dimensions match the structure
    expected_rows = 3 * subgrid_h + 2
    expected_cols = 3 * subgrid_w + 2
    if rows != expected_rows or cols != expected_cols:
         return None, -1, -1, None, background_color

    # Calculate subgrid boundaries (top-left inclusive, bottom-right exclusive)
    boundaries = [[(0, 0, 0, 0) for _ in range(3)] for _ in range(3)]
    for r_idx in range(3):
        r_start = r_idx * (subgrid_h + 1)
        r_end = r_start + subgrid_h
        for c_idx in range(3):
            c_start = c_idx * (subgrid_w + 1)
            c_end = c_start + subgrid_w
            boundaries[r_idx][c_idx] = (r_start, r_end, c_start, c_end)

    return separator_color, subgrid_h, subgrid_w, boundaries, background_color


def _get_subgrid(grid, boundaries):
    """Extracts a subgrid view from the main grid based on boundaries."""
    r_start, r_end, c_start, c_end = boundaries
    return grid[r_start:r_end, c_start:c_end]


def transform(input_grid):
    """
    Applies the conditional subgrid replacement transformation.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_grid = grid.copy()

    # Step 1: Identify the grid structure (separator, dimensions, boundaries)
    separator_color, subgrid_h, subgrid_w, boundaries, background_color = _find_grid_structure(grid)

    # If structure is invalid or not found, return the original grid
    if boundaries is None:
        # print("Warning: Could not determine grid structure. Returning original grid.")
        return input_grid

    # Step 2: Extract the central subgrid pattern (C)
    central_boundaries = boundaries[1][1]
    replacement_pattern = _get_subgrid(grid, central_boundaries)

    # Step 3: Identify the trigger color (P) in the central pattern
    unique_pattern_colors = np.unique(replacement_pattern)
    # Filter out background and separator colors to find pattern-specific colors
    pattern_colors = [c for c in unique_pattern_colors if c != background_color and c != separator_color]

    # Step 4: Check if exactly one unique trigger color exists
    if len(pattern_colors) != 1:
        # If no single trigger color is found, return the original grid unchanged
        # print("Warning: Central subgrid does not define a single trigger color. Returning original grid.")
        return input_grid

    trigger_color = pattern_colors[0]

    # Step 5 & 6: Iterate through subgrids in the top two rows (r=0, 1)
    for r in range(2): # Iterate through row indices 0 and 1
        for c in range(3): # Iterate through column indices 0, 1, 2
            # Step 7: Examine the subgrid directly below (r+1, c)
            below_boundaries = boundaries[r+1][c]
            subgrid_below = _get_subgrid(grid, below_boundaries)

            # Step 8: Check if the trigger color P exists in the subgrid below
            if np.any(subgrid_below == trigger_color):
                # If trigger found, replace the current subgrid (r, c) in the output grid
                # with the central replacement pattern C
                current_boundaries = boundaries[r][c]
                cr_start, cr_end, cc_start, cc_end = current_boundaries

                # Ensure dimensions match before assignment (should always match if structure is valid)
                if output_grid[cr_start:cr_end, cc_start:cc_end].shape == replacement_pattern.shape:
                    output_grid[cr_start:cr_end, cc_start:cc_end] = replacement_pattern
                else:
                    # Log an error if shapes mismatch, indicates an issue with structure parsing or assumptions
                    print(f"Error: Shape mismatch during replacement at subgrid ({r},{c}). Skipping replacement.")

            # Step 9: If trigger color is not found below, the subgrid (r, c) in output_grid
            # remains unchanged (because output_grid started as a copy of grid).

    # Step 10: Subgrids in the last row (r=2) are implicitly unchanged.

    # Step 11: Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()