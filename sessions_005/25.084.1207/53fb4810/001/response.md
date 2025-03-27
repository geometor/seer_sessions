```python
import numpy as np
from collections import defaultdict

"""
Transformation Rule:
1. Identify the background color (azure, 8).
2. Find all blue (1) objects and identify the 'marker' object as the one positioned lowest in the grid.
3. Find all 'isolated' single pixels (non-background pixels surrounded by background).
4. Identify 'active' isolated pixels (those whose color is not blue).
5. If no active pixels exist, return the input grid.
6. Identify 'adjacent active' pixels (active pixels adjacent, including diagonals, to the marker object).
7. Determine the columns for the new pattern based on the columns of the adjacent active pixels.
8. Determine the color sequence for the pattern by collecting the unique colors of *all* active pixels, ordered by their first appearance scanning bottom-to-top, then left-to-right.
9. Determine the bottom row for the pattern as the minimum row index (highest position on grid) among adjacent active pixels.
10. Create the output grid by copying the input.
11. Draw a vertical repeating pattern in the determined columns from row 0 down to the determined bottom row, using the determined color sequence.
12. Set the original locations of all active isolated pixels to the background color in the output grid.
13. Return the modified grid.
"""

def _find_background_color(grid):
    """Finds the most frequent color, assumed to be the background."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def _get_neighbors(r, c, height, width, include_diagonal=True):
    """Gets valid neighbor coordinates for a given cell."""
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if not include_diagonal and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def _find_objects(grid, color):
    """Finds all contiguous objects of a given color."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = set()
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    curr_r, curr_c = q.pop(0)
                    obj_pixels.add((curr_r, curr_c))
                    # Use cardinal neighbors for object definition
                    for nr, nc in _get_neighbors(curr_r, curr_c, height, width, include_diagonal=False):
                        if grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def _find_isolated_pixels(grid, background_color):
    """Finds all pixels surrounded entirely by the background color."""
    height, width = grid.shape
    isolated = []
    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color:
                is_isolated = True
                for nr, nc in _get_neighbors(r, c, height, width, include_diagonal=True):
                    if grid[nr, nc] != background_color:
                        is_isolated = False
                        break
                if is_isolated:
                    isolated.append({'r': r, 'c': c, 'color': grid[r, c]})
    return isolated

def _is_adjacent(pixel_coord, object_coords):
    """Checks if a pixel is adjacent (including diagonals) to any pixel in an object."""
    pr, pc = pixel_coord
    height, width = 30, 30 # Use max possible size for bounds check, actual grid size better
    # Ideally, pass grid dimensions or calculate from object_coords max/min
    for r_obj, c_obj in object_coords:
         # Check if pr, pc is one of the 8 neighbours of r_obj, c_obj
         if max(abs(pr - r_obj), abs(pc - c_obj)) == 1:
              return True
    return False


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify background color
    background_color = _find_background_color(input_grid)

    # 2. Find marker object (lowest blue object)
    marker_color = 1 # Blue
    blue_objects = _find_objects(input_grid, marker_color)
    if not blue_objects:
        return output_grid # No blue objects, maybe return input? Task implies marker exists.

    marker_object = None
    max_row = -1
    for obj in blue_objects:
        current_max_row = max(r for r, c in obj)
        if current_max_row > max_row:
            max_row = current_max_row
            marker_object = obj

    if marker_object is None:
         # Should not happen based on examples, but handle defensively
         return output_grid

    # 3. Find isolated pixels
    isolated_pixels = _find_isolated_pixels(input_grid, background_color)

    # 4. Identify 'active' isolated pixels (non-blue)
    active_pixels = [p for p in isolated_pixels if p['color'] != marker_color]

    # 5. If no active pixels, return input
    if not active_pixels:
        return output_grid

    # 6. Identify 'adjacent active' pixels
    adjacent_active_pixels = []
    for pixel_info in active_pixels:
        if _is_adjacent((pixel_info['r'], pixel_info['c']), marker_object):
            adjacent_active_pixels.append(pixel_info)

    # If no active pixels are adjacent to the marker, no pattern is generated
    # but the active pixels are still removed later.
    if not adjacent_active_pixels:
        # 12. Clean up active pixels even if no pattern is drawn
        for p in active_pixels:
            output_grid[p['r'], p['c']] = background_color
        return output_grid

    # 7. Determine pattern columns
    pattern_columns = sorted(list(set(p['c'] for p in adjacent_active_pixels)))

    # 8. Determine pattern colors (order based on *all* active pixels)
    # Sort active pixels: bottom-to-top (descending row), then left-to-right (ascending col)
    sorted_active_pixels = sorted(active_pixels, key=lambda p: (-p['r'], p['c']))
    pattern_colors = []
    seen_colors = set()
    for p in sorted_active_pixels:
        if p['color'] not in seen_colors:
            pattern_colors.append(p['color'])
            seen_colors.add(p['color'])

    if not pattern_colors: # Should not happen if active_pixels is not empty
        return output_grid # Or handle error

    # 9. Determine pattern bottom row (min row index of adjacent active pixels)
    pattern_bottom_row = min(p['r'] for p in adjacent_active_pixels)

    # 11. Draw the pattern
    num_pattern_colors = len(pattern_colors)
    for c in pattern_columns:
        for r in range(pattern_bottom_row + 1): # Iterate from row 0 down to pattern_bottom_row inclusive
            color_index = r % num_pattern_colors
            output_grid[r, c] = pattern_colors[color_index]

    # 12. Clean up: Set original active pixel locations to background
    for p in active_pixels:
        # Make sure not to erase parts of the newly drawn pattern if an active pixel was there
        # Check if the pixel location is part of the pattern area
        is_in_pattern_area = (p['c'] in pattern_columns and p['r'] <= pattern_bottom_row)
        if not is_in_pattern_area:
             output_grid[p['r'], p['c']] = background_color
        # If it IS in the pattern area, it was already overwritten by step 11.

    return output_grid
```