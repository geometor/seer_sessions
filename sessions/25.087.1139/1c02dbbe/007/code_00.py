import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1. Identify the largest contiguous object composed of gray pixels (color 5) in the input grid. If no gray pixels exist, return the input grid unchanged.
2. Identify all non-white (0), non-gray (5) colored pixels in the input grid. These are considered 'marker' pixels.
3. Group these marker pixels by their color.
4. For each group of markers of the same color, determine the minimal bounding box that encloses all markers in that group.
5. Create a new output grid initialized entirely with the background color (white, 0).
6. Iterate through each pixel coordinate (r, c) that belongs to the largest gray object identified in step 1.
7. For each such gray pixel coordinate (r, c):
    a. Determine how many marker bounding boxes (calculated in step 4) contain this coordinate (r, c).
    b. Count the number of containing bounding boxes.
    c. If exactly one bounding box contains the coordinate (r, c), set the corresponding pixel in the output grid to the color of that bounding box's markers.
    d. If zero or more than one bounding box contains the coordinate (r, c), set the corresponding pixel in the output grid to gray (5).
8. Iterate through each group of marker pixels identified in step 3.
9. For each marker pixel (r, c) with color `marker_color` belonging to a group with bounding box `bbox = (min_r, max_r, min_c, max_c)`:
    a. Check if the marker pixel is *strictly inside* its bounding box: `min_r < r < max_r` AND `min_c < c < max_c`.
    b. If the marker pixel is strictly inside its bounding box, set the corresponding pixel `output_grid[r, c]` to `marker_color`. Note: This might overwrite pixels set in step 7 if a marker happens to be inside the gray area, but the problem constraints seem to avoid this. We prioritize the coloring from step 7 for pixels within the gray object's original area.
10. Pixels in the output grid that do not correspond to the largest gray object *and* are not preserved internal markers remain white (0).
11. Return the resulting output grid.
"""

# Imports needed: numpy, deque from collections
# Helper functions: get_4_way_neighbors, find_largest_contiguous_object, get_bounding_box

def get_4_way_neighbors(r, c, height, width):
    """ Gets orthogonal neighbors within grid bounds. """
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def find_largest_contiguous_object(grid, target_color):
    """
    Finds the largest connected component of pixels with the target_color using BFS.
    Args:
      grid: numpy array representing the input grid.
      target_color: The integer color value to search for.
    Returns:
      A set of (row, col) tuples representing the coordinates of the largest object.
      Returns an empty set if no pixels of target_color are found.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    largest_object = set()

    for r in range(height):
        for c in range(width):
            # Start BFS if we find an unvisited pixel of the target color
            if grid[r, c] == target_color and not visited[r, c]:
                current_object = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_object.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Explore neighbors
                    for nr, nc in get_4_way_neighbors(row, col, height, width):
                        if grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            current_object.add((nr, nc))
                            q.append((nr, nc))
                
                # Keep track of the largest component found so far
                if len(current_object) > len(largest_object):
                    largest_object = current_object

    return largest_object

def get_bounding_box(pixels):
    """
    Calculates the bounding box containing all given pixel coordinates.
    Args:
      pixels: A list or set of (row, col) tuples.
    Returns:
      A tuple (min_row, max_row, min_col, max_col).
      Returns None if the input list is empty.
    """
    if not pixels:
        return None
    # Using np.min/max on array is faster for large sets
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    min_r = min(rows)
    max_r = max(rows)
    min_c = min(cols)
    max_c = max(cols)
    return (min_r, max_r, min_c, max_c)


def transform(input_grid):
    """
    Transforms the input grid based on the specified rules involving the largest gray object,
    external marker bounding boxes, and preserving markers strictly inside their boxes.
    
    Args:
      input_grid: A list of lists representing the input grid.
      
    Returns:
      A list of lists representing the transformed output grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape
    
    gray_color = 5
    background_color = 0

    # 1. Find the largest connected component of gray (5) pixels (the target object).
    target_object_pixels = find_largest_contiguous_object(input_grid_np, gray_color)
    
    # If there's no gray object, return the original grid.
    if not target_object_pixels:
        return input_grid # Return original input if no gray object

    # 2. Find all non-white (0), non-gray (5) pixels (marker pixels).
    # 3. Group marker pixels by color.
    marker_groups = {} # Group locations by color {color: [(r,c), ...]}
    all_marker_pixels = {} # Store all marker locations for later check { (r,c): color }
    for r in range(height):
        for c in range(width):
            color = input_grid_np[r, c]
            # Check if pixel is colored and not gray
            if color != background_color and color != gray_color:
                if color not in marker_groups:
                    marker_groups[color] = []
                marker_groups[color].append((r, c))
                all_marker_pixels[(r,c)] = color # Store location and color

    # 4. Calculate the bounding box for each group of marker colors.
    bounding_boxes = {} # {color: (min_r, max_r, min_c, max_c)}
    for color, pixels in marker_groups.items():
        if pixels: # Ensure the group is not empty
            bounding_boxes[color] = get_bounding_box(pixels)

    # 5. Create a new output grid initialized entirely with the background color (white, 0).
    output_grid = np.full_like(input_grid_np, background_color)

    # 6. Iterate through each pixel (r, c) of the target gray object.
    for r, c in target_object_pixels:
        # 7a. Determine covering bounding boxes
        covering_colors = []
        for color, bbox in bounding_boxes.items():
             if bbox: # Check if bbox exists
                min_r, max_r, min_c, max_c = bbox
                if min_r <= r <= max_r and min_c <= c <= max_c:
                    covering_colors.append(color)
        
        num_covering_boxes = len(covering_colors)

        # 7c. If exactly one bounding box covers it, change the output pixel's color.
        if num_covering_boxes == 1:
            output_grid[r, c] = covering_colors[0]
        # 7d. If 0 or >1 boxes cover it, set the output pixel to gray.
        else:
            output_grid[r, c] = gray_color

    # 8. Iterate through each original marker pixel location.
    # 9. Check if the marker is strictly inside its group's bounding box.
    for (r, c), marker_color in all_marker_pixels.items():
        # Check if this pixel was part of the original gray object; if so, its color is already determined.
        if (r, c) in target_object_pixels:
            continue # Skip, color already set by gray object logic

        # Get the bounding box for this marker's color
        bbox = bounding_boxes.get(marker_color)
        if bbox:
            min_r, max_r, min_c, max_c = bbox
            # 9a. Check if the marker pixel is *strictly inside* its bounding box
            is_strictly_inside = (min_r < r < max_r) and (min_c < c < max_c)
            
            # 9b. If strictly inside, set the output grid pixel to the marker color
            if is_strictly_inside:
                 output_grid[r, c] = marker_color

    # 10. Pixels not part of the gray object or preserved markers remain background (already initialized).
    # 11. Return the modified grid as a list of lists.
    return output_grid.tolist()