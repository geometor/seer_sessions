import numpy as np
from typing import List, Tuple, Set

"""
Transforms an input grid containing a single rectangular object with an outer frame (color A) and an inner core (color B). 
The transformation involves swapping the colors within the original object's bounds and adding two expansion layers around it.

Transformation Steps:
1. Identify the unique non-white colors in the input grid. Assume there are exactly two: an outer frame color (A) and an inner core color (B). Determine which is which by checking the color of a corner pixel of the object's bounding box (assumed to be A).
2. Find the coordinates of all non-white pixels in the input grid (`all_coords`).
3. Initialize an output grid of the same dimensions as the input, filled with the background color (0, white).
4. For each cell (r, c) in the output grid:
    a. Calculate the minimum Manhattan distance (`min_dist`) from (r, c) to any coordinate in `all_coords`.
    b. Apply coloring rules based on `min_dist`:
        i. If `min_dist == 0` (the cell is within the original object's location): 
           - Check the color in the *input* grid at `(r, c)`.
           - If the input color was B (inner), set the output cell `(r, c)` to color A (outer).
           - If the input color was A (outer), set the output cell `(r, c)` to color B (inner).
        ii. Else if `min_dist == 1`: Set the output cell `(r, c)` to color A (original outer color).
        iii. Else if `min_dist == 2`: Set the output cell `(r, c)` to color A (original outer color).
        iv. Else (`min_dist > 2`): Leave the output cell `(r, c)` as white (0).
5. Return the completed output grid.
"""

# Helper functions
def find_colors(grid: np.ndarray) -> List[int]:
    """Finds the unique non-zero colors in the grid."""
    return sorted(list(np.unique(grid[grid != 0])))

def find_bounding_box(grid: np.ndarray) -> Tuple[int, int, int, int] | None:
    """Finds the bounding box (min_r, min_c, max_r, max_c) of non-zero pixels."""
    non_white_coords = np.argwhere(grid != 0)
    if non_white_coords.size == 0:
        return None
    min_r, min_c = non_white_coords.min(axis=0)
    max_r, max_c = non_white_coords.max(axis=0)
    return (int(min_r), int(min_c), int(max_r), int(max_c))

def determine_inner_outer(grid: np.ndarray, colors: List[int], bbox: Tuple[int, int, int, int]) -> Tuple[int | None, int | None]:
    """
    Determines the inner (B) and outer (A) colors.
    Assumes the color at the top-left corner of the bounding box is the outer color (A).
    Handles cases where only one non-white color might be present (although examples imply two).
    """
    if not colors:
        return None, None # No colors found

    min_r, min_c, _, _ = bbox
    outer_color_A = grid[min_r, min_c] # Assume corner is Outer Color A

    if len(colors) == 1:
        # If only one color, it acts as both A and B
        inner_color_B = outer_color_A
    elif len(colors) == 2:
        # The other color is the Inner Color B
        inner_color_B = colors[0] if colors[1] == outer_color_A else colors[1]
    else:
        # Should not happen based on examples, but handle defensively
        print(f"Warning: Expected 1 or 2 non-white colors, found {len(colors)}. Assuming corner color is outer.")
        inner_color_B = None # Cannot reliably determine inner color

    # Ensure integer types before returning
    outer_A = int(outer_color_A)
    inner_B = int(inner_color_B) if inner_color_B is not None else None

    return inner_B, outer_A

def get_all_non_white_coords(grid: np.ndarray) -> Set[Tuple[int, int]]:
    """Returns a set of (row, col) tuples for all non-zero pixels."""
    coords = np.argwhere(grid != 0)
    return set(tuple(coord) for coord in coords)

def min_manhattan_distance(point: Tuple[int, int], coord_set: Set[Tuple[int, int]]) -> int:
    """Calculates the minimum Manhattan distance from a point to any coordinate in a set."""
    if not coord_set:
        return float('inf') # Return infinity if the set is empty
    r1, c1 = point
    min_dist = float('inf')
    for r2, c2 in coord_set:
        dist = abs(r1 - r2) + abs(c1 - c2)
        min_dist = min(min_dist, dist)
    # Ensure the return value is an integer for comparison
    return int(min_dist)

# Main transformation function
def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the color-swapping and two-layer expansion transformation.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Step 1: Identify object properties
    non_white_colors = find_colors(input_np)
    bbox = find_bounding_box(input_np)

    # Handle cases with no object or unexpected color counts
    if bbox is None:
        # No object found, return original grid
        return input_grid
    if not (1 <= len(non_white_colors) <= 2):
         # Based on examples, expect 2 colors. Handle 1 color case, return original if > 2.
         if len(non_white_colors) > 2:
             print("Warning: More than 2 non-white colors found. Returning original grid.")
             return input_grid
         # If 1 color, proceed, it will act as both A and B.

    inner_color_B, outer_color_A = determine_inner_outer(input_np, non_white_colors, bbox)

    # Check if colors were determined successfully (important if more than 2 colors found)
    if inner_color_B is None or outer_color_A is None:
        print("Warning: Could not reliably determine inner/outer colors. Returning original grid.")
        return input_grid

    # Step 2: Get coordinates of all original non-white pixels
    all_coords = get_all_non_white_coords(input_np)
    if not all_coords: # Should be caught by bbox check, but defensive
         return input_grid

    # Step 3: Initialize output grid with background color (0)
    output_np = np.zeros_like(input_np)

    # Step 4 & 5: Iterate through each output cell, calculate distance, apply rules
    for r in range(rows):
        for c in range(cols):
            # a. Calculate min distance to the original object
            min_dist = min_manhattan_distance((r, c), all_coords)

            # b. Apply coloring rules
            if min_dist == 0:
                # i. Swap colors for original object location
                original_color = input_np[r, c]
                if original_color == inner_color_B:
                    output_np[r, c] = outer_color_A
                elif original_color == outer_color_A:
                    output_np[r, c] = inner_color_B
                # Note: If only one color, A==B, so A->B and B->A results in the same color.
            elif min_dist == 1:
                # ii. Layer 1 gets original outer color A
                output_np[r, c] = outer_color_A
            elif min_dist == 2:
                # iii. Layer 2 gets original outer color A
                output_np[r, c] = outer_color_A
            # iv. Else (min_dist > 2): Leave as background (already 0)

    # Convert the result back to a list of lists
    return output_np.tolist()