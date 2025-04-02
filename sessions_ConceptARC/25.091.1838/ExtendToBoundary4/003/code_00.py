import numpy as np
from typing import Tuple, Dict, List, Optional

"""
Identifies a single vertical line and a single horizontal line in the input grid. 
Based on their relative positions, extends one of the lines by adding pixels of that line's color.
Rules:
1. If the horizontal line is entirely to the right of the vertical line's column, the horizontal line extends one pixel to the left.
2. If the vertical line is entirely above the horizontal line's row (and rule 1 doesn't apply), the vertical line extends downwards to fill the gap until the row just above the horizontal line.
3. If the vertical line is entirely below the horizontal line's row (and rule 1 doesn't apply), the vertical line extends upwards by one pixel.
4. Otherwise (lines intersect or touch, and rule 1 doesn't apply), the vertical line extends downwards by one pixel.
Boundary checks are performed to ensure added pixels are within the grid.
"""

# === Helper Functions ===

def find_objects(grid: np.ndarray) -> List[Dict]:
    """
    Finds contiguous objects of the same non-background color in the grid.
    Uses Breadth-First Search (BFS).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    "color": color,
                    "pixels": obj_pixels,
                    "min_r": min_r,
                    "max_r": max_r,
                    "min_c": min_c,
                    "max_c": max_c,
                    "height": max_r - min_r + 1,
                    "width": max_c - min_c + 1
                })
    return objects

def find_lines(grid: np.ndarray) -> Tuple[Optional[Dict], Optional[Dict]]:
    """
    Identifies the single vertical and single horizontal line among found objects.
    A vertical line has width=1, height>=1.
    A horizontal line has height=1, width>=1.
    """
    objects = find_objects(grid)
    vertical_line = None
    horizontal_line = None

    for obj in objects:
        is_vertical = obj['width'] == 1 and obj['height'] >= 1
        is_horizontal = obj['height'] == 1 and obj['width'] >= 1

        if is_vertical:
             if vertical_line is None: # Take the first one found
                 vertical_line = obj
             else:
                 # Assumption: only one vertical line per input based on examples
                 pass
        elif is_horizontal:
             if horizontal_line is None: # Take the first one found
                horizontal_line = obj
             else:
                 # Assumption: only one horizontal line per input based on examples
                 pass

    return vertical_line, horizontal_line

# === Main Transform Function ===

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the line extension transformation based on relative positions.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # Find the vertical and horizontal lines
    vertical_line, horizontal_line = find_lines(input_grid)

    # Check if both lines were found (as expected by the problem description)
    if vertical_line is None or horizontal_line is None:
        # Should not happen based on examples, but return original grid if lines aren't found
        print("Warning: Could not find both a vertical and horizontal line.")
        return output_grid

    # Extract properties for easier access
    v_color = vertical_line['color']
    v_col = vertical_line['min_c'] # Since width is 1, min_c == max_c
    v_min_r = vertical_line['min_r']
    v_max_r = vertical_line['max_r']

    h_color = horizontal_line['color']
    h_row = horizontal_line['min_r'] # Since height is 1, min_r == max_r
    h_min_c = horizontal_line['min_c']
    h_max_c = horizontal_line['max_c']

    # Apply transformation rules based on relative positions

    # Rule 1: Horizontal line is entirely to the right of the vertical line
    if h_min_c > v_col:
        extend_col = h_min_c - 1
        # Check boundary before modifying grid
        if 0 <= extend_col < width and 0 <= h_row < height:
            output_grid[h_row, extend_col] = h_color
            
    # Rule 2: Vertical line is entirely above the horizontal line (and Rule 1 is false)
    elif v_max_r < h_row:
        # Extend downwards until the row just before the horizontal line
        for r in range(v_max_r + 1, h_row):
             # Check boundary for each pixel to add
             if 0 <= r < height and 0 <= v_col < width:
                output_grid[r, v_col] = v_color
                
    # Rule 3: Vertical line is entirely below the horizontal line (and Rule 1 is false)
    elif v_min_r > h_row:
        extend_row = v_min_r - 1
        # Check boundary before modifying grid
        if 0 <= extend_row < height and 0 <= v_col < width:
             output_grid[extend_row, v_col] = v_color
             
    # Rule 4: Otherwise (lines intersect or touch, and Rule 1 is false)
    else:
        extend_row = v_max_r + 1
        # Check boundary before modifying grid
        if 0 <= extend_row < height and 0 <= v_col < width:
             output_grid[extend_row, v_col] = v_color

    return output_grid