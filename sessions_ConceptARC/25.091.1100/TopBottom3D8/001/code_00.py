import numpy as np
from typing import Tuple, Optional, List, Dict, Set

"""
Transformation Rule:

1. Identify the unique vertical line in the input grid. This line consists of pixels of a single non-background color (`V_color`) and background pixels (0) in a single column (`C`).
2. Iterate through each row (`R`) of the grid.
3. For each row `R`, check if the pixel at the intersection with the vertical line (`grid[R, C]`) is non-background.
4. If it intersects, analyze the colors present in row `R`.
    a. **Pure Horizontal Line Intersection:** If row `R` contains only background pixels (0) and one other non-background color `H_color`, and the intersection pixel `grid[R, C]` is equal to `H_color`, then this is a "pure" intersection.
    b. **Non-Pure Horizontal Line Intersection:** If row `R` contains the vertical line color `V_color` at the intersection (`grid[R, C] == V_color`) and at least one *other* non-background color `H_dom_color`, this is a "non-pure" intersection. Identify `H_dom_color` (assuming only one such other color exists based on examples).
5. Collect all identified pure intersections `(R, C)` and non-pure intersections `(R, C, H_dom_color)`.
6. **Apply Transformation Priority:**
    a. If there are any pure intersections, modify the output grid only at these locations. For each pure intersection `(R, C)`, set the output pixel `output_grid[R, C]` to the vertical line color `V_color`. Ignore all non-pure intersections.
    b. If there are *no* pure intersections, but there are non-pure intersections, modify the output grid at these locations. For each non-pure intersection `(R, C, H_dom_color)`, set the output pixel `output_grid[R, C]` to the corresponding dominant horizontal color `H_dom_color`.
7. If an intersection doesn't meet the criteria for pure or non-pure transformation (or is ignored due to the priority rule), its color remains unchanged from the input.
8. Return the modified grid.
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
        non_background_pixels = col_pixels[col_pixels != 0]
        unique_colors = np.unique(non_background_pixels)
        if len(unique_colors) == 1:
            # Check if all other pixels in the column are background
            if np.all((col_pixels == 0) | (col_pixels == unique_colors[0])):
                 return c, unique_colors[0]
    return None # Should not happen based on problem description

def analyze_row_intersection(grid: np.ndarray, r: int, v_col: int, v_color: int) -> Tuple[str, Optional[int]]:
    """
    Analyzes a row `r` to determine the type of intersection with the vertical line.

    Args:
        grid: The input grid.
        r: The row index.
        v_col: The column index of the vertical line.
        v_color: The color of the vertical line.

    Returns:
        A tuple:
        - Interaction type: "pure", "non-pure", or "none".
        - Target color (if applicable):
            - For "pure", returns v_color (the color to change *to*).
            - For "non-pure", returns the dominant horizontal color H_dom_color (the color to change *to*).
            - For "none", returns None.
    """
    row = grid[r, :]
    intersection_pixel_color = grid[r, v_col]
    
    # Ignore rows where the vertical line column is background
    if intersection_pixel_color == 0:
        return "none", None

    non_background_row_pixels = row[row != 0]
    unique_non_background_colors = set(np.unique(non_background_row_pixels))

    # Check for Pure Intersection
    if len(unique_non_background_colors) == 1:
        h_color = list(unique_non_background_colors)[0]
        # The intersection pixel must match the horizontal color
        if intersection_pixel_color == h_color:
            return "pure", v_color # Target color is the vertical line's color
        else:
             # This case happens in train_2 where the intersection pixel is already
             # v_color, but the row *only* contains h_color otherwise.
             # Let's re-evaluate based on the examples.
             # train_1: intersect=2 (h), row={0,2}. output -> 1 (v). Rule: pure intersect -> v_color
             # train_3: intersect=7 (h), row={0,7}. output -> 8 (v). Rule: pure intersect -> v_color
             # train_4 (row 3): intersect=5 (h), row={0,5}. output -> 8 (v). Rule: pure intersect -> v_color
             # Okay, the original pure rule holds: if row has only 1 non-bg color (h_color) AND intersect == h_color, target is v_color.
             return "none", None


    # Check for Non-Pure Intersection
    elif len(unique_non_background_colors) > 1:
        # The intersection pixel must match the vertical line color
        if intersection_pixel_color == v_color:
            other_colors = unique_non_background_colors - {v_color}
            # Based on examples, assume only one 'other' non-background color matters
            if len(other_colors) == 1:
                h_dom_color = list(other_colors)[0]
                return "non-pure", h_dom_color # Target color is the other horizontal color
            else:
                 # Ambiguous case based on examples, treat as no change
                 return "none", None
        else:
             # Intersection pixel is non-background but not v_color, and row has multiple colors.
             # This happens in train_4, row 1. Intersect=8(v), row={0, 5(h_dom), 8(v)}.
             # The definition needs refinement. Let's revisit the rules from analysis:
             # - Pure: Row has only H_color (and 0). Intersect pixel MUST BE H_color. Output is V_color.
             # - Non-Pure: Row has V_color at intersect. Row also has H_dom_color elsewhere. Output is H_dom_color.
             # So, if intersection pixel != v_color, it cannot be a non-pure intersection eligible for change by that rule.
            return "none", None
            
    # Row only contains background? (Shouldn't happen if intersection pixel is non-background)
    return "none", None


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule:
    Finds a vertical line and horizontal lines/segments.
    Modifies the intersection pixel based on whether the horizontal line is "pure"
    (only one non-background color) or "non-pure" (contains the vertical line color
    at the intersection plus another dominant color). Pure intersections take priority
    and change the intersection to the vertical line's color. If no pure intersections
    exist, non-pure intersections change the intersection pixel to the dominant
    horizontal color.
    """
    grid = np.array(input_grid, dtype=np.int8)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # 1. Find the unique vertical line
    line_info = find_vertical_line(grid)
    if line_info is None:
        return input_grid # Should not happen in ARC tasks
    v_col, v_color = line_info

    # 2. Find all potential intersections and classify them
    pure_intersections: List[Tuple[int, int]] = [] # Stores (r, c)
    non_pure_intersections: List[Tuple[int, int, int]] = [] # Stores (r, c, h_dom_color)

    for r in range(height):
        # Check only rows where the vertical line column is non-background
        if grid[r, v_col] != 0:
            intersection_type, target_color = analyze_row_intersection(grid, r, v_col, v_color)
            
            if intersection_type == "pure":
                 # We store the target color (v_color) directly now for simplicity
                 pure_intersections.append((r, v_col, target_color)) 
            elif intersection_type == "non-pure":
                 non_pure_intersections.append((r, v_col, target_color)) # target_color is h_dom_color

    # 3. Apply transformations based on priority
    if pure_intersections: # If any pure intersections exist, process only them
        for r, c, target_color in pure_intersections:
            output_grid[r, c] = target_color # target_color is v_color here
    elif non_pure_intersections: # Otherwise, process non-pure intersections
        for r, c, target_color in non_pure_intersections:
            output_grid[r, c] = target_color # target_color is h_dom_color here
            
    # If neither list has entries, no changes are made, output_grid remains a copy of input.

    return output_grid.tolist()