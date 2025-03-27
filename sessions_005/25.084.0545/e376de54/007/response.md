```python
"""
1.  **Identify Objects:** Determine all contiguous regions (objects) of the same color in the input grid. Consider only horizontal and vertical neighbors when grouping pixels into objects.
2.  **Identify Horizontal Segments:** Within each object and for each row, identify all contiguous horizontal segments, noting their starting column, ending column, and color.
3.  **Conditional Segment Replacement:** For each row within each object:
    *   If the row contains one or more *single-pixel* segments of colors *different* from the color of a *multi-pixel* segment in that row, replace the background pixels between the minimum `start_col` and the maximum `end_col` among all single pixels in that row and that object with the original color of the *multi-pixel* segment.
4.  **Background:** Pixels not part of any identified and extended object retain their original input color (implicitly handled by only modifying specific segments).
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects in a grid.

    Args:
        grid: A 2D numpy array.

    Returns:
        A list of objects, where each object is a list of (row, col) tuples.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object, color):
        visited.add((r, c))
        current_object.append((r, c))

        neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        for nr, nc in neighbors:
            if is_valid(nr, nc) and (nr, nc) not in visited and grid[nr, nc] == color:
                dfs(nr, nc, current_object, color)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object, grid[r, c])
                objects.append(current_object)
    return objects

def get_horizontal_segments(grid):
    """
    Identifies contiguous horizontal segments in a grid.

    Args:
        grid: A 2D numpy array.

    Returns:
        A list of dictionaries, each representing a segment.
    """
    segments = []
    rows, cols = grid.shape
    for row_index in range(rows):
        row = grid[row_index,:]
        start_col = -1
        for i, color in enumerate(row):
            if start_col == -1:
                start_col = i
            elif color != row[start_col]:
                segments.append({
                    "row": row_index,
                    "start_col": start_col,
                    "end_col": i,
                    "color": row[start_col]
                })
                start_col = i
            # Handle last segment
        if start_col != -1:
            segments.append({
              "row": row_index,
              "start_col": start_col,
              "end_col": len(row),
              "color": row[start_col]
            })
    return segments
def transform(input_grid):
    # initialize output_grid
    output_grid = input_grid.copy()
    objects = find_objects(input_grid)
    segments = get_horizontal_segments(input_grid)

    for obj in objects:
      # Get all row indices in the object
      obj_rows = sorted(list(set(r for r, _ in obj)))

      for row_index in obj_rows:
        #find single pixels in row and object
        single_pixels = []
        for c in range(input_grid.shape[1]):
          if (row_index,c) in obj and any(s['row'] == row_index and s['start_col'] == c and s['end_col'] == c + 1 for s in segments):
            single_pixels.append((row_index,c))

        #find segments in row
        row_segments = [s for s in segments if s['row'] == row_index]

        for seg in row_segments:
          # If row contains one or more *single-pixel* segments of colors *different* from the color of a *multi-pixel* segment in that row
          if seg['end_col'] - seg['start_col'] > 1: #multi pixel
            different_color_single_pixels = [p for p in single_pixels if input_grid[p] != seg['color']]
            if different_color_single_pixels:
               # replace the background pixels between the minimum `start_col` and the maximum `end_col` among all single pixels
              min_col = min(c for _, c in different_color_single_pixels)
              max_col = max(c for _, c in different_color_single_pixels)

              for c in range(min_col+1, max_col):
                output_grid[row_index,c] = seg['color']
    return output_grid
```