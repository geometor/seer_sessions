
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Transformation Rule:
1.  Initialization: Create the output grid as a copy of the input grid.
2.  Identify Background: Determine the background color (assumed Azure, 8) as the most frequent color in the input grid.
3.  Find Marker Object:
    *   Find all distinct, contiguous objects composed of blue (1) pixels using cardinal neighbors.
    *   Identify the 'marker' object as the blue object that extends furthest down (i.e., has the pixel(s) with the maximum row index). If no blue objects exist, return the input grid.
    *   Determine the top-most row index (`marker_top_row`) occupied by the marker object.
4.  Find Single-Pixel Objects: Find all objects in the grid consisting of exactly one pixel, whose color is not the background color.
5.  Identify Active Pixels: Filter the single-pixel objects found in step 4, keeping only those whose color is *not* blue (1). These are the 'active pixels'. Store their location (r, c) and color.
6.  Handle No Active Pixels: If there are no active pixels, return the input grid.
7.  Identify Adjacent Active Pixels: Check each active pixel for adjacency (including diagonals) to *any* pixel belonging to the marker object. Collect the active pixels that are adjacent.
8.  Determine Pattern Columns: Create a sorted list of the unique column indices from the adjacent active pixels found in step 7.
9.  Determine Pattern Color Sequence:
    *   Filter the active pixels (from step 5) to keep only those whose row index is *greater than* `marker_top_row`.
    *   Sort these filtered active pixels first by row index in descending order (bottom-to-top), and then by column index in ascending order (left-to-right).
    *   Create the color sequence by taking the colors of these sorted pixels in order. Keep only the *first* occurrence of each unique color encountered.
10. Determine Pattern Bottom Row: Find the minimum row index among the adjacent active pixels found in step 7.
11. Draw Pattern (if applicable):
    *   If there are adjacent active pixels (step 7) AND the pattern color sequence (step 9) is not empty:
        *   Iterate through each column index in the `Pattern Columns` (step 8).
        *   For each column, iterate through rows from 0 down to the `Pattern Bottom Row` (step 10), inclusive.
        *   Set the pixel color in the `output_grid` at `(row, column)` using the `Pattern Color Sequence`, cycling through the sequence based on the `row` index (`color = sequence[row % len(sequence)]`).
12. Cleanup Active Pixels: Iterate through all active pixels identified in step 5. For each active pixel at `(r, c)`:
    *   Check if the location `(r, c)` falls within the area where the pattern was drawn (i.e., if step 11 was executed, `c` is in `Pattern Columns` and `r` is less than or equal to `Pattern Bottom Row`).
    *   If the location is *not* within the pattern area, set `output_grid[r, c]` to the background color. (If it *is* within the pattern area, it has already been overwritten by the pattern drawing step).
13. Return: Return the modified output grid.
"""

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

def _find_objects(grid, color_to_find=None, ignore_color=None, min_size=None, max_size=None):
    """
    Finds all contiguous objects based on cardinal adjacency.
    Returns a list of dictionaries, each containing 'color', 'pixels' (set of (r,c)), 'size', 'locations' (list of {'r':r, 'c':c}), 'min_r', 'max_r'.
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

            while q:
                curr_r, curr_c = q.pop(0)
                obj_pixels.add((curr_r, curr_c))
                pixel_locations_list.append({'r': curr_r, 'c': curr_c})
                min_r_obj = min(min_r_obj, curr_r)
                max_r_obj = max(max_r_obj, curr_r)

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
                })
    return objects


def _is_adjacent(pixel_coord, object_pixel_set):
    """Checks if a pixel coordinate is adjacent (including diagonals) to any pixel in a given set."""
    pr, pc = pixel_coord
    # Check all 8 neighbors of the pixel_coord
    height, width = 30, 30 # Assume max possible grid size for neighbor generation bound checking - safe but potentially inefficient. It's better if grid dimensions are known/passed.
                            # However, we only need to check if a neighbour *exists in the set*, so grid dimensions aren't strictly necessary here.
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            neighbor_coord = (pr + dr, pc + dc)
            if neighbor_coord in object_pixel_set:
                return True
    return False


def transform(input_grid):
    # 1. Initialization
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2. Identify Background Color (most frequent)
    colors, counts = np.unique(input_grid, return_counts=True)
    background_color = colors[np.argmax(counts)]

    # 3. Find Marker Object (lowest blue object)
    marker_color = 1 # Blue
    blue_objects = _find_objects(input_grid, color_to_find=marker_color)

    if not blue_objects:
        return output_grid # No blue objects found

    marker_object = None
    max_marker_row = -1
    for obj in blue_objects:
        current_max_row = obj['max_r']
        if current_max_row > max_marker_row:
            max_marker_row = current_max_row
            marker_object = obj
        # Tie-breaking: if rows are equal, does it matter? NL program doesn't specify. Assume first found is fine.

    if marker_object is None: # Should not happen if blue_objects wasn't empty
         return output_grid

    marker_top_row = marker_object['min_r']
    marker_pixels = marker_object['pixels']

    # 4. Find Single-Pixel Objects (non-background)
    single_pixel_objects = _find_objects(input_grid, ignore_color=background_color, max_size=1)

    # 5. Identify Active Pixels (single-pixel, non-blue)
    active_pixels = []
    for obj in single_pixel_objects:
        if obj['color'] != marker_color:
            # Store only essential info: location and color
            loc = obj['locations'][0] # It's a single pixel object
            active_pixels.append({'r': loc['r'], 'c': loc['c'], 'color': obj['color']})

    # 6. Handle No Active Pixels
    if not active_pixels:
        return output_grid # Nothing to do, return original grid

    # 7. Identify Adjacent Active Pixels (adjacent to marker)
    adjacent_active_pixels = []
    for p_info in active_pixels:
        if _is_adjacent((p_info['r'], p_info['c']), marker_pixels):
            adjacent_active_pixels.append(p_info)

    # Initialize pattern variables
    pattern_columns = []
    pattern_colors = []
    pattern_bottom_row = -1
    pattern_drawn = False

    # Determine pattern parameters only if there are adjacent active pixels
    if adjacent_active_pixels:
        # 8. Determine Pattern Columns
        pattern_columns = sorted(list(set(p['c'] for p in adjacent_active_pixels)))

        # 9. Determine Pattern Color Sequence
        # Filter active pixels below marker's top row
        relevant_for_color = [p for p in active_pixels if p['r'] > marker_top_row]
        # Sort: bottom-up, then left-right
        relevant_for_color.sort(key=lambda p: (-p['r'], p['c']))
        # Get unique colors in order
        seen_colors = set()
        for p in relevant_for_color:
            if p['color'] not in seen_colors:
                pattern_colors.append(p['color'])
                seen_colors.add(p['color'])

        # 10. Determine Pattern Bottom Row
        pattern_bottom_row = min(p['r'] for p in adjacent_active_pixels)

        # 11. Draw Pattern (if colors and columns exist)
        if pattern_columns and pattern_colors:
            num_pattern_colors = len(pattern_colors)
            for c in pattern_columns:
                for r in range(pattern_bottom_row + 1): # From row 0 down to bottom row inclusive
                    color_index = r % num_pattern_colors
                    output_grid[r, c] = pattern_colors[color_index]
            pattern_drawn = True # Mark that the pattern was drawn for cleanup logic

    # 12. Cleanup Active Pixels
    for p in active_pixels:
        r, c = p['r'], p['c']
        # Check if this pixel location falls within the drawn pattern area
        is_in_pattern_area = pattern_drawn and (c in pattern_columns) and (r <= pattern_bottom_row)

        # If the pixel wasn't overwritten by the pattern, set it to background
        if not is_in_pattern_area:
            output_grid[r, c] = background_color

    # 13. Return
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 2 3 2 3 2 3 2 3
8 8 8 8 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 8 8 1 8 8 8
8 8 8 8 8 8 8 8 8 1 1 1 8 8
8 8 8 8 8 8 8 8 8 8 1 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 8
8 8 8 8 1 8 8 8 8 8 2 8 8 8
8 8 8 1 1 1 2 3 2 3 4 3 2 3
8 8 8 8 1 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 8 8 4 8 8 8
8 8 8 8 8 8 8 8 8 8 2 8 8 8
8 8 8 8 8 8 8 8 8 8 1 8 8 8
8 8 8 8 8 8 8 8 8 1 1 1 8 8
8 8 8 8 8 8 8 8 8 8 1 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 1 8 8 8 8 8 8 8 8 8
8 8 8 1 1 1 8 8 8 8 8 8 8 8
8 8 8 8 1 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 1 8 8 8
8 8 8 8 8 8 8 8 8 1 1 1 8 8
8 8 8 8 8 8 8 8 8 8 1 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 11.904761904761898

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 1 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8
8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 4 2 8 8 8
8 8 2 3 8 8 8 8 1 1 8 8 8
8 8 2 3 8 8 8 1 1 1 1 8 8
8 8 2 3 8 8 8 1 1 1 1 8 8
8 8 2 3 8 8 8 1 1 1 1 8 8
8 8 2 3 8 8 8 8 1 1 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 8 8 8 8 8 8 4 2 8 8 8
8 8 1 1 8 8 8 8 4 2 8 8 8
8 1 1 1 1 8 8 8 4 2 8 8 8
8 1 1 1 1 8 8 8 4 2 8 8 8
8 1 1 1 1 8 8 8 4 2 8 8 8
8 8 1 1 8 8 8 8 4 2 8 8 8
8 8 2 3 8 8 8 8 4 2 8 8 8
8 8 2 3 8 8 8 8 4 2 8 8 8
8 8 2 3 8 8 8 8 4 2 8 8 8
8 8 2 3 8 8 8 8 4 2 8 8 8
8 8 2 3 8 8 8 8 4 2 8 8 8
8 8 2 3 8 8 8 8 4 2 8 8 8
8 8 2 3 8 8 8 8 1 1 8 8 8
8 8 2 3 8 8 8 1 1 1 1 8 8
8 8 2 3 8 8 8 1 1 1 1 8 8
8 8 2 3 8 8 8 1 1 1 1 8 8
8 8 2 3 8 8 8 8 1 1 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 1 8 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8
8 1 1 1 1 8 8 8 8 8 8 8 8
8 8 1 1 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 1 1 8 8 8
8 8 2 3 8 8 8 1 1 1 1 8 8
8 8 2 3 8 8 8 1 1 1 1 8 8
8 8 2 3 8 8 8 1 1 1 1 8 8
8 8 2 3 8 8 8 8 1 1 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
8 8 2 3 8 8 8 8 8 8 8 8 8
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.053511705685594
