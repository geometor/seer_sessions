```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1.  Identify all contiguous objects (groups of connected pixels of the same color) that are not white (0). Use 4-way connectivity.
2.  Determine the single largest object based on the number of pixels it contains. If there's a tie in size, select the one whose top-most, left-most pixel comes first in a row-by-row, column-by-column scan. Let the color of this largest object be the `KeyColor` and its coordinates be `KeyObjectCoords`.
3.  Identify all non-white pixels in the input grid whose coordinates are *not* in `KeyObjectCoords`. These are the `PayloadPixels`. Collect their coordinates (`PayloadCoords`) and colors.
4.  If there are no `PayloadPixels`, return an empty grid represented as `[[]]`.
5.  Determine the set of `ColorsToRemove` based on the `KeyColor`:
    *   If `KeyColor` is Green (3), `ColorsToRemove` = {Green (3), Maroon (9)}.
    *   If `KeyColor` is Blue (1), `ColorsToRemove` = {Blue (1), Red (2), Yellow (4), Maroon (9)}.
    *   If `KeyColor` is Azure (8), `ColorsToRemove` = {Blue (1), Orange (7), Azure (8)}.
    *   Otherwise, `ColorsToRemove` is an empty set.
6.  Create a new set of coordinates, `KeptPayloadCoords`, containing only the coordinates `(r, c)` from `PayloadCoords` where the color of the input grid at `(r, c)` is *not* in `ColorsToRemove`.
7.  If `KeptPayloadCoords` is empty, return an empty grid represented as `[[]]`.
8.  Calculate the minimum bounding box that encloses all coordinates in `KeptPayloadCoords`. Let the top-left corner be `(min_r, min_c)` and the bottom-right corner be `(max_r, max_c)`.
9.  Calculate the dimensions of the output grid: `height = max_r - min_r + 1`, `width = max_c - min_c + 1`.
10. Create a new output grid of size `(height, width)`, initialized entirely with white (0).
11. Iterate through each coordinate `(r, c)` in `KeptPayloadCoords`:
    *   Get the `CurrentColor` from the input grid at `(r, c)`.
    *   Calculate the corresponding position in the output grid: `out_r = r - min_r`, `out_c = c - min_c`.
    *   Set the pixel in the output grid at `(out_r, out_c)` to `CurrentColor`.
12. Return the generated output grid.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-white color in the grid using Breadth-First Search (4-connectivity).
    Sorts objects by size descending, then by top-most row, then left-most column for tie-breaking.

    Args:
        grid (np.array): Input grid.

    Returns:
        list: A list of objects, sorted by size (desc), then top-row (asc), then left-col (asc).
              Each object is a dictionary containing 'color' (int), 'coords' (set of (r, c) tuples),
              'size' (int), 'min_r' (int), and 'min_c' (int).
              Excludes objects with color 0 (white). Returns empty list if no non-white objects found.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If the cell hasn't been visited and is not white (0)
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c)) # Mark start node visited immediately
                min_r_obj, min_c_obj = r, c # Keep track of top-left for tie-breaking

                # Start BFS from this cell
                while q:
                    row, col = q.popleft()
                    # Update min row/col for this object
                    min_r_obj = min(min_r_obj, row)
                    min_c_obj = min(min_c_obj, col)
                    # Add the current coordinate to the object
                    obj_coords.add((row, col))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if the neighbor is within bounds, not visited, and has the same color
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc)) # Mark neighbor visited when adding to queue
                            q.append((nr, nc))

                # Add the found object to the list
                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'size': len(obj_coords),
                    'min_r': min_r_obj,
                    'min_c': min_c_obj
                })

    # Sort by size descending, then row ascending, then col ascending
    objects.sort(key=lambda o: (-o['size'], o['min_r'], o['min_c']))
    return objects

def get_bounding_box(coords):
    """
    Calculates the bounding box for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col), or None if coords is empty.
    """
    if not coords:
        return None

    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)

    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Applies the transformation based on the natural language program.
    """
    input_array = np.array(input_grid, dtype=int)

    # 1. & 2. Find all non-white objects and identify the largest (with tie-breaking)
    objects = find_objects(input_array)

    # Handle edge case: no non-white objects found
    if not objects:
        return [[]] # Return empty list for empty grid

    largest_object = objects[0] # Largest is first due to sorting
    key_color = largest_object['color']
    key_object_coords = largest_object['coords']

    # 3. Identify PayloadPixels (all non-white pixels NOT in the largest object)
    all_non_white_coords = set(zip(*np.where(input_array != 0)))
    payload_coords = all_non_white_coords - key_object_coords

    # 4. Handle case where no payload pixels exist
    if not payload_coords:
         return [[]] # Return empty list for empty grid

    # 5. Determine ColorsToRemove based on KeyColor
    colors_to_remove = set()
    if key_color == 3: # Green Key
        colors_to_remove = {3, 9} # Remove Green, Maroon
    elif key_color == 1: # Blue Key
        colors_to_remove = {1, 2, 4, 9} # Remove Blue, Red, Yellow, Maroon
    elif key_color == 8: # Azure Key
        colors_to_remove = {1, 7, 8} # Remove Blue, Orange, Azure
    # Otherwise, colors_to_remove remains empty

    # 6. Filter payload coordinates to get KeptPayloadCoords
    kept_payload_coords = set()
    for r, c in payload_coords:
        if input_array[r, c] not in colors_to_remove:
            kept_payload_coords.add((r, c))

    # 7. Handle case where no payload pixels are kept after filtering
    if not kept_payload_coords:
         return [[]] # Return empty list for empty grid

    # 8. Calculate the bounding box of the kept coordinates
    min_r, min_c, max_r, max_c = get_bounding_box(kept_payload_coords)

    # 9. Calculate output dimensions
    out_height = max_r - min_r + 1
    out_width = max_c - min_c + 1

    # 10. Create the output grid, initialized with white (0)
    output_grid = np.zeros((out_height, out_width), dtype=int)

    # 11. Populate the output grid with kept payload pixels, adjusting coordinates
    for r, c in kept_payload_coords:
        current_color = input_array[r, c]
        # Calculate the position in the output grid relative to the bounding box origin
        out_r = r - min_r
        out_c = c - min_c
        # Place the color in the output grid
        output_grid[out_r, out_c] = current_color

    # 12. Return the result as a list of lists
    return output_grid.tolist()
```