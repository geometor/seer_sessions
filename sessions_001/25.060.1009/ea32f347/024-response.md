# ea32f347 • 024 • refine_coder

---
```tool_code
"""
1.  **Identify the Shape:** Locate the contiguous shape formed by gray (5) pixels in the input grid.
2.  **Segment Identification:** Divide the shape into three segments:
    *   A vertical line segment. The longest continuous line of gray pixels
        in a single column
    *   The horizontal segment attached to the vertical segment at some row.
    *   The horizontal segment attached to the vertical segment at some row.
3.  **Recolor Segments:**
    *   Change the color of the vertical line segment to blue (1).
    *   Change the color of the horizontal line segments based on their connection row:
        * If connection row is above the middle row of the vertical segment,
        color red (2).
        * If connection row is at or below the middle row, color yellow (4).
4.  **Maintain Background:** Keep all other pixels as white (0).
5. **Output**: produce the new grid with the shape segments and background.
"""

import numpy as np

def get_shape_pixels(grid, shape_color=5):
    # returns a list of (row, col) tuples representing the shape
    shape_pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == shape_color:
                shape_pixels.append((r, c))
    return shape_pixels

def segment_shape(shape_pixels):
    # segments shape to vertical and horizontal parts
    vertical_segment = []
    horizontal_segments = []

    # Find the main vertical line
    col_counts = {}
    for r, c in shape_pixels:
        if c not in col_counts:
            col_counts[c] = 0
        col_counts[c] += 1

    vertical_col = None
    for col, count in col_counts.items():
        if count > 2:  # Assuming vertical line has more than 2 pixels
            vertical_col = col
            break

    if vertical_col is not None:
      for r,c in shape_pixels:
        if c == vertical_col:
          vertical_segment.append((r,c))

    # divide horizontal components

    for r, c in shape_pixels:
      if (r,c) not in vertical_segment:
        horizontal_segments.append((r,c))
    return vertical_segment, horizontal_segments


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # get shape
    shape_pixels = get_shape_pixels(input_grid)

    # segment the shape
    vertical_segment, horizontal_segments = segment_shape(shape_pixels)

    # recolor vertical
    for r, c in vertical_segment:
        output_grid[r, c] = 1  # Blue

    # Determine middle row of vertical segment
    if vertical_segment:
      vertical_rows = [r for r, _ in vertical_segment]
      middle_row = (min(vertical_rows) + max(vertical_rows)) / 2


      # recolor horizontal segments based on connection point
      for r, c in horizontal_segments:
          if r < middle_row:
              output_grid[r, c] = 2  # Red
          else:
              output_grid[r, c] = 4  # Yellow

    return output_grid
```
