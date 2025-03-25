"""
1.  **Identify Framed Object:**
    *   Find the object in the *input* grid whose shape is most closely replicated (with possible color change, and filling) within the *output* grid. Consider multiple disconnected input components of the same color as potentially forming *one* object. This is our "framed object".
2.  **Identify Frame:**
    * Examine the *output* grid.
    * Find the largest rectangular contiguous region of pixels that "encloses" or "frames" a differently colored region (the transformed "framed object") within the output grid.
    * Find the colors in the *input* grid that *do not* take part of the "framed object".
3.  **Output Grid Construction:**
    *   The output grid's dimensions are defined by either the "frame" shape or the "framed object," whichever results in the largest complete rectangle that encompasses both.
    *   Populate the "frame" in the output using one of the colors that was *not* part of the "framed object" in the input.  The shape is maintained (or slightly modified to become a complete frame).
    *   Populate the "framed object" area in the output. This involves:
        *   Identifying the new color of the framed object (a color present in the output but not the input, if a new color is introduced).
        *   Filling the bounding box of the framed object's original shape with this new color (or a combination of new colors from the output).
"""

import numpy as np
from collections import defaultdict

def find_objects(grid):
    """
    Finds connected components (objects) in a grid, including single pixels.
    Returns a dictionary where keys are colors and values are lists of (row, col) tuples.
    """
    objects = defaultdict(list)
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return []
        visited.add((r, c))
        obj = [(r, c)]
        obj.extend(dfs(r + 1, c, color))
        obj.extend(dfs(r - 1, c, color))
        obj.extend(dfs(r, c + 1, color))
        obj.extend(dfs(r, c - 1, color))
        return obj

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                objects[color].extend(dfs(r,c,color)) # append pixels to existing
    return dict(objects)


def bounding_box(pixels):
    """
    Calculates the bounding box of a set of pixels.
    Returns ((min_row, min_col), (max_row, max_col)).
    """
    if not pixels:
        return ((0, 0), (0, 0))
    rows, cols = zip(*pixels)
    return ((min(rows), min(cols)), (max(rows), max(cols)))

def shape_similarity(pixels1, pixels2):
    """
    A very basic shape similarity metric.  Counts the number of pixels
    that overlap when the centroids of the two pixel sets are aligned.
    """
    if not pixels1 or not pixels2:
        return 0

    # Calculate centroids
    centroid1_row = sum(r for r, _ in pixels1) / len(pixels1)
    centroid1_col = sum(c for _, c in pixels1) / len(pixels1)
    centroid2_row = sum(r for r, _ in pixels2) / len(pixels2)
    centroid2_col = sum(c for _, c in pixels2) / len(pixels2)

    # Translate pixels to align centroids
    translated_pixels1 = {(r - centroid1_row, c - centroid1_col) for r, c in pixels1}
    translated_pixels2 = {(r - centroid2_row, c - centroid2_col) for r, c in pixels2}

    # Calculate overlap
    overlap = len(translated_pixels1.intersection(translated_pixels2))
    return overlap


def get_frame_and_framed_colors(input_objects, expected_output_objects):

    best_framed_color = None
    best_frame_color = None
    max_similarity = -1
    output_colors = set(expected_output_objects.keys())

    # find colors and combination of colors that best match output
    for input_color, input_pixels in input_objects.items():
            for output_color, output_pixels in expected_output_objects.items():
              similarity = shape_similarity(input_pixels, output_pixels)
              if similarity > max_similarity:
                    max_similarity = similarity
                    best_framed_color = input_color
                    
    # find colors that do not take part in the framed object
    frame_colors = [c for c in input_objects if c != best_framed_color]
    if len(frame_colors) > 0:
      best_frame_color = frame_colors[0]

    return best_framed_color, best_frame_color, output_colors
def transform(input_grid):
    input_objects = find_objects(input_grid)

    # Dummy expected output objects for development purposes.  In a real
    # scenario, we wouldn't have access to the expected output during
    # the transformation. We use it here *only* to infer the rule.
    # Create dummy output grid to simulate
    expected_output_grid = np.zeros_like(input_grid)
    expected_output_objects = find_objects(expected_output_grid)

    # get dimensions
    rows, cols = input_grid.shape
    output_grid = np.zeros((rows, cols), dtype=int)

    # Identify framed and frame object
    framed_color, frame_color, output_colors = get_frame_and_framed_colors(input_objects, expected_output_objects)

    if framed_color is None or frame_color is None:
        return output_grid

    # 3. **Output Grid Construction:**
    # Get pixels
    framed_pixels = input_objects.get(framed_color,[])
    frame_pixels = input_objects.get(frame_color,[])

    # determine output size
    framed_bbox = bounding_box(framed_pixels)
    frame_bbox = bounding_box(frame_pixels)
    out_max_row = max(framed_bbox[1][0], frame_bbox[1][0])
    out_max_col = max(framed_bbox[1][1], frame_bbox[1][1])

    output_grid = np.zeros((out_max_row + 1, out_max_col + 1), dtype=int)

    # fill frame
    new_frame_color = frame_color # Default to same color
    for color in output_colors:
        if shape_similarity(frame_pixels,expected_output_objects[color]) > 0:
            new_frame_color = color
            break
    for r, c in frame_pixels:
        if r <= out_max_row and c <= out_max_col:  # Check bounds
           output_grid[r, c] = new_frame_color

    # fill framed
    new_color = None
    for color in output_colors:
      if color != new_frame_color:
          new_color = color

    if new_color is not None:
      framed_min_row, framed_min_col = framed_bbox[0]
      framed_max_row, framed_max_col = framed_bbox[1]
      for r in range(framed_min_row, framed_max_row + 1):
          for c in range(framed_min_col, framed_max_col + 1):
              if r <= out_max_row and c <= out_max_col:
                output_grid[r, c] = new_color
    return output_grid