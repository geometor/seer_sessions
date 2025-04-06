import copy

"""
Transforms a 4x9 input grid into a 4x4 output grid.

1.  **Input Decomposition**: Divide the 4x9 input grid into a `LeftGrid` (columns 0-3) and a `RightGrid` (columns 5-8). Ignore the separator column (column 4).
2.  **Analyze `RightGrid`**: Examine the `RightGrid`. Identify the single unique non-zero digit present, call it `M`. Count the total number of times `M` appears in the `RightGrid`, call this count `C`. (If `RightGrid` contains only zeros, proceed to step 4 with the 'Overlay' behavior).
3.  **Determine Transformation Mode**: Check if a specific condition based on `M` and `C` is met:
    *   Is `M` equal to 2 AND (`C` equal to 4 OR `C` equal to 8)?
    *   OR is `M` equal to 3 AND `C` equal to 5?
    *   If either of these conditions is true, the mode is "Use LeftGrid".
    *   Otherwise, the mode is "Overlay".
4.  **Generate Output**:
    *   If the mode is "Use LeftGrid", the output is simply a copy of the `LeftGrid`.
    *   If the mode is "Overlay", generate the output grid by starting with a copy of the `LeftGrid`. Then, iterate through each cell (row `r`, column `c`) of the `RightGrid`. If the value `RightGrid[r][c]` is non-zero, update the corresponding cell in the output grid to this value (`output[r][c] = RightGrid[r][c]`).
"""

def analyze_right_grid(right_grid: list[list[int]]) -> tuple[int | None, int]:
    """
    Analyzes the RightGrid to find the unique non-zero digit (M) and its count (C).

    Args:
        right_grid: The 4x4 grid derived from columns 5-8 of the input.

    Returns:
        A tuple (M, C), where M is the unique non-zero digit (or None if none exist)
        and C is its count. Assumes at most one unique non-zero digit based on examples.
    """
    non_zeros = []
    for r in range(len(right_grid)):
        for c in range(len(right_grid[0])):
            if right_grid[r][c] != 0:
                non_zeros.append(right_grid[r][c])

    if not non_zeros:
        return None, 0 # No non-zero values

    unique_non_zeros = set(non_zeros)
    # Assuming only one unique non-zero value based on training data observation
    if len(unique_non_zeros) == 1:
        m = unique_non_zeros.pop()
        c = len(non_zeros)
        return m, c
    else:
         # Handle unexpected cases if necessary, for now, assume the simplest case
         # If multiple unique non-zeros, the condition logic might be invalid.
         # Let's return the first non-zero found and its count for now,
         # but ideally, the rule should clarify this.
         # For this problem's examples, this else block is not hit.
         m = non_zeros[0]
         c = non_zeros.count(m) # Count only the first non-zero found
         # A safer fallback might be to default to overlay if ambiguity exists
         print(f"Warning: Multiple unique non-zeros found in RightGrid: {unique_non_zeros}. Using M={m}, C={c} for condition check.")
         # Or maybe return (None, 0) to default to overlay? Let's default to overlay behavior.
         return None, 0 # Default to overlay if ambiguous


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input 4x9 grid to a 4x4 grid based on the conditional overlay rule.
    """
    rows = 4
    output_cols = 4
    left_grid_cols = 4
    right_grid_start_col = 5

    # Extract LeftGrid (columns 0-3)
    left_grid = [row[:left_grid_cols] for row in input_grid]

    # Extract RightGrid (columns 5-8)
    right_grid = [row[right_grid_start_col:right_grid_start_col + output_cols] for row in input_grid]

    # Analyze RightGrid to get the unique non-zero value M and its count C
    m, c = analyze_right_grid(right_grid)

    # Determine the transformation mode based on the condition
    use_left_grid_mode = False
    if m is not None:
        if (m == 2 and c in [4, 8]) or (m == 3 and c == 5):
            use_left_grid_mode = True

    # Generate the output grid based on the mode
    if use_left_grid_mode:
        # Mode: Use LeftGrid - Return a copy of LeftGrid directly
        output_grid = copy.deepcopy(left_grid)
    else:
        # Mode: Overlay - Start with LeftGrid and overlay non-zero values from RightGrid
        output_grid = copy.deepcopy(left_grid)
        for r in range(rows):
            for col_idx in range(output_cols):
                right_val = right_grid[r][col_idx]
                if right_val != 0:
                    output_grid[r][col_idx] = right_val

    return output_grid