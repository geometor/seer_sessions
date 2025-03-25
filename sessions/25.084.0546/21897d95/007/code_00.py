"""
1.  **Object Identification:** Identify all contiguous regions of the same color in the input grid as distinct objects.

2.  **Frame Candidate Selection:**
    *   Identify objects in the *input* that could potentially be frames.  Frame candidates are objects that:
        *   Are rectangular.
        *   Have a large number of pixels relative to other objects.

3.  **Framed Object Candidate Selection:** Consider objects within the bounding box of the potential frame. Candidates must:

    *   Be a different color than the frame.
    *   Have a bounding box smaller than the frame.

4.  **Transformation Rule:**

    *   Iterate through all pairs of frame and object
    *   The largest identified rectangular object in the input grid becomes the "frame".
    *   Determine the dimensions of the output grid based on the bounding box of the frame.  If there isn't a clearly defined frame, the dimensions match the largest object bounding box.
    *   The second largest identified rectangular region becomes the framed object
    *   Fill the output grid:
        *   The "frame" object from the input is placed in the output.
        *   The "framed object" is replaced by a filled rectangle of another color within the dimensions of its bounding box. The new color is present in the output but not the input OR it's a color that's consistent across multiple examples
        *   Other objects that are rectangular are kept, with possible pixel changes but same color.

5.  **Ambiguity Resolution:** If multiple frame/framed object combinations are possible, prioritize those where the framed object's color change is consistent with other examples, or a new color not in the input is introduced.
"""

import numpy as np
from collections import defaultdict

def find_objects(grid):
    """
    Finds connected components (objects) in a grid.
    Returns a dictionary: {color: [(r, c), ...], ...}.
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
                objects[color].extend(dfs(r, c, color))
    return dict(objects)

def bounding_box(pixels):
    """Calculates the bounding box of a set of pixels."""
    if not pixels:
        return ((0, 0), (0, 0))
    rows, cols = zip(*pixels)
    return ((min(rows), min(cols)), (max(rows), max(cols)))

def is_rectangular(pixels, bbox):
    """Checks if a set of pixels forms a filled rectangle."""
    if not pixels:
        return False

    min_row, min_col = bbox[0]
    max_row, max_col = bbox[1]
    expected_pixels = (max_row - min_row + 1) * (max_col - min_col + 1)
    return len(pixels) == expected_pixels

def get_rectangle_pixels(bbox):
   """Return a list of (r,c) tuples for a rectangle"""
   pixels = []
   min_row,min_col = bbox[0]
   max_row,max_col = bbox[1]
   for r in range(min_row,max_row+1):
      for c in range(min_col,max_col+1):
         pixels.append((r,c))
   return pixels

def transform(input_grid):
    """Transforms the input grid according to the identified rules."""
    input_objects = find_objects(input_grid)

    # 1. Find potential frame objects (rectangular and large)
    frame_candidates = []
    for color, pixels in input_objects.items():
        bbox = bounding_box(pixels)
        if is_rectangular(pixels, bbox):
            frame_candidates.append((color, pixels, bbox))

    # Sort candidates by area (largest first)
    frame_candidates.sort(key=lambda x: len(x[1]), reverse=True)

    # Iterate through frame and framed object candidates
    for frame_color, frame_pixels, frame_bbox in frame_candidates:
        for framed_color, framed_pixels, framed_bbox in frame_candidates:
           if frame_color == framed_color:
              continue

           # init grid based on frame bbox
           min_row, min_col = frame_bbox[0]
           max_row, max_col = frame_bbox[1]

           output_grid = np.zeros((max_row+1,max_col+1),dtype=int)

           # place frame
           for r,c in frame_pixels:
              output_grid[r,c] = frame_color # keep color for now

           # find a color for the framed object, prioritize one not in input objects
           output_colors = set()
           for (r,c) in get_rectangle_pixels(framed_bbox):
                if r < output_grid.shape[0] and c < output_grid.shape[1]: # bounds check
                  output_colors.add(output_grid[r,c])
           available_colors = [c for c in input_objects if c != frame_color]
           new_framed_color = None

           # use color not in original input if available
           if len(available_colors) > 0:
               new_framed_color = available_colors[0]

           if new_framed_color is not None:
              for (r,c) in get_rectangle_pixels(framed_bbox):
                if r < output_grid.shape[0] and c < output_grid.shape[1]: # bounds check
                  output_grid[r,c] = new_framed_color
              return output_grid

    # default case
    return input_grid