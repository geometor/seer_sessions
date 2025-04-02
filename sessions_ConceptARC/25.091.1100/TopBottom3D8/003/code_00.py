import numpy as np
from typing import Tuple, Optional, List, Set

"""
Transformation Rule:

1. Identify the unique vertical line in the input grid. This line consists of pixels of a single non-background color (`V_color`) and background pixels (0) in a single column (`C`).
2. Iterate through each row (`R`) of the grid.
3. For each row `R`, analyze the intersection point `(R, C)` and the composition of colors in the row.
4. Classify the intersection based on the row's colors:
    a. **Pure Intersection:** The row `R` contains exactly one unique non-background color `H_color`, AND the intersection pixel `grid[R, C]` has this color `H_color`. The required change is to set the intersection pixel to `V_color`.
    b. **Non-Pure Intersection:** The row `R` contains multiple unique non-background colors, AND the intersection pixel `grid[R, C]` has the vertical line's color `V_color`, AND there is exactly one *other* non-background color `H_dom_color` present in the row. The required change is to set the intersection pixel to `H_dom_color`.
5. Collect all required changes for both pure and non-pure intersections.
6. Apply the changes with priority: If any pure intersection changes were identified, apply *only* those changes. Otherwise (if no pure changes were identified), apply all the non-pure intersection changes.
7. Return the modified grid. Pixels not part of a prioritized change remain unchanged.
"""

def find_vertical_line(grid: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Finds the column index and color of the unique vertical line.
    A vertical line column contains only background (0) and one other color.
    Returns (column_index, line_color) or None if not found.
    """
    height, width = grid.shape
    for c in range(width):
        col_pixels = grid[:, c]
        # Find unique non-zero colors in the column
        non_background_pixels = col_pixels[col_pixels != 0]
        unique_colors = np.unique(non_background_pixels)
        
        # Check if there's exactly one non-background color
        if len(unique_colors) == 1:
            # Check if all pixels are either background or this unique color
            line_color = unique_colors[0]
            is_line_column = np.all((col_pixels == 0) | (col_pixels == line_color))
            if is_line_column:
                return c, line_color
    return None

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule based on vertical line intersections
    and row color composition with priority for 'pure' intersections.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    grid = np.array(input_grid, dtype=np.int8)
    # Create a copy to modify, which will become the output
    output_grid = np.copy(grid)
    height, width = grid.shape

    # 1. Identify the unique vertical line (column index C, color V_color)
    line_info = find_vertical_line(grid)
    if line_info is None:
        # If no vertical line is found (shouldn't happen based on examples), return original grid
        return input_grid 
    v_col, v_color = line_info

    # 2. Initialize lists to store required changes based on rules
    pure_rule_changes: List[Tuple[int, int, int]] = [] # Stores (row, col, new_color)
    non_pure_rule_changes: List[Tuple[int, int, int]] = [] # Stores (row, col, new_color)

    # 3. Iterate through each row to analyze intersections
    for r in range(height):
        intersect_color = grid[r, v_col]

        # 3a. Skip if the intersection point is background color
        if intersect_color == 0:
            continue

        # 3b. Analyze colors in the current row
        row = grid[r, :]
        non_background_row_pixels = row[row != 0]
        unique_row_colors: Set[int] = set(np.unique(non_background_row_pixels))

        # 4a. Check for Pure Intersection Rule
        if len(unique_row_colors) == 1:
            h_color = list(unique_row_colors)[0]
            # Condition: Row has only one non-bg color (h_color) AND intersect pixel IS h_color
            if intersect_color == h_color:
                # Store the required change: intersect pixel becomes v_color
                pure_rule_changes.append((r, v_col, v_color))

        # 4b. Check for Non-Pure Intersection Rule
        elif len(unique_row_colors) > 1:
            # Condition: Intersect pixel IS v_color
            if intersect_color == v_color:
                other_colors = unique_row_colors - {v_color}
                # Condition: Exactly one OTHER non-bg color exists in the row
                if len(other_colors) == 1:
                    h_dom_color = list(other_colors)[0]
                    # Store the required change: intersect pixel becomes h_dom_color
                    non_pure_rule_changes.append((r, v_col, h_dom_color))

    # 5. Apply Changes Based on Priority
    # 5a. If pure changes exist, apply ONLY them
    if pure_rule_changes:
        for r_change, c_change, target_color in pure_rule_changes:
            output_grid[r_change, c_change] = target_color
    # 5b. Else (no pure changes), apply non-pure changes (if any)
    elif non_pure_rule_changes:
        for r_change, c_change, target_color in non_pure_rule_changes:
            output_grid[r_change, c_change] = target_color

    # 6. Return the modified grid converted back to list of lists format
    return output_grid.tolist()