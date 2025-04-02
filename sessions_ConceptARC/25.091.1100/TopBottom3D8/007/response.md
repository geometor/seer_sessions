```python
import numpy as np
from typing import Tuple, Optional, List, Set

"""
Transformation Rule:

1.  Identify the unique vertical line in the input grid. The vertical line is defined as the unique column `C` where exactly one non-background color `V_color` appears more than once.
2.  Create a copy of the input grid to serve as the output grid.
3.  Iterate through each row `R` of the grid.
4.  Analyze the intersection point `(R, C)` and the composition of colors in row `R`.
5.  Apply changes based on two independent rules:
    a.  **Pure Rule:** If row `R` contains exactly one unique non-background color `H_color`, AND the intersection pixel `grid[R, C]` has this color `H_color`, then update the output grid at `(R, C)` to `V_color`.
    b.  **Non-Pure Rule:** If row `R` contains multiple unique non-background colors, AND the intersection pixel `grid[R, C]` has the vertical line's color `V_color`, AND there is exactly one *other* non-background color `H_dom_color` present in the row, then update the output grid at `(R, C)` to `H_dom_color`.
6.  These rules are evaluated for each intersection, and if the conditions for either rule are met, the corresponding change is applied directly to the output grid.
7.  Return the modified output grid.
"""


def find_vertical_line(grid: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Finds the column index and color of the unique vertical line.
    A vertical line is defined as the unique column C where exactly one
    non-background color V_color appears more than once.

    Args:
        grid: The input grid as a NumPy array.

    Returns:
        A tuple (column_index, line_color) or None if no such line is found.
    """
    height, width = grid.shape
    potential_lines = []
    for c in range(width):
        col = grid[:, c]
        non_bg_col = col[col != 0] # Filter out background pixels
        if len(non_bg_col) == 0:
            continue # Skip columns with only background

        # Count occurrences of each non-background color in the column
        unique_colors, counts = np.unique(non_bg_col, return_counts=True)

        # Find colors that appear more than once
        colors_more_than_once = unique_colors[counts > 1]

        # Check if exactly one color appears more than once
        if len(colors_more_than_once) == 1:
            v_color = colors_more_than_once[0]
            # Store the column index and the dominant color
            potential_lines.append({'col': c, 'color': v_color})

    # Assuming there's always exactly one such line based on ARC examples
    if len(potential_lines) == 1:
         return potential_lines[0]['col'], potential_lines[0]['color']
    elif len(potential_lines) > 1:
         # Fallback for potential ambiguity, though not seen in examples
         # Returning the first one found based on column index.
         print(f"Warning: Multiple potential vertical lines found: {potential_lines}. Using the first one (column {potential_lines[0]['col']}).")
         return potential_lines[0]['col'], potential_lines[0]['color']

    return None # No line found meeting the criteria

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule based on vertical line intersections
    and row color composition. Applies 'Pure' and 'Non-Pure' rules independently.
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
        print("Warning: No unique vertical line found based on the definition.")
        return input_grid # Return input as is
    v_col, v_color = line_info

    # 2. Iterate through each row to analyze intersections and apply rules
    for r in range(height):
        intersect_color = grid[r, v_col]

        # 2a. Skip if the intersection point is background color
        if intersect_color == 0:
            continue

        # 2b. Analyze colors in the current row
        row = grid[r, :]
        non_background_row_pixels = row[row != 0]
        # Handle rows with only background (apart from intersection) if needed
        if len(non_background_row_pixels) == 0:
             # This case implies the intersection pixel is the only non-bg pixel.
             # It doesn't fit either rule cleanly. Let's assume no change.
             continue
             
        unique_row_colors: Set[int] = set(np.unique(non_background_row_pixels))

        # 3. Check and Apply Pure Rule
        # Condition: Row has exactly one unique non-bg color (h_color) AND intersect pixel IS h_color
        if len(unique_row_colors) == 1:
            h_color = list(unique_row_colors)[0]
            if intersect_color == h_color:
                # Action: Change the output pixel to v_color
                output_grid[r, v_col] = v_color
                # Continue to next row as rules are mutually exclusive based on len(unique_row_colors)
                continue 

        # 4. Check and Apply Non-Pure Rule
        # Condition: Row has multiple unique non-bg colors AND intersect pixel IS v_color
        # AND exactly one OTHER non-bg color (h_dom_color) exists in the row
        elif len(unique_row_colors) > 1:
            if intersect_color == v_color:
                other_colors = unique_row_colors - {v_color}
                if len(other_colors) == 1:
                    h_dom_color = list(other_colors)[0]
                    # Action: Change the output pixel to h_dom_color
                    output_grid[r, v_col] = h_dom_color
                    # Continue to next row
                    continue
                    
        # 5. If neither rule applied, the pixel in output_grid remains unchanged (as it was copied initially)

    # 6. Return the modified grid converted back to list of lists format
    return output_grid.tolist()
```