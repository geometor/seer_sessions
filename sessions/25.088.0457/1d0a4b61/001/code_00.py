import numpy as np

"""
Identifies a repeating pattern within a grid, ignoring noise (white pixels, value 0),
and reconstructs the grid by tiling this pattern inside a 1-pixel blue border.

1.  Determine the grid dimensions (Height H, Width W).
2.  Identify the repeating pattern's period, `p`. This is done by finding the 
    smallest integer `p >= 1` such that the subgrid `input[1:1+p, 1:1+p]` is 
    consistent with the subgrids to its right (`input[1:1+p, 1+p:1+2*p]`) and 
    below it (`input[1+p:1+2*p, 1:1+p]`), ignoring any white (0) pixels during 
    the comparison. This assumes the top-left `p x p` area inside the border is 
    representative and potentially noise-free enough to define the pattern.
3.  Extract the canonical `p x p` pattern unit, `P`, from the top-left corner 
    inside the border: `P = input[1 : 1+p, 1 : 1+p]`.
4.  Create a new output grid of the same dimensions H x W.
5.  Set the border of the output grid (row 0, row H-1, column 0, column W-1) 
    to blue (color 1).
6.  Fill the interior of the output grid (rows 1 to H-2, columns 1 to W-2) 
    by repeating the pattern unit `P`. For each cell `(r, c)` where 
    `1 <= r < H-1` and `1 <= c < W-1`, set the output cell color to 
    `output[r, c] = P[(r-1) % p, (c-1) % p]`.
7.  Return the completed output grid as a list of lists.
"""

def transform(input_grid_list):
    """
    Transforms the input grid by finding a repeating pattern, ignoring noise (0s),
    and reconstructing the grid by tiling the pattern within a blue border.

    Args:
        input_grid_list: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
        
    Raises:
        ValueError: If the pattern period cannot be determined.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    H, W = input_grid.shape

    if H < 3 or W < 3:
        # Not large enough for a border and an interior pattern
        return input_grid_list # Or handle as an error/edge case

    # --- Step 2: Identify the pattern period 'p' ---
    # Iterate through possible periods starting from 1.
    # Check consistency between the top-left block and the blocks to its right and below,
    # ignoring any white (0) pixels.
    period = None
    for p in range(1, max(H - 2, W - 2)): # Period cannot be larger than the inner grid dimensions
        # Check if there's enough space to verify this period
        can_check_right = (1 + 2 * p <= W - 1)
        can_check_down = (1 + 2 * p <= H - 1)
        
        if not (can_check_right and can_check_down):
            # If p is too large to even check the first repetition block, it cannot be the period.
            # Or, if the grid is small, maybe p is the full inner width/height? This needs care.
            # For now, only consider periods verifiable by checking the first repeat block.
             if p == max(H - 2, W - 2) and period is None: 
                 # If we reached the max possible p and found nothing, check if the entire inner grid is the pattern
                 if H - 2 == W - 2:
                     period = H - 2 # Assume full inner grid is the pattern if square
                 # else: Cannot determine period for non-square full inner grid patterns easily this way
             continue # Try next smaller p if not max, or stop if max

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
        # Only check vertical if horizontal was consistent, avoids unnecessary checks
        if h_consistent: 
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
             # If horizontal wasn't consistent, this 'p' is not the period.
            v_consistent = False

        # If both horizontal and vertical checks passed (ignoring 0s), we found the smallest period
        if h_consistent and v_consistent:
            period = p
            break # Exit the loop once the smallest period is found

    # Handle case where no period was found
    if period is None:
        # Check if the entire inner grid could be the pattern period (if H-2 == W-2)
        inner_dim = H - 2
        if H == W and inner_dim > 0:
             # If square, maybe the whole inner part is the pattern?
             period = inner_dim
             # print(f"Warning: Standard period check failed. Assuming full inner grid ({period}x{period}) is the pattern.")
        else:
             raise ValueError(f"Could not determine pattern period for grid size {H}x{W}. Check failed up to p={max(H - 2, W - 2) -1}.")


    # --- Step 3: Extract the canonical pattern unit ---
    # Assumes the top-left p x p block inside the border is the correct pattern source.
    p = period
    pattern_unit = input_grid[1 : 1+p, 1 : 1+p]

    # --- Step 4: Create the output grid ---
    output_grid = np.zeros_like(input_grid)

    # --- Step 5: Set the blue border (color 1) ---
    output_grid[0, :] = 1
    output_grid[H-1, :] = 1
    output_grid[:, 0] = 1
    output_grid[:, W-1] = 1

    # --- Step 6: Fill the interior by tiling the pattern unit ---
    for r in range(1, H - 1):
        for c in range(1, W - 1):
            # Calculate the corresponding index within the pattern unit using modulo arithmetic
            # Adjust for 1-based indexing of the inner grid vs 0-based indexing of the pattern
            pattern_r = (r - 1) % p
            pattern_c = (c - 1) % p
            # Assign the color from the pattern unit
            output_grid[r, c] = pattern_unit[pattern_r, pattern_c]

    # --- Step 7: Return the completed output grid ---
    # Convert back to list of lists for the required output format
    return output_grid.tolist()