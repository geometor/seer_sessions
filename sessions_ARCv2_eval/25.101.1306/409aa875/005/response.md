```python
import numpy as np
from typing import List, Dict, Tuple

"""
Transforms an input grid based on identifying and processing specific 'V' and 'L' shaped patterns.

V-shape Processing:
1. Identifies V-shapes: three pixels of the same non-orange color C arranged as (r, c), (r+1, c-1), (r+1, c+1).
2. Calculates the horizontal distance of the center pixel (r, c) from the grid's vertical center line.
3. Determines if a maroon V-shape is 'central' (has the minimum distance among all maroon V-shapes).
4. Projects the V-shape vertically upwards by a fixed distance (k=5).
5. The color of the projected pixel depends on the original V-shape:
   - White V-shapes project as maroon.
   - Central maroon V-shapes project as blue.
   - Non-central maroon V-shapes project as maroon.

L-shape Processing (triggered only if red L-shapes exist):
1. Identifies L-shapes: three red pixels arranged as (r, c), (r, c+1), (r+1, c).
2. Applies a fixed global pattern: sets pixels at specific coordinates in rows 1 and 9 to maroon.
3. Finds the minimum row ('min_r') containing any red L-shape corner (r, c).
4. Identifies the red L-shape in 'min_r' that is closest to the grid's vertical center line (tie-breaking using the leftmost column).
5. Changes the three pixels composing this specific central L-shape to maroon.
"""

# --- Constants ---
ORANGE = 7
MAROON = 9
WHITE = 0
RED = 2
BLUE = 1
V_SHAPE_PROJECTION_K = 5  # Constant vertical offset for V-shapes
L_SHAPE_GLOBAL_ROWS = [1, 9]
L_SHAPE_GLOBAL_COLS = [0, 3, 6, 9]


def find_v_shapes(grid: np.ndarray, center_col: float) -> List[Dict]:
    """
    Finds all V-shapes in the grid.

    A V-shape consists of 3 pixels of the same non-orange color C
    at (r, c), (r+1, c-1), (r+1, c+1).

    Returns a list of dictionaries, each containing:
        'center': (r, c) tuple
        'color': C (integer color value)
        'dist': Absolute horizontal distance of 'c' from 'center_col'
    """
    v_shapes = []
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(1, width - 1):
            color = grid[r, c]
            # Check if the pixel is not the background color and forms a V-shape
            if color != ORANGE and \
               grid[r+1, c-1] == color and \
               grid[r+1, c+1] == color:
                dist = abs(c - center_col)
                v_shapes.append({'center': (r, c), 'color': color, 'dist': dist})
    return v_shapes


def find_red_l_shapes(grid: np.ndarray, center_col: float) -> List[Dict]:
    """
    Finds all red L-shapes in the grid.

    An L-shape consists of 3 red pixels at (r, c), (r, c+1), (r+1, c).

    Returns a list of dictionaries, each containing:
        'corner': (r, c) tuple (top-left pixel)
        'pixels': List of coordinates [(r, c), (r, c+1), (r+1, c)]
        'dist': Absolute horizontal distance of 'c' from 'center_col'
    """
    l_shapes = []
    height, width = grid.shape
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if the pixels form a red L-shape
            if grid[r, c] == RED and \
               grid[r, c+1] == RED and \
               grid[r+1, c] == RED:
                dist = abs(c - center_col)
                pixels = [(r, c), (r, c+1), (r+1, c)]
                l_shapes.append({'corner': (r, c), 'pixels': pixels, 'dist': dist})
    return l_shapes


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid based on V and L shapes.
    """
    # Initialize grid and constants
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

        # Iterate through all found V-shapes
        for v in v_shapes:
            r, c = v['center']
            color = v['color']
            dist = v['dist']

            # Calculate target coordinates using the constant projection distance
            target_r = r - V_SHAPE_PROJECTION_K
            target_c = c

            # Determine output color based on input color and centrality
            output_color = -1 # Default invalid color
            if color == WHITE:
                output_color = MAROON
            elif color == MAROON:
                if dist == min_dist_maroon: # Central maroon V-shape(s)
                    output_color = BLUE
                else: # Non-central maroon V-shape
                    output_color = MAROON

            # Apply the modification if the color is valid and target is within grid bounds
            if output_color != -1 and 0 <= target_r < height:
                output_grid[target_r, target_c] = output_color

    # --- Process Red L-shapes ---
    if red_l_shapes:
        # 1. Apply global pattern
        for r_glob in L_SHAPE_GLOBAL_ROWS:
            for c_glob in L_SHAPE_GLOBAL_COLS:
                if 0 <= r_glob < height and 0 <= c_glob < width:
                     output_grid[r_glob, c_glob] = MAROON

        # 2. Find minimum row containing red L-shapes
        min_r = min(l['corner'][0] for l in red_l_shapes)

        # 3. Filter L-shapes to keep only those at the minimum row
        top_row_l_shapes = [l for l in red_l_shapes if l['corner'][0] == min_r]

        # 4. Find the central L-shape among those in the minimum row
        # Sort by distance, then by column index for tie-breaking
        top_row_l_shapes.sort(key=lambda l: (l['dist'], l['corner'][1]))
        central_l_shape = top_row_l_shapes[0] # The first one after sorting is the target

        # 5. Modify the pixels of the central L-shape to maroon
        for pr, pc in central_l_shape['pixels']:
            if 0 <= pr < height and 0 <= pc < width:
                output_grid[pr, pc] = MAROON

    # Convert back to list of lists and return
    return output_grid.tolist()
```