import numpy as np
from typing import List, Tuple, Set

"""
Identifies an object composed of an outer frame (Color A) and inner core (Color B) in the input grid.
Creates an output grid by expanding this object based on Manhattan distance from the inner core and preserving parts of the original outer frame.

Transformation Steps:
1. Identify the coordinates of pixels for the inner color (B) (`inner_coords`) and the outer color (A) (`outer_coords`) in the input grid.
2. Create a new output grid of the same dimensions as the input, initialized with the background color (white, 0).
3. For each cell (r, c) in the grid:
    a. Calculate the minimum Manhattan distance (`min_dist_inner`) from (r, c) to any coordinate in `inner_coords`.
    b. Check if the coordinate (r, c) exists in the set `outer_coords` (`is_original_outer`).
    c. Apply coloring rules based on precedence:
        i. If `min_dist_inner == 1`: Set the output cell `(r, c)` to color B.
        ii. Else if `min_dist_inner == 2`: Set the output cell `(r, c)` to color A.
        iii. Else if `is_original_outer` is true: Set the output cell `(r, c)` to color A.
        iv. Otherwise: Leave the output cell `(r, c)` as white (0).
4. Return the completed output grid.
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
    Determines the inner and outer colors based on the corner pixel of the bounding box.
    Assumes the color at the top-left corner of the bounding box is the outer color.
    """
    if not colors:
        return None, None

    min_r, min_c, _, _ = bbox
    outer_c = grid[min_r, min_c]

    if len(colors) == 1:
        inner_c = outer_c # If only one color, it acts as both
    elif len(colors) == 2:
        inner_c = colors[0] if colors[1] == outer_c else colors[1]
    else:
        # Handle unexpected number of colors if necessary, here assuming outer is determined
        inner_c = None # Or raise error? Based on problem constraints, should be 1 or 2.

    return int(inner_c) if inner_c is not None else None, int(outer_c)

def get_color_coords(grid: np.ndarray, color: int) -> Set[Tuple[int, int]]:
    """Returns a set of (row, col) tuples for all pixels of a specific color."""
    coords = np.argwhere(grid == color)
    return set(tuple(coord) for coord in coords)

def min_manhattan_distance(point: Tuple[int, int], coord_set: Set[Tuple[int, int]]) -> float:
    """Calculates the minimum Manhattan distance from a point to any coordinate in a set."""
    if not coord_set:
        return float('inf') # Return infinity if the set is empty
    r1, c1 = point
    min_dist = float('inf')
    for r2, c2 in coord_set:
        dist = abs(r1 - r2) + abs(c1 - c2)
        min_dist = min(min_dist, dist)
    return min_dist

# Main transformation function
def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the two-layer expansion transformation based on distance
    to the original object's inner core and outer frame.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify object properties
    non_white_colors = find_colors(input_np)
    bbox = find_bounding_box(input_np)

    # Handle cases with no object or unexpected color counts
    if bbox is None or not (1 <= len(non_white_colors) <= 2):
        print("Warning: No object found or unexpected number of colors. Returning original grid.")
        return input_grid # Return original grid if no object or wrong color count

    inner_color, outer_color = determine_inner_outer(input_np, non_white_colors, bbox)

    # Check if colors were determined successfully
    if inner_color is None or outer_color is None:
        print("Warning: Could not determine inner/outer colors. Returning original grid.")
        return input_grid # Should not happen if bbox and colors are valid, but safety check

    # Get coordinates for inner and outer colors
    inner_coords = get_color_coords(input_np, inner_color)
    outer_coords = get_color_coords(input_np, outer_color)

    # 2. Initialize output grid with background color (0)
    output_np = np.zeros_like(input_np)

    # 3. Iterate through each cell (r, c) and apply coloring rules
    for r in range(rows):
        for c in range(cols):
            # a. Calculate min distance to inner core pixels
            min_dist_inner = min_manhattan_distance((r, c), inner_coords)

            # b. Check if the current cell was originally part of the outer frame
            is_original_outer = (r, c) in outer_coords

            # c. Apply coloring rules with precedence
            if min_dist_inner == 1:
                # i. Rule 1: Distance 1 from inner -> Inner Color
                output_np[r, c] = inner_color
            elif min_dist_inner == 2:
                # ii. Rule 2: Distance 2 from inner -> Outer Color
                output_np[r, c] = outer_color
            elif is_original_outer:
                # iii. Rule 3: Was originally outer (and not covered by rule 1/2) -> Outer Color
                output_np[r, c] = outer_color
            # iv. Otherwise: Leave as background (already initialized to 0)

    # 4. Return the completed output grid as a list of lists
    return output_np.tolist()