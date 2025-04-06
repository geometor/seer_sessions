import copy

"""
Transformation rule:
1. Initialize the output grid as a deep copy of the input grid.
2. Scan the input grid rows from bottom to top.
3. Identify the first row (`r_orig`) that contains a horizontal pattern `B C...C B`, where:
    * `B` is a non-zero boundary color.
    * `C` is a non-zero central color, different from `B`.
    * `C...C` is a contiguous segment of color `C` with length `N >= 1`.
    * The `B` pixels are immediately adjacent to the `C` segment at columns `c_left` and `c_right`.
4. Once the first such pattern is found, stop scanning. Record `C`, `B`, `N`, `r_orig`, `c_left`, `c_right`.
5. If no pattern is found, return the unchanged copy of the input grid.
6. If a pattern was found, apply propagation rules:
    a. **Special Case:** If `B == 8` OR (`B == 2` AND `N > 1`):
        - Add color `C` at `(r_orig - 3, c_left - 1)` (if in bounds).
        - Add color `C` at `(r_orig - 3, c_right + 1)` (if in bounds).
        - Add color `C` at `(r_orig - 2, c_left)` (if in bounds).
        - Add color `C` at `(r_orig - 2, c_right)` (if in bounds).
    b. **Default Case:** Otherwise:
        - Add color `C` at `(r_orig - 2, c_left)` (if in bounds).
        - Add color `C` at `(r_orig - 2, c_right)` (if in bounds).
7. Return the modified output grid.
"""

def _find_pattern(grid: list[list[int]]) -> dict | None:
    """
    Helper function to find the first occurrence (from bottom) of the B-C-B pattern.

    Args:
        grid: The input grid.

    Returns:
        A dictionary containing pattern details (C, B, N, r_orig, c_left, c_right)
        or None if no pattern is found.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for r_orig in range(rows - 1, -1, -1): # Scan rows from bottom up
        row = grid[r_orig]
        c = 0
        while c < cols:
            # Find potential start of central segment (non-zero)
            if row[c] != 0:
                central_color_C = row[c]
                start_c = c
                # Find the end of the central segment
                while c + 1 < cols and row[c + 1] == central_color_C:
                    c += 1
                end_c = c
                central_segment_length_N = end_c - start_c + 1

                # Check for left boundary pixel B (non-zero, different from C)
                c_left = start_c - 1
                if c_left >= 0:
                    boundary_color_B = row[c_left]
                    if boundary_color_B != 0 and boundary_color_B != central_color_C:
                        # Check for right boundary pixel B (must be the *same* B)
                        c_right = end_c + 1
                        if c_right < cols and row[c_right] == boundary_color_B:
                            # Pattern found!
                            return {
                                "C": central_color_C,
                                "B": boundary_color_B,
                                "N": central_segment_length_N,
                                "r_orig": r_orig,
                                "c_left": c_left,
                                "c_right": c_right,
                            }
                # Move scanner past the current segment
                c = end_c + 1
            else:
                c += 1 # Move past zero
    return None # No pattern found

def _is_within_bounds(r, c, rows, cols):
    """Checks if coordinates (r, c) are within the grid boundaries."""
    return 0 <= r < rows and 0 <= c < cols

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    rows = len(output_grid)
    cols = len(output_grid[0]) if rows > 0 else 0

    # Find the specific B-C-B pattern scanning from bottom up
    pattern_info = _find_pattern(input_grid)

    # If no pattern is found, return the original grid copy
    if not pattern_info:
        return output_grid

    # Extract pattern details
    C = pattern_info["C"]
    B = pattern_info["B"]
    N = pattern_info["N"]
    r_orig = pattern_info["r_orig"]
    c_left = pattern_info["c_left"]
    c_right = pattern_info["c_right"]

    # Apply propagation rules to add new pixels
    # Special Case: B=8 or (B=2 and N > 1)
    if B == 8 or (B == 2 and N > 1):
        # Rule 1: Add C at (r_orig - 3, c_left - 1)
        target_r, target_c = r_orig - 3, c_left - 1
        if _is_within_bounds(target_r, target_c, rows, cols):
            output_grid[target_r][target_c] = C

        # Rule 2: Add C at (r_orig - 3, c_right + 1)
        target_r, target_c = r_orig - 3, c_right + 1
        if _is_within_bounds(target_r, target_c, rows, cols):
            output_grid[target_r][target_c] = C

        # Rule 3: Add C at (r_orig - 2, c_left)
        target_r, target_c = r_orig - 2, c_left
        if _is_within_bounds(target_r, target_c, rows, cols):
            output_grid[target_r][target_c] = C

        # Rule 4: Add C at (r_orig - 2, c_right)
        target_r, target_c = r_orig - 2, c_right
        if _is_within_bounds(target_r, target_c, rows, cols):
            output_grid[target_r][target_c] = C
    # Default Case: Other B values, or B=2 and N=1
    else:
        # Rule 5: Add C at (r_orig - 2, c_left)
        target_r, target_c = r_orig - 2, c_left
        if _is_within_bounds(target_r, target_c, rows, cols):
            output_grid[target_r][target_c] = C

        # Rule 6: Add C at (r_orig - 2, c_right)
        target_r, target_c = r_orig - 2, c_right
        if _is_within_bounds(target_r, target_c, rows, cols):
            output_grid[target_r][target_c] = C

    # Return the modified grid
    return output_grid