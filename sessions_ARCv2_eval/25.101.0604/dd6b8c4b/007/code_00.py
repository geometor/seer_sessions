"""
Transforms an 11x11 input grid based on a specific central 3x3 pattern and its
12 immediate border neighbors.

1.  Initialize an output_grid as a deep copy of the input_grid.
2.  **Primary Transformation (Central Pattern):**
    a.  Define the target pattern_region as the 3x3 subgrid
        [[3,3,3],[3,2,3],[3,3,3]] located at rows 4-6, columns 4-6 (slice
        [4:7, 4:7]) in the input_grid.
    b.  Check if the subgrid at the target location in the input_grid exactly
        matches the pattern_region.
    c.  If the pattern matches:
        i.  Identify the 12 border_neighbor cells surrounding the pattern_region
            using their fixed coordinates.
        ii. Count how many of these 12 border_neighbor cells contain the value 6
            in the input_grid. Store this count as count6.
        iii. Determine the appropriate transformed_pattern based on count6:
            *   If count6 is exactly 0, the transformed_pattern is
                [[9,9,9],[9,2,3],[3,3,3]].
            *   Else if count6 is exactly 11, the transformed_pattern is
                [[9,9,3],[3,2,3],[3,3,3]].
            *   Else (if count6 is any value from 1 to 10, or 12), the
                transformed_pattern is [[9,9,9],[9,9,9],[9,9,9]].
        iv. Replace the 3x3 subgrid at rows 4-6, columns 4-6 in the output_grid
            with the determined transformed_pattern.
3.  Return the output_grid.
    (Note: This implementation only covers the primary transformation described
    above. It does not implement the secondary '9 -> 7' transformation observed
    in the examples, as the rule for that transformation is currently unknown.)
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a transformation to a central 3x3 pattern in the grid based on
    the count of '6's in its 12 immediate border neighbors.

    Args:
        input_grid: An 11x11 grid represented as a list of lists of integers.

    Returns:
        A new 11x11 grid with the transformation applied, or a copy of the
        input if the target pattern is not found or conditions aren't met.
    """
    # initialize output_grid as a deep copy to avoid modifying the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # --- Step 2: Primary Transformation (Central Pattern) ---

    # Define the target pattern and its location indices (start inclusive, end exclusive)
    pattern_rows_start, pattern_rows_end = 4, 7
    pattern_cols_start, pattern_cols_end = 4, 7
    target_pattern = [
        [3, 3, 3],
        [3, 2, 3],
        [3, 3, 3]
    ]

    # Check grid dimensions are sufficient for the pattern and its neighbors
    if rows < pattern_rows_end or cols < pattern_cols_end or pattern_rows_start < 0 or pattern_cols_start < 0:
        return output_grid # Cannot perform check if grid is too small

    # Extract the actual subgrid from the input grid at the target location
    actual_subgrid = [
        row[pattern_cols_start:pattern_cols_end]
        for row in input_grid[pattern_rows_start:pattern_rows_end]
    ]

    # Check if the extracted subgrid matches the target pattern
    if actual_subgrid == target_pattern:
        # Define coordinates of the 12 border neighbors relative to the top-left of the grid
        neighbor_coords = [
            (3, 4), (3, 5), (3, 6),  # Top neighbors
            (7, 4), (7, 5), (7, 6),  # Bottom neighbors
            (4, 3), (5, 3), (6, 3),  # Left neighbors
            (4, 7), (5, 7), (6, 7)   # Right neighbors
        ]

        # Count the number of 6s among the border neighbors
        count6 = 0
        for r, c in neighbor_coords:
            # Check bounds (important if grid size wasn't guaranteed 11x11)
            if 0 <= r < rows and 0 <= c < cols:
                if input_grid[r][c] == 6:
                    count6 += 1

        # Determine the transformation pattern based on the specific value of count6
        transformed_pattern = None
        if count6 == 0:
            # Condition i: Exactly 0 sixes
             transformed_pattern = [
                 [9, 9, 9],
                 [9, 2, 3],
                 [3, 3, 3]
             ]
        elif count6 == 11:
             # Condition ii: Exactly 11 sixes
             transformed_pattern = [
                 [9, 9, 3],
                 [3, 2, 3],
                 [3, 3, 3]
             ]
        else: # Includes count6 = 1 to 10, and count6 = 12 based on observed examples
             # Condition iii: Any other count of sixes
             transformed_pattern = [
                 [9, 9, 9],
                 [9, 9, 9],
                 [9, 9, 9]
             ]

        # Apply the determined transformation to the output grid
        if transformed_pattern: # Should always be true if pattern matched
            for r_idx, row_val in enumerate(transformed_pattern):
                for c_idx, cell_val in enumerate(row_val):
                    # Calculate the corresponding row and column in the output grid
                    output_row = pattern_rows_start + r_idx
                    output_col = pattern_cols_start + c_idx
                    # Update the cell (bounds check again for safety)
                    if 0 <= output_row < rows and 0 <= output_col < cols:
                        output_grid[output_row][output_col] = cell_val

    # --- Step 3: Secondary Transformation (Unresolved Rule) ---
    # Not implemented as the rule is unknown.

    # --- Step 4: Return the result ---
    return output_grid