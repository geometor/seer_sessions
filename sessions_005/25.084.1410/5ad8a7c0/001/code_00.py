import numpy as np

"""
The transformation rule analyzes the input grid for horizontally symmetric patterns of red pixels (color 2) against a white background (color 0).

1.  **Condition Check:**
    a.  Identify all red pixels in the grid.
    b.  For every red pixel at position (row, col), check the following:
        i.  If the pixel is *not* on the left edge (col 0) or right edge (col width-1), verify that its symmetric counterpart at (row, width-1-col) is also a red pixel. If not, the condition fails.
        ii. Check if any pair of symmetric red pixels are horizontally adjacent (i.e., col + 1 == width - 1 - col). If such an adjacent symmetric pair exists, the condition fails.
    c.  If any check in step 1.b fails for any red pixel, the transformation is aborted, and the original input grid is returned.
    d.  Simultaneously, track if *all* red pixels across the entire grid are located *only* at the edges (col 0 or col width-1).

2.  **Transformation (if Condition Met):**
    a.  If the condition from step 1 holds true for all red pixels:
    b.  If *all* red pixels in the original input were located *only* at the edges (as determined in step 1.d):
        i. For each row containing red pixels, fill the *entire* row with red (2) in the output grid.
    c.  If *some* red pixels were located *inward* from the edges:
        i. For each row `r` containing red pixels:
           - Find the minimum column index (`min_col`) and maximum column index (`max_col`) of red pixels *in that specific row*.
           - If this row `r` contains any non-edge red pixels (i.e., `min_col != 0` or `max_col != width-1`), fill the segment of that row from `min_col` to `max_col` (inclusive) with red (2) in the output grid.
           - Rows containing only edge red pixels remain unchanged in this case.
    d.  Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a conditional horizontal fill based on the symmetry of red pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.copy(input_np) # Start with a copy

    # Find all red pixels
    red_coords = set(tuple(coord) for coord in np.argwhere(input_np == 2))

    if not red_coords: # No red pixels, no change
        return output_grid

    condition_met = True
    all_pixels_at_edges = True

    # --- Condition Check ---
    for r, c in red_coords:
        # Check 1: Non-edge pixels must have a symmetric partner
        if c != 0 and c != width - 1:
            all_pixels_at_edges = False # Found a non-edge pixel
            if (r, width - 1 - c) not in red_coords:
                condition_met = False
                # print(f"Debug: Symmetry failed at ({r},{c}). Partner ({r},{width-1-c}) not found.")
                break

        # Check 2: Adjacent symmetric pairs are disallowed
        # This happens when c and width-1-c are adjacent, meaning c+1 = width-1-c
        if c + 1 == width - 1 - c:
             # Check if both pixels of the adjacent pair are actually red (already implicitly true since we iterate over red_coords)
             # but this condition itself signals the failure case described
             condition_met = False
             # print(f"Debug: Adjacent symmetry failed at ({r},{c}) and ({r},{c+1}).")
             break

    if not condition_met:
        # print("Debug: Condition not met, returning original grid.")
        return output_grid # Return the initial copy (unchanged)

    # --- Transformation (Condition IS Met) ---
    # print(f"Debug: Condition met. All pixels at edges: {all_pixels_at_edges}")
    rows_with_red = sorted(list(set(r for r, c in red_coords)))

    for r in rows_with_red:
        # Get columns for this specific row from the original input
        row_cols = [c for rr, c in red_coords if rr == r]
        if not row_cols: # Should not happen if r is from rows_with_red, but good practice
            continue

        min_col = min(row_cols)
        max_col = max(row_cols)

        if all_pixels_at_edges:
            # Fill the entire row
            # print(f"Debug: Filling entire row {r}")
            output_grid[r, :] = 2
        else:
            # Only fill segment if the row contains non-edge pixels
            if min_col != 0 or max_col != width - 1:
                 # print(f"Debug: Filling segment in row {r} from {min_col} to {max_col}")
                 output_grid[r, min_col : max_col + 1] = 2
            # else:
                 # print(f"Debug: Row {r} has only edge pixels, leaving unchanged in mixed mode.")


    return output_grid.tolist() # Convert back to list of lists if needed
