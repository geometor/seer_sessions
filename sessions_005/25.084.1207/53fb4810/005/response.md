```python
import numpy as np
from collections import Counter

"""
Transformation Rule:
1.  Initialization: Create the output grid as a copy of the input grid.
2.  Identify Background: Determine the background color as the most frequent color in the input grid.
3.  Find Marker Object:
    *   Find all distinct, contiguous objects composed of blue (1) pixels using cardinal neighbors.
    *   If no blue objects exist, return the input grid.
    *   Identify the 'marker' object(s) as the blue object(s) that extend furthest down (maximum row index).
    *   Determine the maximum row index (`marker_max_row`) among all marker objects.
    *   Collect all pixel coordinates `(r, c)` from all marker objects where `r == marker_max_row`. Call this set `marker_bottom_pixels`.
4.  Find Potential Trigger Pixels: Find all objects consisting of exactly one pixel, whose color is neither the background color nor blue (1). Store their location `(r, c)` and color.
5.  Identify Trigger Pixels: Filter the potential trigger pixels found in step 4. Keep only those `(r, c)` where `r < marker_max_row` and there exists some `(br, bc)` in `marker_bottom_pixels` such that `c == bc`.
6.  Handle No Trigger Pixels: If no trigger pixels are found, return the input grid.
7.  Determine Pattern Columns: Create a sorted list of the unique column indices `c` from the identified trigger pixels.
8.  Determine Pattern Top Row: Find the maximum row index `r` among the identified trigger pixels. This is the row index down to which the pattern will be drawn.
9.  Determine Pattern Color Sequence:
    *   Sort the trigger pixels found in step 5, first by row index in descending order (bottom-to-top), and then by column index in ascending order (left-to-right).
    *   Create the color sequence by taking the colors of these sorted pixels in order. Keep only the *first* occurrence of each unique color encountered.
10. Draw Pattern:
    *   If the pattern color sequence is empty, skip drawing.
    *   Iterate through each column index `c` in the `Pattern Columns`.
    *   Iterate through rows `r` from 0 to the `Pattern Top Row`, inclusive.
    *   Set the pixel color in the `output_grid` at `(r, c)` using the `Pattern Color Sequence`, cycling through the sequence based on the `row` index (`color = sequence[r % len(sequence)]`).
11. Cleanup Single Pixels: Iterate through all potential trigger pixels identified in step 4. For each pixel at `(r, c)`:
    *   Check if the location `(r, c)` falls within the area where the pattern was drawn (i.e., if drawing occurred, `c` is in `Pattern Columns` and `r` is less than or equal to `Pattern Top Row`).
    *   If the location is *not* within the pattern area, set `output_grid[r, c]` to the background color.
12. Return: Return the modified output grid.
"""

import numpy as np
from collections import Counter

def _get_neighbors(r, c, height, width, include_diagonal=False):
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

def _find_objects(grid, color_to_find=None, ignore_color=None, min_size=None, max_size=None):
    """
    Finds all contiguous objects based on cardinal adjacency.
    Returns a list of dictionaries, each containing 'color', 'pixels' (set of (r,c)), 'size', 'locations' (list of {'r':r, 'c':c}), 'min_r', 'max_r', 'min_c', 'max_c'.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Skip if already visited or if it's the ignore_color
            if visited[r, c] or (ignore_color is not None and color == ignore_color):
                continue
            # Skip if looking for a specific color and this isn't it
            if color_to_find is not None and color != color_to_find:
                continue

            # Start Flood Fill (BFS) for a new object
            obj_pixels = set()
            q = [(r, c)]
            visited[r, c] = True
            current_color = grid[r, c] # Color of the object being traced
            pixel_locations_list = []
            min_r_obj, max_r_obj = r, r
            min_c_obj, max_c_obj = c, c


            while q:
                curr_r, curr_c = q.pop(0)
                obj_pixels.add((curr_r, curr_c))
                pixel_locations_list.append({'r': curr_r, 'c': curr_c})
                min_r_obj = min(min_r_obj, curr_r)
                max_r_obj = max(max_r_obj, curr_r)
                min_c_obj = min(min_c_obj, curr_c)
                max_c_obj = max(max_c_obj, curr_c)

                # Explore cardinal neighbors
                for nr, nc in _get_neighbors(curr_r, curr_c, height, width, include_diagonal=False):
                    # Check if neighbor has the same color and hasn't been visited
                    if grid[nr, nc] == current_color and not visited[nr, nc]:
                        visited[nr, nc] = True
                        q.append((nr, nc))

            # Check size constraints after finding the whole object
            obj_size = len(obj_pixels)
            valid_size = True
            if min_size is not None and obj_size < min_size:
                valid_size = False
            if max_size is not None and obj_size > max_size:
                valid_size = False

            if valid_size:
                objects.append({
                    'color': current_color,
                    'pixels': obj_pixels,
                    'size': obj_size,
                    'locations': sorted(pixel_locations_list, key=lambda p: (p['r'], p['c'])), # Sorted list of dicts
                    'min_r': min_r_obj,
                    'max_r': max_r_obj,
                    'min_c': min_c_obj,
                    'max_c': max_c_obj
                })
    return objects


def transform(input_grid):
    # 1. Initialization
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2. Identify Background Color (most frequent)
    colors, counts = np.unique(input_grid, return_counts=True)
    if colors.size > 0:
        background_color = colors[np.argmax(counts)]
    else: # Handle empty grid case
        background_color = 0 # Default to black/white? Task spec says 0 is white.

    # 3. Find Marker Object(s) and Bottom Pixels
    marker_color = 1 # Blue
    blue_objects = _find_objects(input_grid, color_to_find=marker_color)

    if not blue_objects:
        return output_grid # No blue objects found

    marker_max_row = -1
    for obj in blue_objects:
        marker_max_row = max(marker_max_row, obj['max_r'])

    marker_bottom_pixels = set()
    marker_bottom_cols = set() # Keep track of columns containing bottom pixels
    for obj in blue_objects:
        if obj['max_r'] == marker_max_row:
            for r_coord, c_coord in obj['pixels']:
                if r_coord == marker_max_row:
                    marker_bottom_pixels.add((r_coord, c_coord))
                    marker_bottom_cols.add(c_coord)

    # 4. Find Potential Trigger Pixels (single, non-bg, non-blue)
    potential_trigger_pixels_info = []
    single_pixel_objects = _find_objects(input_grid, ignore_color=background_color, max_size=1)
    for obj in single_pixel_objects:
        if obj['color'] != marker_color:
            loc = obj['locations'][0] # It's a single pixel object
            potential_trigger_pixels_info.append({'r': loc['r'], 'c': loc['c'], 'color': obj['color']})

    # 5. Identify Trigger Pixels
    trigger_pixels = []
    for p_info in potential_trigger_pixels_info:
        r, c = p_info['r'], p_info['c']
        # Check if pixel is above the marker's bottom row and shares a column with a marker bottom pixel
        if r < marker_max_row and c in marker_bottom_cols:
            trigger_pixels.append(p_info)

    # 6. Handle No Trigger Pixels
    if not trigger_pixels:
        # If no triggers, clean up ALL potential triggers identified in step 4
        for p in potential_trigger_pixels_info:
           output_grid[p['r'], p['c']] = background_color
        return output_grid

    # 7. Determine Pattern Columns
    pattern_columns = sorted(list(set(p['c'] for p in trigger_pixels)))

    # 8. Determine Pattern Top Row (inclusive boundary for drawing)
    pattern_top_row = -1
    if trigger_pixels:
        pattern_top_row = max(p['r'] for p in trigger_pixels)

    # 9. Determine Pattern Color Sequence
    # Sort triggers: bottom-up (desc row), then left-right (asc col)
    trigger_pixels.sort(key=lambda p: (-p['r'], p['c']))
    pattern_colors = []
    seen_colors = set()
    for p in trigger_pixels:
        if p['color'] not in seen_colors:
            pattern_colors.append(p['color'])
            seen_colors.add(p['color'])

    # 10. Draw Pattern
    pattern_drawn = False
    if pattern_columns and pattern_colors and pattern_top_row >= 0:
        num_pattern_colors = len(pattern_colors)
        for c in pattern_columns:
            for r in range(pattern_top_row + 1): # From row 0 down to pattern_top_row inclusive
                color_index = r % num_pattern_colors
                output_grid[r, c] = pattern_colors[color_index]
        pattern_drawn = True # Mark that the pattern was drawn for cleanup logic

    # 11. Cleanup Single Pixels (potential triggers)
    for p in potential_trigger_pixels_info:
        r, c = p['r'], p['c']
        # Check if this pixel location falls within the drawn pattern area
        is_in_pattern_area = pattern_drawn and (c in pattern_columns) and (r <= pattern_top_row)

        # If the pixel wasn't overwritten by the pattern, set it to background
        if not is_in_pattern_area:
            output_grid[r, c] = background_color

    # 12. Return
    return output_grid
```