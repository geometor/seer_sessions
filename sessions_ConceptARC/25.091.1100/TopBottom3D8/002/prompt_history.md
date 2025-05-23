
## train_1

**input:**
```
0 0 0 0 1 0
0 0 0 0 1 0
0 0 0 0 1 0
2 2 2 2 2 2
0 0 0 0 1 0
0 0 0 0 1 0
```


**output:**
```
0 0 0 0 1 0
0 0 0 0 1 0
0 0 0 0 1 0
2 2 2 2 1 2
0 0 0 0 1 0
0 0 0 0 1 0
```


## train_2

**input:**
```
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
4 3 4 4 4 4
0 3 0 0 0 0
0 3 0 0 0 0
```


**output:**
```
0 3 0 0 0 0
0 3 0 0 0 0
0 3 0 0 0 0
4 4 4 4 4 4
0 3 0 0 0 0
0 3 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 8 0
0 0 0 0 8 0
7 7 7 7 7 7
0 0 0 0 8 0
0 0 0 0 8 0
0 0 0 0 8 0
```


**output:**
```
0 0 0 0 8 0
0 0 0 0 8 0
7 7 7 7 8 7
0 0 0 0 8 0
0 0 0 0 8 0
0 0 0 0 8 0
```


## train_4

**input:**
```
0 8 0 0 0 0
5 8 5 5 5 5
0 8 0 0 0 0
5 5 5 5 5 5
0 8 0 0 0 0
0 8 0 0 0 0
```


**output:**
```
0 8 0 0 0 0
5 5 5 5 5 5
0 8 0 0 0 0
5 8 5 5 5 5
0 8 0 0 0 0
0 8 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception**

1.  **Grid Structure:** All examples use 6x6 grids.
2.  **Key Elements:** Each input grid features exactly one prominent vertical line and one or more prominent horizontal lines. These lines consist of a single, non-background color (white, 0).
3.  **Intersection:** The vertical and horizontal lines intersect at one or more points.
4.  **Transformation Focus:** The core transformation happens only at the intersection point(s) between the vertical and horizontal lines. The rest of the grid remains unchanged.
5.  **Transformation Logic:** The color of the intersection pixel(s) changes based on the colors of the intersecting lines and the nature of the horizontal line.
    *   If the intersection involves a "pure" horizontal line (a row containing only the background color and one other color), the intersection pixel takes the color of the vertical line. This happens in examples 1, 3, and the intersection at (3,1) in example 4.
    *   If the intersection involves a "non-pure" horizontal line (a row where the intersection pixel has the vertical line's color, but other pixels in the row have a different non-background color), the intersection pixel takes the color of the *other* non-background color present in that row. This happens in example 2.
    *   If both types of intersections occur (as in example 4), the "pure line" rule takes precedence for its intersection, and the "non-pure line" intersection remains unchanged.

**Facts**


```yaml
Examples:
  - Description: Train_1
    Input:
      Grid Size: 6x6
      Objects:
        - Type: Vertical Line
          Color: Blue (1)
          Location: Column 4
        - Type: Horizontal Line
          Color: Red (2)
          Location: Row 3
          Purity: Pure (only Red and White in the row)
      Intersection:
        - Location: (3, 4)
          Initial Color: Red (2) # Matches horizontal line color
    Output:
      Grid Size: 6x6
      Changes:
        - Location: (3, 4)
          New Color: Blue (1) # Changed to vertical line color

  - Description: Train_2
    Input:
      Grid Size: 6x6
      Objects:
        - Type: Vertical Line
          Color: Green (3)
          Location: Column 1
        - Type: Horizontal Line Segment
          Dominant Color: Yellow (4)
          Location: Row 3
          Purity: Non-pure (contains Yellow and Green)
      Intersection:
        - Location: (3, 1)
          Initial Color: Green (3) # Matches vertical line color
    Output:
      Grid Size: 6x6
      Changes:
        - Location: (3, 1)
          New Color: Yellow (4) # Changed to horizontal row's dominant color

  - Description: Train_3
    Input:
      Grid Size: 6x6
      Objects:
        - Type: Vertical Line
          Color: Azure (8)
          Location: Column 4
        - Type: Horizontal Line
          Color: Orange (7)
          Location: Row 2
          Purity: Pure (only Orange and White in the row)
      Intersection:
        - Location: (2, 4)
          Initial Color: Orange (7) # Matches horizontal line color
    Output:
      Grid Size: 6x6
      Changes:
        - Location: (2, 4)
          New Color: Azure (8) # Changed to vertical line color

  - Description: Train_4
    Input:
      Grid Size: 6x6
      Objects:
        - Type: Vertical Line
          Color: Azure (8)
          Location: Column 1
        - Type: Horizontal Line Segment (Row 1)
          Dominant Color: Gray (5)
          Location: Row 1
          Purity: Non-pure (contains Gray and Azure)
        - Type: Horizontal Line (Row 3)
          Color: Gray (5)
          Location: Row 3
          Purity: Pure (only Gray and White in the row)
      Intersections:
        - Location: (1, 1) # With non-pure row 1
          Initial Color: Azure (8) # Matches vertical line color
        - Location: (3, 1) # With pure row 3
          Initial Color: Gray (5) # Matches horizontal line color
    Output:
      Grid Size: 6x6
      Changes:
        - Location: (3, 1)
          New Color: Azure (8) # Changed to vertical line color (pure line rule applied)
        - Location: (1, 1)
          New Color: Azure (8) # No change (non-pure rule not applied because a pure rule was applicable elsewhere)

Derived Rule:
  Identify Vertical Line: Find the single column `C` containing only background (0) and one other color `V_color`.
  Identify Horizontal Lines: Find all rows `R` containing non-background colors.
    - Pure Horizontal Line: Row `R` contains only background (0) and one other color `H_color`.
    - Non-Pure Horizontal Line: Row `R` contains the pixel `(R, C)` with `V_color` and at least one other non-background color `H_dom_color`.
  Apply Transformation:
    1. Prioritize Pure Lines: If any pure horizontal line (row `R`, color `H_color`) intersects the vertical line at `(R, C)`, change the color of pixel `(R, C)` to `V_color`.
    2. Apply Non-Pure Rule (only if no pure lines intersected): If no pure horizontal lines intersect the vertical line, then for any non-pure horizontal line (row `R`, dominant color `H_dom_color`) intersecting the vertical line at `(R, C)` (where `grid[R][C] == V_color`), change the color of pixel `(R, C)` to `H_dom_color`.
    3. No Change: If an intersection exists but doesn't fit criteria 1 or 2 (e.g., the intersection on the non-pure line in train_4 when a pure line intersection also exists), it remains unchanged.
```


**Natural Language Program**

1.  Make a copy of the input grid to serve as the output grid.
2.  Identify the unique vertical line: Find the column index `C` and the non-background color `V_color` such that all pixels in column `C` are either background (0) or `V_color`.
3.  Initialize flags: `pure_intersection_found = False`.
4.  Create lists to store information about pure and non-pure horizontal lines intersecting the vertical line column `C`.
5.  Iterate through each row `R` of the grid:
    a.  Check if the pixel at `(R, C)` is non-background (i.e., part of the vertical line).
    b.  If it is, analyze the entire row `R` to determine if it's a "pure" or "non-pure" horizontal line interacting at the intersection.
    c.  Collect all non-background colors in row `R`. Let this set be `row_colors`.
    d.  If `row_colors` contains exactly one color `H_color` (and potentially the background color 0), and `grid[R][C]` is equal to `H_color`, then this is a potential "pure" horizontal line intersecting the vertical line. Store `(R, C, H_color)`.
    e.  If `row_colors` contains more than one non-background color, and `grid[R][C]` is equal to `V_color`, identify the dominant *other* non-background color `H_dom_color` in the row. Store `(R, C, H_dom_color)` as a potential "non-pure" intersection.
6.  Process pure intersections first: Iterate through the stored pure intersections `(R, C, H_color)`. For each, update the output grid at `(R, C)` to `V_color`. Set `pure_intersection_found = True`.
7.  Process non-pure intersections (only if no pure intersections were found): If `pure_intersection_found` is `False`, iterate through the stored non-pure intersections `(R, C, H_dom_color)`. For each, update the output grid at `(R, C)` to `H_dom_color`.
8.  Return the modified output grid.
```python
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
```
