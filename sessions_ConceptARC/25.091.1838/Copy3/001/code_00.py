import numpy as np
from scipy.spatial.distance import euclidean
from collections import deque

"""
Transforms an input grid based on its width:

1. If the grid width is even:
   - The output grid is formed by copying the left half of the input grid onto the right half. The left half remains unchanged.

2. If the grid width is odd:
   - Identify a marker object: a horizontal 1x2 block of magenta pixels ([[6, 6]]).
   - Find the instance of this marker object whose top-left corner is closest to the geometric center of the grid. The coordinates (r_marker, c_marker) of this marker's top-left corner define an offset vector.
   - If no marker is found, the output is identical to the input.
   - Identify all distinct connected objects (contiguous blocks of the same non-white color) in the input grid.
   - For each object *except* the specific marker object used for the offset:
     - Copy the object to a new location in the output grid by adding the offset (r_marker, c_marker) to the coordinates of each pixel in the object.
     - Only pixels landing within the grid boundaries are placed.
     - Copied pixels overwrite the existing content at the target location. The original grid content and objects (including the marker) remain unless overwritten.
"""

def find_objects(grid, colors_to_ignore=[0]):
    """
    Finds all connected objects of the same color in the grid.

    Args:
        grid (np.array): The input grid.
        colors_to_ignore (list): List of color values to ignore (background).

    Returns:
        list: A list of tuples, where each tuple represents an object:
              (color, set_of_coordinates, top_left_coordinate).
              set_of_coordinates is a set of (row, col) tuples.
              top_left_coordinate is a tuple (min_row, min_col).
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color not in colors_to_ignore and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append((color, obj_coords, (min_r, min_c)))
    return objects

def find_pattern(grid, pattern):
    """
    Finds all occurrences of a given pattern in the grid.

    Args:
        grid (np.array): The input grid.
        pattern (np.array): The pattern to search for.

    Returns:
        list: A list of (row, col) tuples representing the top-left coordinates
              of found pattern instances.
    """
    grid_h, grid_w = grid.shape
    pattern_h, pattern_w = pattern.shape
    locations = []

    for r in range(grid_h - pattern_h + 1):
        for c in range(grid_w - pattern_w + 1):
            subgrid = grid[r:r+pattern_h, c:c+pattern_w]
            if np.array_equal(subgrid, pattern):
                locations.append((r, c))
    return locations

def transform(input_grid):
    """
    Applies the transformation rule based on grid width.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_np = np.copy(input_np) # Start with a copy

    # Check if width is even or odd
    if width % 2 == 0:
        # Even width: Mirror left half to right half
        mid = width // 2
        left_half = input_np[:, :mid]
        output_np[:, mid:] = left_half
    else:
        # Odd width: Offset copy based on marker
        marker_pattern = np.array([[6, 6]]) # Magenta 1x2 block
        marker_locations = find_pattern(input_np, marker_pattern)

        if not marker_locations:
            # No marker found, return the copy of the input
            return output_np.tolist()

        # Calculate grid center
        center_r = (height - 1) / 2.0
        center_c = (width - 1) / 2.0
        grid_center = (center_r, center_c)

        # Find the marker closest to the center
        closest_marker_loc = min(
            marker_locations,
            key=lambda loc: euclidean(loc, grid_center)
        )
        r_marker, c_marker = closest_marker_loc
        offset_dr, offset_dc = r_marker, c_marker

        # Find all objects
        objects = find_objects(input_np, colors_to_ignore=[0]) # Ignore white background

        # Iterate through objects and copy them with offset, skipping the chosen marker
        for color, coords, top_left_coord in objects:
            # Check if this object is the chosen marker
            is_marker = False
            # For a 1x2 marker, the top_left_coord is sufficient to identify it
            if top_left_coord == closest_marker_loc and color == 6: 
                 # Basic check, might need refinement if other magenta objects exist
                 # Let's be more specific: check if the object's pixels exactly match the marker pattern relative to top_left
                 obj_pixels_relative = {(r - top_left_coord[0], c - top_left_coord[1]) for r, c in coords}
                 marker_pixels_relative = {(0,0), (0,1)} # For [[6, 6]] pattern
                 if obj_pixels_relative == marker_pixels_relative:
                     is_marker = True

            if not is_marker:
                # Copy this object with offset
                for r_p, c_p in coords:
                    target_r = r_p + offset_dr
                    target_c = c_p + offset_dc

                    # Check grid boundaries
                    if 0 <= target_r < height and 0 <= target_c < width:
                        output_np[target_r, target_c] = color

    # Convert back to list of lists before returning
    return output_np.tolist()