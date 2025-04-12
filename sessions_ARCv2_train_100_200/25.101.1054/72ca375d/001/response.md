```python
import numpy as np
from typing import List, Tuple, Set

"""
Transformation Rule:
1. Identify all unique non-white pixel color values in the input grid.
2. Determine the median (middle value) of these unique color values when sorted numerically.
3. Find the object composed of pixels matching this median color.
4. Calculate the bounding box of this object (the smallest rectangle enclosing all its pixels).
5. Extract the subgrid defined by this bounding box from the input grid to form the output grid.
"""

def find_bounding_box(grid: np.ndarray, color: int) -> Tuple[int, int, int, int]:
    """
    Finds the bounding box (min_row, max_row, min_col, max_col) for a given color in the grid.
    Returns (-1, -1, -1, -1) if the color is not found.
    """
    rows, cols = np.where(grid == color)
    if rows.size == 0:
        return -1, -1, -1, -1  # Color not found
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selects an object based on its color being the median of all non-white colors present,
    and extracts its bounding box from the input grid.
    """
    # Convert input list of lists to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)

    # 1. Identify all unique non-white pixel color values
    unique_colors: Set[int] = set(grid_np.flatten())
    non_white_colors: List[int] = sorted([c for c in unique_colors if c != 0])

    # 2. Determine the median color
    # Assuming there are always 3 non-white colors as per examples
    if len(non_white_colors) != 3:
        # Handle cases with not exactly 3 colors if necessary,
        # but based on examples, we expect 3.
        # For now, let's stick to the observed pattern.
        # If this assumption is wrong, the logic might need adjustment.
        # If only 1 color, it's the median. If 2, maybe pick one? Or error?
        # Let's assume 3 based on the provided train examples.
        if len(non_white_colors) == 1:
             median_color = non_white_colors[0]
        elif len(non_white_colors) == 2:
             # Undefined median based on problem description, could pick min or max?
             # Let's default to min for now if this unexpected case happens.
             median_color = non_white_colors[0] # Or potentially raise an error
        elif len(non_white_colors) == 0:
             return [] # Return empty grid if no non-white colors
        else: # More than 3, find the actual median
             median_index = (len(non_white_colors) - 1) // 2
             median_color = non_white_colors[median_index]

    else: # Exactly 3 colors
        median_color = non_white_colors[1] # The middle element

    # 3 & 4. Find the object and its bounding box
    min_row, max_row, min_col, max_col = find_bounding_box(grid_np, median_color)

    # Check if the color was found
    if min_row == -1:
        # This shouldn't happen if the median color was correctly identified
        # from the grid's unique colors, but handle defensively.
        return [] # Return empty grid or handle error appropriately

    # 5. Extract the bounding box subgrid
    output_grid_np = grid_np[min_row : max_row + 1, min_col : max_col + 1]

    # Convert numpy array back to list of lists for the required output format
    output_grid = output_grid_np.tolist()

    return output_grid
```