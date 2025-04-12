```python
import numpy as np
from collections import defaultdict

"""
Identifies the color group(s) containing the overall leftmost pixel(s) and the color group(s) containing the overall rightmost pixel(s) in the input grid.
Translates the identified leftmost color group(s) horizontally so their leftmost edge aligns with the grid's left edge (column 0).
Translates the identified rightmost color group(s) horizontally so their rightmost edge aligns with the grid's right edge (last column).
All other pixels become background (white, 0). The vertical position and internal structure of the moved groups are preserved.
"""

def _get_color_coordinates(grid: np.ndarray) -> tuple[dict[int, list[tuple[int, int]]], int, int]:
    """Finds coordinates for each non-background color and overall min/max columns."""
    color_coords = defaultdict(list)
    min_overall_col = grid.shape[1]
    max_overall_col = -1
    has_non_background = False

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != 0:
                has_non_background = True
                color_coords[color].append((r, c))
                min_overall_col = min(min_overall_col, c)
                max_overall_col = max(max_overall_col, c)

    if not has_non_background:
        min_overall_col = -1 # Indicate no non-background pixels found
        max_overall_col = -1

    return color_coords, min_overall_col, max_overall_col

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Horizontally translates the leftmost color group to the left edge 
    and the rightmost color group to the right edge of the grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output grid with background color
    output_np = np.zeros_like(input_np)

    # Find coordinates for each color and the overall min/max columns
    color_coords, min_overall_col, max_overall_col = _get_color_coordinates(input_np)

    # If no non-background pixels, return the empty grid
    if min_overall_col == -1:
        return output_np.tolist()

    # Identify the colors present at the minimum overall column
    leftmost_colors = set()
    for color, coords in color_coords.items():
        for r, c in coords:
            if c == min_overall_col:
                leftmost_colors.add(color)
                break # No need to check other coords for this color

    # Identify the colors present at the maximum overall column
    rightmost_colors = set()
    for color, coords in color_coords.items():
        for r, c in coords:
            if c == max_overall_col:
                rightmost_colors.add(color)
                break # No need to check other coords for this color

    # Process and translate leftmost colors
    for color in leftmost_colors:
        coords = color_coords[color]
        if not coords: continue # Should not happen if color is in leftmost_colors, but safe check

        # Find the minimum column for this specific color
        min_col_for_this_color = min(c for r, c in coords)

        # Calculate the shift needed to move to the left edge
        shift = 0 - min_col_for_this_color

        # Apply the shift to each pixel of this color in the output grid
        for r, c in coords:
            new_c = c + shift
            if 0 <= new_c < width: # Ensure the new column is within bounds
                 output_np[r, new_c] = color

    # Process and translate rightmost colors
    # Note: If a color is in both sets, this might overwrite its placement from the previous step
    # The examples suggest this is the desired behavior (the final position is determined by the rightmost alignment)
    # However, checking the first example, red moves left, blue moves right. They are distinct sets.
    # Rechecking the logic: a color can only be in leftmost_colors OR rightmost_colors if min_overall_col != max_overall_col.
    # If min_overall_col == max_overall_col (e.g., a single vertical line), a color could be in both.
    # The instructions imply separate treatment. Let's stick to processing both sets.
    for color in rightmost_colors:
        coords = color_coords[color]
        if not coords: continue

        # Find the maximum column for this specific color
        max_col_for_this_color = max(c for r, c in coords)

        # Calculate the shift needed to move to the right edge
        shift = (width - 1) - max_col_for_this_color

        # Apply the shift to each pixel of this color in the output grid
        for r, c in coords:
            new_c = c + shift
            # It's crucial to potentially overwrite here if a color was also leftmost
            if 0 <= new_c < width: # Ensure the new column is within bounds
                output_np[r, new_c] = color


    return output_np.tolist()
```