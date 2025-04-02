import numpy as np
from collections import deque, Counter
import math

"""
Identifies the two largest non-white objects in the input grid.
One object (source) contains an internal pattern composed of pixels of a single color different from the object's primary color and the background (white).
This pattern is then transferred to the second largest object (target).
The transfer is based on aligning the centers of the bounding boxes of the source and target objects.
The translation vector calculated from the center alignment is applied to the absolute coordinates of the source pattern pixels to determine their new locations in the output grid.
The pattern color replaces the existing color at these new target locations. All other pixels remain unchanged.
"""

def _get_neighbors(r, c, rows, cols):
    """ Helper function to get valid 8-way neighbors within grid bounds. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def _find_objects_bfs(grid):
    """ Finds connected components of non-white pixels using BFS. """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-white pixel and not yet visited, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                obj_colors = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                current_color = grid[r,c] # Color of the starting pixel of the component

                component_queue = deque([(r,c)]) # Use a separate queue for BFS within the same color component
                component_visited = set([(r,c)])

                while component_queue:
                    curr_r, curr_c = component_queue.popleft()

                    obj_pixels.append((curr_r, curr_c))
                    obj_colors.append(grid[curr_r, curr_c])

                    # Update bounding box coordinates
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors
                    for nr, nc in _get_neighbors(curr_r, curr_c, rows, cols):
                        # Add to component queue only if it has the same color and not visited for this component
                        if grid[nr, nc] == current_color and (nr, nc) not in component_visited:
                            visited[nr, nc] = True # Mark globally visited
                            component_visited.add((nr, nc))
                            component_queue.append((nr, nc))
                        # Also mark neighbors of different non-zero colors as visited to prevent starting BFS from them later
                        elif grid[nr,nc] != 0 and not visited[nr,nc]:
                             visited[nr, nc] = True # Mark globally visited so we don't start BFS from here

                if obj_pixels:
                    # Determine primary color (most frequent non-white, should be the component color here)
                    color_counts = Counter(obj_colors)
                    primary_color = color_counts.most_common(1)[0][0]

                    # Bounding box (inclusive max for coords, +1 for range/slicing)
                    bbox = (min_r, min_c, max_r + 1, max_c + 1)

                    objects.append({
                        'pixels': obj_pixels,
                        'bbox': bbox,
                        'primary_color': primary_color,
                        'size': len(obj_pixels)
                    })

    # Sort objects by size (descending)
    objects.sort(key=lambda o: o['size'], reverse=True)
    return objects

def _calculate_bbox_center(bbox):
    """ Calculates the center of a bounding box. """
    min_r, min_c, max_r, max_c = bbox
    center_r = min_r + (max_r - min_r) / 2.0
    center_c = min_c + (max_c - min_c) / 2.0
    return center_r, center_c

def transform(input_grid):
    """
    Transforms the input grid by copying an internal pattern from a source
    object to a target object, aligning by bounding box centers.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify all non-white objects
    # Using skimage.measure.label for potentially better handling of complex shapes
    # Revert to BFS if skimage is not allowed or fails
    try:
        from skimage.measure import label, regionprops
        labeled_grid = label(input_grid > 0, connectivity=2) # 8-way connectivity
        regions = regionprops(labeled_grid, intensity_image=input_grid)
        objects = []
        for region in regions:
             pixels = tuple(map(tuple, region.coords.T))
             if not pixels: continue
             non_white_colors = [c for c in region.intensity_image[region.image].flatten() if c != 0]
             if not non_white_colors: continue
             primary_color = Counter(non_white_colors).most_common(1)[0][0]
             objects.append({
                 'pixels': list(pixels),
                 'bbox': region.bbox, # (min_r, min_c, max_r, max_c) - exclusive max
                 'primary_color': primary_color,
                 'size': region.area # region.area should be count of non-zero pixels
             })
        objects.sort(key=lambda o: o['size'], reverse=True)

    except ImportError:
        # Fallback to BFS if skimage is not available
        print("Warning: skimage not found, using BFS for object detection.")
        objects = _find_objects_bfs(input_grid)


    # 2. Need at least two objects for the transformation
    if len(objects) < 2:
        return output_grid # No transformation possible

    # 3. Assume the two largest objects are the source/target pair
    obj_a = objects[0]
    obj_b = objects[1]

    # 4. Try to find the source, target, pattern color, and pattern absolute coordinates
    source_object = None
    target_object = None
    pattern_color = None
    pattern_coords_absolute = [] # Store absolute coordinates

    # Function to check an object for a pattern and return absolute coords
    def check_for_pattern(potential_source):
        bbox = potential_source['bbox']
        min_r, min_c, max_r, max_c = bbox # Exclusive max convention from regionprops/BFS bbox format
        primary_color = potential_source['primary_color']

        found_pattern = False
        potential_pattern_color = -1
        abs_coords = []

        # Iterate through the bounding box of the potential source
        for r in range(min_r, max_r):
            for c in range(min_c, max_c):
                 # Check grid bounds rigorously
                if 0 <= r < rows and 0 <= c < cols:
                    color = input_grid[r, c]
                    # Look for a color that is not background (0) and not the object's primary color
                    if color != 0 and color != primary_color:
                        # If this is the first pattern pixel found, store its color
                        if not found_pattern:
                            potential_pattern_color = color
                            found_pattern = True

                        # Ensure all pattern pixels have the same color (task assumption)
                        if color == potential_pattern_color:
                            # Store absolute coordinates
                            abs_coords.append((r, c))
                        else:
                            # Found a different internal color - this object doesn't fit the simple pattern model
                            return False, -1, []

        return found_pattern, potential_pattern_color, abs_coords

    # Check Object A as potential source
    found_in_a, color_a, coords_a = check_for_pattern(obj_a)
    if found_in_a:
        source_object = obj_a
        target_object = obj_b
        pattern_color = color_a
        pattern_coords_absolute = coords_a
    else:
        # Check Object B as potential source
        found_in_b, color_b, coords_b = check_for_pattern(obj_b)
        if found_in_b:
            source_object = obj_b
            target_object = obj_a
            pattern_color = color_b
            pattern_coords_absolute = coords_b

    # 5. If no source/pattern was identified, return the original grid
    if source_object is None or pattern_color is None or not pattern_coords_absolute:
        return output_grid

    # 6. Calculate centers and translation vector
    source_bbox = source_object['bbox']
    target_bbox = target_object['bbox']

    source_center_r, source_center_c = _calculate_bbox_center(source_bbox)
    target_center_r, target_center_c = _calculate_bbox_center(target_bbox)

    delta_r = target_center_r - source_center_r
    delta_c = target_center_c - source_center_c

    # 7. Apply the translated pattern to the target object locations in the output grid
    for src_r, src_c in pattern_coords_absolute:
        # Calculate target coordinates by applying the translation vector
        # Round to nearest integer for pixel coordinates
        target_r = round(src_r + delta_r)
        target_c = round(src_c + delta_c)

        # Check if the calculated coordinates are within the grid bounds
        if 0 <= target_r < rows and 0 <= target_c < cols:
            # Update the output grid with the pattern color at the target location
            output_grid[target_r, target_c] = pattern_color

    # 8. Return the modified grid
    return output_grid