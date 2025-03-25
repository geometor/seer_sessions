```python
"""
1.  **Background Replacement:** All background pixels (color 0) are replaced with color 3 (green).

2.  **Shape Identification and Processing**: Scan the input grid to find connected regions (shapes) of non-background pixels.
    * The *first* colored shape found has special handling. Find contiguous blocks of the same color.
    * All pixels of colors other than the first color found should have their color changed according to the following rule:
      * Color 2 changes to color 6

3.  **First Shape Expansion:** The *first* shape encountered during the scan expands by one pixel in all *orthogonal* directions (up, down, left, and right). If the expansion would cover a pixel that is not the background color (3) or the background color in the original image (0), it stops.

4. No other shapes are expanded.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    output_grid = np.full_like(input_grid, 3)  # Initialize with background color 3
    rows, cols = input_grid.shape
    first_shape_color = -1
    first_shape_pixels = []
    visited = set()

    def get_neighbors(r, c, orthogonal=False):
      """Gets the neighbors of a cell. Orthogonal only or diagonals"""
      neighbors = []
      deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)] if orthogonal else [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
      for dr, dc in deltas:
          nr, nc = r + dr, c + dc
          if 0 <= nr < rows and 0 <= nc < cols:
              neighbors.append((nr, nc))
      return neighbors
    
    def find_shape(r,c, color, visited):
      """finds a contiguous shape"""
      shape_pixels = []
      q = [(r,c)]
      while q:
        cr, cc = q.pop(0)
        if (cr,cc) in visited:
          continue
        visited.add((cr,cc))
        shape_pixels.append((cr,cc))
        for nr, nc in get_neighbors(cr, cc, orthogonal=True):
          if input_grid[nr,nc] == color:
            q.append((nr,nc))
      return shape_pixels
    
    # Find first shape and other shapes
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0 and (r,c) not in visited:
                if first_shape_color == -1:
                    first_shape_color = input_grid[r, c]
                    first_shape_pixels = find_shape(r,c, first_shape_color, visited)
                else:
                    current_color = input_grid[r,c]
                    current_shape = find_shape(r,c, current_color, visited)
                    new_color = current_color
                    if current_color == 2:
                      new_color = 6
                    for sr, sc in current_shape:
                      output_grid[sr,sc] = new_color
                      
    #Expand the first shape
    if first_shape_color != -1:
        for r, c in first_shape_pixels:
            output_grid[r, c] = first_shape_color  # Set the original shape pixels
        for r, c in first_shape_pixels:
          for nr, nc in get_neighbors(r, c, orthogonal=True):
            if input_grid[nr,nc] == 0:
              output_grid[nr,nc] = first_shape_color

    return output_grid
```