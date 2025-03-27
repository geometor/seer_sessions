"""
Identifies the largest connected object in the input grid as the 'pattern' and the smallest connected objects as 'markers'. 
It then copies the input grid to the output grid and stamps copies of the 'pattern' onto the output grid. 
Each pattern copy is centered on the location of each pixel belonging to any 'marker' object.

1.  **Identify Background:** Determine the background color by finding the most frequent color in the input grid.
2.  **Find Objects:** Identify all distinct connected objects (contiguous groups of same-colored pixels, using 8-way adjacency) that are *not* the background color. For each object, note its color, size (pixel count), pixel coordinates, and bounding box.
3.  **Identify Pattern Object:** Find the object with the largest size. This is the 'pattern object'. Record its color, its pixel coordinates relative to its bounding box's top-left corner (its shape), and calculate the relative center offset of its bounding box (`row_offset = bbox_height // 2`, `col_offset = bbox_width // 2`).
4.  **Identify Marker Colors:** Find the minimum size among all non-background objects. Identify the set of all distinct colors associated with objects of this minimum size. These are the 'marker colors'.
5.  **Find Marker Locations:** Locate all pixels in the *original input grid* that have any of the identified 'marker colors'. These coordinates are the 'marker locations'.
6.  **Initialize Output:** Create the output grid by making an exact copy of the input grid.
7.  **Stamp Pattern Copies:** For each 'marker location' `(marker_row, marker_col)`:
    *   Calculate the intended top-left coordinate `(target_top_left_row, target_top_left_col)` for placing the pattern copy by aligning the pattern's bounding box center offset with the marker location.
    *   Iterate through each relative pixel coordinate `(rel_row, rel_col)` defining the pattern's shape.
    *   Calculate the destination coordinate `(dest_row, dest_col)` on the output grid.
    *   If the destination coordinate is within the grid bounds, change the color of the pixel at this location in the output grid to the pattern object's color (overwriting the previous color).
8.  **Return Output:** The modified grid after processing all marker locations is the final output.
"""

import numpy as np
from collections import Counter, deque

def find_connected_objects(grid, background_color):
    """
    Finds all connected objects in the grid using BFS, excluding the background color.
    Uses 8-way adjacency.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore.

    Returns:
        dict: A dictionary where keys are object IDs (1-based) and values are
              dictionaries containing 'color', 'coords' (list of tuples),
              'size', and 'bbox' (tuple: min_r, min_c, max_r, max_c).
    """
    objects = {}
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    obj_id_counter = 0

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color and not visited[r, c]:
                # Start BFS for a new object
                obj_id_counter += 1
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_coords = []
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc

                            # Check bounds, color match, and visited status
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Store found object
                objects[obj_id_counter] = {
                    'color': color,
                    'coords': current_object_coords,
                    'size': len(current_object_coords),
                    'bbox': (min_r, min_c, max_r, max_c) # Store as tuple: min_r, min_c, max_r, max_c
                }
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Identify Background Color
    if input_grid_np.size == 0:
        return [] # Handle empty grid case
    color_counts = Counter(input_grid_np.flatten())
    # Handle case where grid has only one color or is uniform
    if not color_counts:
         background_color = 0 # Default if truly empty? Should be caught by size check.
    else:
        background_color = color_counts.most_common(1)[0][0]


    # 2. Find Non-Background Objects
    all_objects = find_connected_objects(input_grid_np, background_color)

    # Edge Case: No non-background objects found
    if not all_objects:
        return input_grid # Return original grid as list of lists

    # 3. Identify Pattern Object (Largest)
    pattern_obj_id = max(all_objects, key=lambda k: all_objects[k]['size'])
    pattern_obj = all_objects[pattern_obj_id]
    pattern_color = pattern_obj['color']
    pattern_coords_absolute = pattern_obj['coords']
    min_r, min_c, max_r, max_c = pattern_obj['bbox']

    # Calculate pattern shape relative to its bounding box top-left
    pattern_coords_relative = []
    for r_abs, c_abs in pattern_coords_absolute:
        pattern_coords_relative.append((r_abs - min_r, c_abs - min_c))

    # Calculate relative center offset of the pattern's bounding box
    bbox_height = max_r - min_r + 1
    bbox_width = max_c - min_c + 1
    center_dr = bbox_height // 2
    center_dc = bbox_width // 2

    # 4. Identify Marker Color(s) (Color(s) of Smallest Object(s))
    if not all_objects: # Should be caught earlier, but defensive check
        min_size = 0
    else:
        min_size = min(obj['size'] for obj in all_objects.values())
        
    marker_colors = set(obj['color'] for obj in all_objects.values() if obj['size'] == min_size)

    # 5. Find Marker Locations (all pixels with marker colors)
    marker_locations = []
    if marker_colors: # Only search if marker colors exist
        marker_locations = list(zip(*np.where(np.isin(input_grid_np, list(marker_colors)))))
        # The above is equivalent to:
        # for r in range(height):
        #     for c in range(width):
        #         if input_grid_np[r, c] in marker_colors:
        #             marker_locations.append((r, c))

    # 6. Initialize Output Grid (as a copy of the input)
    output_grid = np.copy(input_grid_np)

    # 7. Stamp Pattern Copies onto the Output Grid
    for marker_r, marker_c in marker_locations:
        # a. Calculate target top-left for placing the pattern copy
        target_top_left_r = marker_r - center_dr
        target_top_left_c = marker_c - center_dc

        # b. Iterate through pattern's relative coordinates
        for rel_r, rel_c in pattern_coords_relative:
            # c. Calculate destination coordinate
            dest_r = target_top_left_r + rel_r
            dest_c = target_top_left_c + rel_c

            # d. Check bounds
            if 0 <= dest_r < height and 0 <= dest_c < width:
                # e. Set pixel color (overwrite)
                output_grid[dest_r, dest_c] = pattern_color

    # 8. Final Output (convert back to list of lists)
    return output_grid.tolist()