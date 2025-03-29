import numpy as np

"""
Transforms the input grid based on a conditional replacement rule operating on a 3x3 partitioned structure.

1.  Identifies a 3x3 subgrid structure within the input grid. The structure is defined by horizontal and vertical lines of a single, non-background color (the 'separator color'). Assumes the background color is 0.
2.  Extracts the central subgrid (at index 1, 1).
3.  Identifies the single primary color 'P' present within the central subgrid, excluding the background color and the separator color. This color 'P' acts as the 'trigger color'.
4.  If the central subgrid does not contain exactly one such primary color P (e.g., it's empty, contains only background/separator, or multiple colors), the function returns the original input grid unchanged.
5.  Creates a copy of the input grid to serve as the output grid.
6.  Iterates through the subgrids in the top two rows of the 3x3 structure (row indices 0 and 1).
7.  For each subgrid at index (r, c) in these top two rows:
    a. It examines the subgrid directly below it in the *input* grid, at index (r+1, c). Let this be 'subgrid_below'.
    b. It checks if any pixel within 'subgrid_below' matches the trigger color P.
    c. If the trigger color P *is* found in 'subgrid_below', the content of the current subgrid (r, c) in the *output* grid is replaced entirely by the content of 'subgrid_below' from the *input* grid.
    d. If the trigger color P is *not* found in 'subgrid_below', the content of the current subgrid (r, c) in the *output* grid remains unchanged (it keeps the original content from the input grid).
8.  Subgrids in the bottom row (row index 2) are never modified.
9.  Returns the potentially modified output grid.
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
            if separator_color == -1:
                separator_color = unique_colors[0]
            if unique_colors[0] == separator_color:
                 separator_rows.append(r)

    # If no potential separator rows found, fail.
    if not separator_rows:
        return None, -1, -1, None, background_color
        
    # If separator_color wasn't assigned (e.g., only background rows found), fail.
    if separator_color == -1:
        # Try finding separator color from columns if rows didn't work
        for c in range(cols):
             unique_colors_col = np.unique(grid[:, c])
             if len(unique_colors_col) == 1 and unique_colors_col[0] != background_color:
                  if separator_color == -1:
                      separator_color = unique_colors_col[0]
                      break # Found potential separator from columns
        if separator_color == -1: # Still no separator color found
             return None, -1, -1, None, background_color
        # Re-find separator rows using the color found from columns
        separator_rows = []
        for r in range(rows):
            unique_colors = np.unique(grid[r, :])
            if len(unique_colors) == 1 and unique_colors[0] == separator_color:
                 separator_rows.append(r)


    # Find potential separator columns matching the determined separator color
    for c in range(cols):
        unique_colors = np.unique(grid[:, c])
        # Check if the column consists solely of the separator color
        if len(unique_colors) == 1 and unique_colors[0] == separator_color:
             separator_cols.append(c)
        # Allow for columns that contain background color AND the separator color,
        # but only if the separator color exists in that column. This handles cases
        # where separator lines might be interrupted by the grid edge if subgrids touch the edge.
        # This check is less strict and might need refinement based on more examples.
        # For now, sticking to the strict single-color column check.
        # elif separator_color in unique_colors and background_color in unique_colors and len(unique_colors) == 2:
        #      separator_cols.append(c) # Less strict - consider refining

    # Expect exactly 2 separator rows and 2 separator columns for a 3x3 grid
    if len(separator_rows) != 2 or len(separator_cols) != 2:
        # print(f"Debug: Found {len(separator_rows)} rows, {len(separator_cols)} cols. Separator: {separator_color}")
        return None, -1, -1, None, background_color

    # Determine subgrid dimensions from the first separator lines
    subgrid_h = separator_rows[0]
    subgrid_w = separator_cols[0]

    # Check for positive dimensions
    if subgrid_h <= 0 or subgrid_w <= 0:
         return None, -1, -1, None, background_color

    # Verify that the second separator lines are positioned correctly for uniform subgrids
    # Check if grid structure is consistent
    if separator_rows[1] != 2 * subgrid_h + 1 or \
       separator_cols[1] != 2 * subgrid_w + 1:
        # Allow for edge case where subgrid height/width might be 0 (only separators exist)
        # This shouldn't happen with valid ARC grids usually.
        # print(f"Debug: Inconsistent spacing. H:{subgrid_h}, W:{subgrid_w}, R:{separator_rows}, C:{separator_cols}")
        return None, -1, -1, None, background_color

    # Verify overall grid dimensions match the structure
    expected_rows = 3 * subgrid_h + 2
    expected_cols = 3 * subgrid_w + 2
    if rows != expected_rows or cols != expected_cols:
         # print(f"Debug: Dimension mismatch. Expected ({expected_rows},{expected_cols}), got ({rows},{cols})")
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
    # Handle cases where subgrid dimensions might be 0
    if r_start >= r_end or c_start >= c_end:
        return np.array([[]], dtype=grid.dtype).reshape(0, 0) # Return empty 2D array
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
    central_pattern = _get_subgrid(grid, central_boundaries)

    # Step 3: Identify the trigger color (P) in the central pattern
    # Handle empty central pattern case
    if central_pattern.size == 0:
         # print("Warning: Central subgrid is empty. Returning original grid.")
         return input_grid
         
    unique_pattern_colors = np.unique(central_pattern)
    # Filter out background and separator colors to find pattern-specific colors
    pattern_colors = [c for c in unique_pattern_colors if c != background_color and c != separator_color]

    # Step 4: Check if exactly one unique trigger color exists
    if len(pattern_colors) != 1:
        # If no single trigger color is found, return the original grid unchanged
        # print(f"Warning: Central subgrid does not define a single trigger color (found {pattern_colors}). Returning original grid.")
        return input_grid

    trigger_color = pattern_colors[0]

    # Step 5 & 6: Iterate through subgrids in the top two rows (r=0, 1)
    for r in range(2): # Iterate through row indices 0 and 1
        for c in range(3): # Iterate through column indices 0, 1, 2
            # Step 7a: Get the subgrid directly below (r+1, c) from the *input* grid
            below_boundaries = boundaries[r+1][c]
            subgrid_below = _get_subgrid(grid, below_boundaries)
            
            # Handle case where subgrid below might be empty
            if subgrid_below.size == 0:
                 continue # Nothing to check or copy, skip to next subgrid

            # Step 7b: Check if the trigger color P exists in the subgrid below
            if np.any(subgrid_below == trigger_color):
                # Step 7c: If trigger found, replace the current subgrid (r, c) in the output grid
                # with the content of the subgrid below (r+1, c) from the input grid.
                current_boundaries = boundaries[r][c]
                cr_start, cr_end, cc_start, cc_end = current_boundaries

                # Ensure dimensions match before assignment (should always match if structure is valid)
                # Target slice in output grid:
                target_slice = output_grid[cr_start:cr_end, cc_start:cc_end]
                
                if target_slice.shape == subgrid_below.shape:
                    output_grid[cr_start:cr_end, cc_start:cc_end] = subgrid_below
                else:
                    # Log an error if shapes mismatch, indicates an issue with structure parsing or assumptions
                    print(f"Error: Shape mismatch during replacement at subgrid ({r},{c}). Target shape {target_slice.shape}, Source shape {subgrid_below.shape}. Skipping replacement.")

            # Step 7d: If trigger color is not found below, the subgrid (r, c) in output_grid
            # remains unchanged (because output_grid started as a copy of grid).

    # Step 8: Subgrids in the last row (r=2) are implicitly unchanged.

    # Step 9: Convert the final numpy array back to a list of lists for the expected output format
    return output_grid.tolist()