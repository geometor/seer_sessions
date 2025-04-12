import numpy as np
from typing import List, Dict, Tuple

"""
Transforms an input grid based on identifying and processing specific 'V' and 'L' shaped patterns.

V-shape Processing:
- Identifies V-shapes (top pixel + two diagonal bottom pixels of the same non-orange color).
- Calculates a vertical projection distance 'k' based on the V-shape's row and its horizontal distance from the grid's center.
- Projects the V-shape upwards by 'k' rows.
- The projection color depends on the original V-shape color:
    - White V-shapes project as maroon.
    - Maroon V-shapes closest to the vertical center project as blue.
    - Other (non-central) maroon V-shapes project as maroon.

L-shape Processing (triggered only if red L-shapes exist):
- Identifies L-shapes (3 red pixels: top-left corner, pixel right, pixel below).
- Applies a fixed global pattern of maroon pixels in rows 1 and 9 at columns 0, 3, 6, 9.
- Finds the minimum row containing any red L-shape.
- Identifies the red L-shape in that minimum row which is closest to the vertical center (tie-breaking with the leftmost column).
- Changes the three pixels composing this specific central L-shape to maroon.
"""

# Define Colors and Constants
ORANGE = 7
MAROON = 9
WHITE = 0
RED = 2
BLUE = 1
PROJECTION_THRESHOLD_ROW = 13
PROJECTION_K_NEAR = 6
PROJECTION_K_FAR = 5
PROJECTION_DIST_THRESHOLD = 5.0 # Max distance from center for row-based k logic
L_SHAPE_GLOBAL_ROWS = [1, 9]
L_SHAPE_GLOBAL_COLS = [0, 3, 6, 9]


def find_v_shapes(grid: np.ndarray, center_col: float) -> List[Dict]:
    """Finds all V-shapes, returning their center, color, and distance from center."""
    v_shapes = []
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(1, width - 1):
            color = grid[r, c]
            if color != ORANGE and \
               grid[r+1, c-1] == color and \
               grid[r+1, c+1] == color:
                dist = abs(c - center_col)
                v_shapes.append({'center': (r, c), 'color': color, 'dist': dist})
    return v_shapes

def find_red_l_shapes(grid: np.ndarray, center_col: float) -> List[Dict]:
    """Finds all red L-shapes, returning corner, pixels, and distance from center."""
    l_shapes = []
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            if grid[r, c] == RED and \
               grid[r, c+1] == RED and \
               grid[r+1, c] == RED:
                dist = abs(c - center_col)
                pixels = [(r, c), (r, c+1), (r+1, c)]
                l_shapes.append({'corner': (r, c), 'pixels': pixels, 'dist': dist})
    return l_shapes


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape
    center_col = (width - 1) / 2.0

    # --- Find Shapes ---
    v_shapes = find_v_shapes(grid, center_col)
    red_l_shapes = find_red_l_shapes(grid, center_col)

    # --- Process V-shapes ---
    if v_shapes:
        # Find minimum distance for maroon V-shapes to identify central ones
        maroon_v_shapes = [v for v in v_shapes if v['color'] == MAROON]
        min_dist_maroon = min((v['dist'] for v in maroon_v_shapes), default=float('inf'))

        for v in v_shapes:
            r, c = v['center']
            color = v['color']
            dist = v['dist']

            # Calculate projection offset 'k'
            k_row = PROJECTION_K_NEAR if r < PROJECTION_THRESHOLD_ROW else PROJECTION_K_FAR
            k = PROJECTION_K_FAR if dist > PROJECTION_DIST_THRESHOLD else k_row
            target_r = r - k
            target_c = c

            # Determine output color
            output_color = -1 # Default invalid
            if color == WHITE:
                output_color = MAROON
            elif color == MAROON:
                if dist == min_dist_maroon: # Central maroon V-shape(s)
                    output_color = BLUE
                else: # Non-central maroon V-shape
                    output_color = MAROON

            # Apply the modification if valid color and within bounds
            if output_color != -1 and 0 <= target_r < height:
                output_grid[target_r, target_c] = output_color

    # --- Process Red L-shapes ---
    if red_l_shapes:
        # Apply global pattern
        for r_glob in L_SHAPE_GLOBAL_ROWS:
            for c_glob in L_SHAPE_GLOBAL_COLS:
                if 0 <= r_glob < height and 0 <= c_glob < width:
                     output_grid[r_glob, c_glob] = MAROON

        # Find minimum row containing red L-shapes
        min_r = min(l['corner'][0] for l in red_l_shapes)

        # Filter L-shapes to keep only those at the minimum row
        top_row_l_shapes = [l for l in red_l_shapes if l['corner'][0] == min_r]

        # Find the central L-shape among those in the minimum row
        # Sort by distance, then by column for tie-breaking
        top_row_l_shapes.sort(key=lambda l: (l['dist'], l['corner'][1]))
        central_l_shape = top_row_l_shapes[0] # The first one after sorting is the target

        # Modify the pixels of the central L-shape
        for pr, pc in central_l_shape['pixels']:
            if 0 <= pr < height and 0 <= pc < width:
                output_grid[pr, pc] = MAROON

    return output_grid.tolist()