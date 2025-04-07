```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all contiguous objects (non-white pixels, 4-way adjacency).
2. Identify colors of single-pixel objects as 'ignored colors'.
3. Filter out objects whose color is ignored. These are 'kept objects'.
4. Find the largest kept object (by pixel count). This is the 'background object'. Its color is the 'background color'.
5. Calculate the bounding box of the background object.
6. Determine the output grid dimensions as twice the height and twice the width of the background object's bounding box.
7. Create the output grid filled with the background color.
8. Identify all other kept objects as 'foreground objects'.
9. Determine the minimal bounding box containing all pixels of all foreground objects ('foreground group bbox').
10. Copy the pixels of the foreground objects from the input grid into the output grid. The placement logic aims to preserve the relative arrangement of foreground objects. A simple placement strategy is used here: map the top-left corner of the foreground group bbox in the input to the top-left corner (0,0) of the output grid, copying only the foreground pixels within the output grid's bounds.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-background (non-white) pixels in the grid using 4-way adjacency.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (a set of (r, c) tuples), 'size',
              and 'bbox' (min_r, min_c, max_r, max_c).
              Returns an empty list if the grid is empty or only contains white (0).
    """
    if grid is None or grid.size == 0:
        return []

    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color_val = 0 # Assuming white is the background to ignore during object finding

    for r in range(rows):
        for c in range(cols):
            # Check if pixel is non-white and not visited
            if grid[r, c] != background_color_val and not visited[r, c]:
                color = grid[r, c]
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    current_object_pixels.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if neighbor has the same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if current_object_pixels:
                    objects.append({
                        'color': color,
                        'pixels': current_object_pixels,
                        'size': len(current_object_pixels),
                        'bbox': (min_r, min_c, max_r, max_c) # top, left, bottom, right
                    })

    return objects

def get_bbox_dims(bbox):
    """Calculates height and width from a bbox tuple."""
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def transform(input_grid):
    """
    Transforms the input grid based on the derived rules.
    """
    # 1. Identify all non-white objects
    objects = find_objects(input_grid)

    if not objects:
        # Handle empty input or input with only background
        # Return a 1x1 white grid as a default for empty cases
        return np.array([[0]], dtype=int)

    # 2. Identify ignored colors (from single-pixel objects)
    ignored_colors = set()
    for obj in objects:
        if obj['size'] == 1:
            ignored_colors.add(obj['color'])

    # 3. Filter kept objects
    kept_objects = [obj for obj in objects if obj['color'] not in ignored_colors]

    if not kept_objects:
         # Handle case where all objects are ignored
         # Return a 1x1 white grid
         return np.array([[0]], dtype=int)

    # 4. Find background object (largest kept object)
    background_object = max(kept_objects, key=lambda obj: obj['size'])
    background_color = background_object['color']
    bg_bbox = background_object['bbox']

    # 5. Calculate output grid dimensions (double the background object's bbox dims)
    bg_bbox_h, bg_bbox_w = get_bbox_dims(bg_bbox)
    output_height = bg_bbox_h * 2
    output_width = bg_bbox_w * 2

    # 6. Create output grid filled with background color
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    # 7. Identify foreground objects
    foreground_objects = [obj for obj in kept_objects if obj != background_object]

    if not foreground_objects:
        # If no foreground objects, return the background-filled grid
        return output_grid

    # 8. Determine the combined bounding box of all foreground objects
    all_fg_pixels = set().union(*[obj['pixels'] for obj in foreground_objects])
    if not all_fg_pixels:
       # Should not happen if foreground_objects is not empty, but safety check
       return output_grid

    fg_min_r = min(r for r, c in all_fg_pixels)
    fg_min_c = min(c for r, c in all_fg_pixels)
    # max_r and max_c not strictly needed for this placement strategy, but good to have
    # fg_max_r = max(r for r, c in all_fg_pixels)
    # fg_max_c = max(c for r, c in all_fg_pixels)


    # 9. & 10. Place foreground objects onto the output grid
    # Placement Strategy: Map the top-left of the foreground group's bbox
    # (fg_min_r, fg_min_c) to the output grid's origin (0, 0).
    placement_offset_r = 0 - fg_min_r
    placement_offset_c = 0 - fg_min_c

    for obj in foreground_objects:
        obj_color = obj['color']
        for r, c in obj['pixels']:
            # Calculate position relative to the output grid's origin
            out_r = r + placement_offset_r
            out_c = c + placement_offset_c

            # Place the pixel if it's within the output grid bounds
            if 0 <= out_r < output_height and 0 <= out_c < output_width:
                 output_grid[out_r, out_c] = obj_color

    return output_grid
```