import numpy as np

"""
Identifies a repeating pattern within a grid, ignoring noise (white pixels, value 0), 
reconstructs the 'clean' version of the pattern by observing all non-noise pixels 
across the grid, and then reconstructs the grid by tiling this clean pattern 
inside a 1-pixel blue border.

1.  Determine the grid dimensions (Height H, Width W). Handle grids too small 
    for a border and pattern.
2.  Identify the repeating pattern's period, `p`. Find the smallest integer `p >= 1` 
    such that the non-white pixels in the subgrid `input[1:1+p, 1:1+p]` are 
    consistent with the non-white pixels in the subgrids to its right 
    (`input[1:1+p, 1+p:1+2*p]`) and below it (`input[1+p:1+2*p, 1:1+p]`).
    Handle cases where a period cannot be determined.
3.  Reconstruct the canonical `p x p` pattern unit, `clean_pattern_unit`. 
    Initialize a `p x p` grid with white (0). Iterate through all cells `(r, c)` 
    in the interior of the input grid (`1 <= r < H-1`, `1 <= c < W-1`). If 
    `input[r, c]` is not white (0), determine its position `(pr, pc)` within 
    the pattern (`pr = (r-1)%p`, `pc = (c-1)%p`). If the corresponding cell 
    `clean_pattern_unit[pr, pc]` is still white (0), update it with the value 
    from `input[r, c]`. This ensures the clean pattern is built from the first 
    observed non-white pixel for each pattern position.
4.  Create a new output grid of the same dimensions H x W.
5.  Set the border of the output grid (row 0, row H-1, column 0, column W-1) 
    to blue (color 1).
6.  Fill the interior of the output grid (rows 1 to H-2, columns 1 to W-2) 
    by tiling the reconstructed `clean_pattern_unit`. For each cell `(r, c)` 
    where `1 <= r < H-1` and `1 <= c < W-1`, set the output cell color to 
    `output[r, c] = clean_pattern_unit[(r-1) % p, (c-1) % p]`.
7.  Return the completed output grid as a list of lists.
"""

def determine_period(input_grid):
    """
    Determines the period of the repeating pattern within the input grid's interior,
    ignoring white (0) pixels.
    """
    H, W = input_grid.shape
    if H < 3 or W < 3:
        return None # Not large enough

    period = None
    # Iterate through possible periods starting from 1.
    # Check consistency between the top-left block and the blocks to its right and below,
    # ignoring any white (0) pixels.
    max_possible_p = max(1, H - 2, W - 2) # Ensure max_possible_p is at least 1

    for p in range(1, max_possible_p + 1):
        # Check if there's enough space to verify this period by comparing adjacent blocks
        # Need at least 1+2*p rows/cols within the border
        can_check_right = (1 + 2 * p <= W - 1)
        can_check_down = (1 + 2 * p <= H - 1)

        # If we can't check adjacent blocks, this 'p' cannot be confirmed using this method.
        # However, if p equals the full inner dimension and the grid is large enough,
        # it *could* be the period. We'll handle this possibility after the loop if no smaller period is found.
        if not (can_check_right and can_check_down):
             if p == H - 2 and p == W - 2 and p > 0: # Check if it's the full square inner grid
                 # We can tentatively accept this as the period if no smaller one was found.
                 # This case will be handled if the loop finishes without finding a period.
                 pass # Don't break, maybe a smaller p works partially? No, proceed.
             continue # Cannot verify this p by comparing neighbors

        # Extract the potential pattern and its neighbours
        pattern = input_grid[1 : 1+p, 1 : 1+p]
        pattern_right = input_grid[1 : 1+p, 1+p : 1+2*p]
        pattern_down = input_grid[1+p : 1+2*p, 1 : 1+p]

        # Check horizontal consistency (ignore 0s)
        h_consistent = True
        for r in range(p):
            for c in range(p):
                v1 = pattern[r, c]
                v2 = pattern_right[r, c]
                # Compare only if both pixels are non-zero (not noise)
                if v1 != 0 and v2 != 0 and v1 != v2:
                    h_consistent = False
                    break
            if not h_consistent: break

        # Check vertical consistency (ignore 0s)
        v_consistent = True
        if h_consistent: # Only check vertical if horizontal was consistent
            for r in range(p):
                for c in range(p):
                    v1 = pattern[r, c]
                    v2 = pattern_down[r, c]
                    # Compare only if both pixels are non-zero
                    if v1 != 0 and v2 != 0 and v1 != v2:
                        v_consistent = False
                        break
                if not v_consistent: break
        else:
            v_consistent = False # If horizontal wasn't consistent, vertical doesn't matter

        # If both checks passed (ignoring 0s), we found the smallest period
        if h_consistent and v_consistent:
            period = p
            break # Exit the loop once the smallest period is found

    # If the loop finished without finding a period by comparing adjacent blocks
    if period is None:
        # Check if the entire inner grid could be the pattern period
        inner_h, inner_w = H - 2, W - 2
        if inner_h > 0 and inner_w > 0:
            # If the only possibility left is the full inner grid size
            period = max(inner_h, inner_w) # A simple guess, maybe incorrect for non-square tiling
            # More accurately, the period must divide both inner_h and inner_w if it tiles perfectly.
            # Let's assume the largest dimension dictates the period if comparison failed.
            # A better approach might be needed for complex cases.
            # For now, assume the largest inner dimension if square, or maybe just inner_h? Let's try max.
            # Revisit: If comparison failed, maybe the top-left wasn't clean.
            # A better heuristic might be needed, but let's assume largest dimension works for now.
             if inner_h == inner_w:
                 period = inner_h # If inner grid is square, period is its dimension
             else:
                 # This case is ambiguous with the current check.
                 # Let's default to None, forcing an error later if needed.
                 period = None
                 # Or maybe try finding GCD of inner_h, inner_w? Too complex for now.

    return period

def reconstruct_clean_pattern(input_grid, p):
    """
    Reconstructs the 'clean' p x p pattern unit by observing all non-white pixels
    in the interior of the input grid.
    """
    H, W = input_grid.shape
    # Initialize the clean pattern with white (0)
    clean_pattern_unit = np.zeros((p, p), dtype=int)
    # Keep track of which pattern cells have been assigned a non-white color
    pattern_assigned = np.zeros((p, p), dtype=bool)

    # Iterate through the interior of the input grid
    for r in range(1, H - 1):
        for c in range(1, W - 1):
            value = input_grid[r, c]
            # If the pixel is not noise (white)
            if value != 0:
                # Calculate its position within the p x p pattern
                pattern_r = (r - 1) % p
                pattern_c = (c - 1) % p
                # If this position in the clean pattern hasn't been assigned yet
                if not pattern_assigned[pattern_r, pattern_c]:
                    # Assign the value from the input grid
                    clean_pattern_unit[pattern_r, pattern_c] = value
                    # Mark this pattern position as assigned
                    pattern_assigned[pattern_r, pattern_c] = True
                # Optional: Add consistency check here if needed
                # elif clean_pattern_unit[pattern_r, pattern_c] != value:
                #     print(f"Warning: Inconsistent pattern value at ({r},{c}) -> pattern ({pattern_r},{pattern_c}). Found {value}, expected {clean_pattern_unit[pattern_r, pattern_c]}")
                #     pass # Keep the first value found

    return clean_pattern_unit


def transform(input_grid_list):
    """
    Transforms the input grid by finding a repeating pattern, reconstructing 
    its clean version by ignoring noise (0s), and reconstructing the grid 
    by tiling the clean pattern within a blue border.

    Args:
        input_grid_list: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.

    Raises:
        ValueError: If the grid dimensions are too small or the pattern period 
                    cannot be determined.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    H, W = input_grid.shape

    # --- Step 1: Check Grid Size ---
    if H < 3 or W < 3:
        # Not large enough for a border and an interior pattern.
        # Depending on task requirements, could return input, error, or specific output.
        # Let's raise an error as the described transformation isn't possible.
        raise ValueError(f"Grid size {H}x{W} is too small for border and pattern.")

    # --- Step 2: Identify the pattern period 'p' ---
    period = determine_period(input_grid)

    # Handle case where no period was found
    if period is None:
        raise ValueError(f"Could not determine pattern period for grid size {H}x{W}.")

    p = period

    # --- Step 3: Reconstruct the clean pattern unit ---
    clean_pattern_unit = reconstruct_clean_pattern(input_grid, p)

    # --- Step 4: Create the output grid ---
    output_grid = np.zeros_like(input_grid)

    # --- Step 5: Set the blue border (color 1) ---
    output_grid[0, :] = 1
    output_grid[H-1, :] = 1
    output_grid[:, 0] = 1
    output_grid[:, W-1] = 1

    # --- Step 6: Fill the interior by tiling the clean pattern unit ---
    for r in range(1, H - 1):
        for c in range(1, W - 1):
            # Calculate the corresponding index within the pattern unit using modulo arithmetic
            pattern_r = (r - 1) % p
            pattern_c = (c - 1) % p
            # Assign the color from the reconstructed clean pattern unit
            output_grid[r, c] = clean_pattern_unit[pattern_r, pattern_c]

    # --- Step 7: Return the completed output grid ---
    # Convert back to list of lists for the required output format
    return output_grid.tolist()