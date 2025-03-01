# 045e512c • 010 • refine_coder

---
```python
"""
Transforms an input grid containing a "cross" shape by expanding and replicating the cross's colored pixels (red and yellow) in a mirrored pattern, with the blue pixel acting as the center.  The blue pixel is also moved to the vertical center.
"""

import numpy as np

def find_center(grid):
    # Find the blue pixel, assumed to be the center
    blue_pixels = np.argwhere(grid == 1)
    if blue_pixels.size == 0:
      return None
    return blue_pixels[0]

def find_adjacent_segments(grid, center, color):
  segments = []
  rows, cols = grid.shape
  r, c = center

  # Check for adjacent pixels in all 8 directions
  for dr in [-1, 0, 1]:
    for dc in [-1, 0, 1]:
      if dr == 0 and dc == 0:
        continue  # Skip the center pixel itself

      nr, nc = r + dr, c + dc
      if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color:
          segments.append((nr, nc))
  return segments

def replicate_red(grid, center, red_segments):
  output_grid = np.copy(grid)
  rows, cols = grid.shape
  center_row, center_col = center

  for r_seg in red_segments:
    row_offset = r_seg[0] - center_row
    col_offset = r_seg[1] - center_col
    
    # Mirrored position
    mirrored_row = center_row - row_offset
    
    # Extend red to left edge
    for c in range(0, r_seg[1] + 1):
        output_grid[r_seg[0], c] = 2
        
    # Extend mirrored red to right edge
    for c in range(mirrored_row,cols):
      output_grid[mirrored_row,c] = 2

    # Fill between red lines
    fill_start = min(r_seg[0], mirrored_row)
    fill_end = max(r_seg[0], mirrored_row)

    for r in range(fill_start+1, fill_end):
        for c in range(cols):
          if output_grid[r,c] != 4:
            output_grid[r, c] = 2

  return output_grid

def replicate_yellow(grid, center, yellow_segments):
  output_grid = np.copy(grid)
  rows, _ = output_grid.shape
  center_row, center_col = center

  for y_seg in yellow_segments:
    col_offset = y_seg[1] - center_col
    for r in range(rows):
      output_grid[r,center_col + col_offset] = 4

  return output_grid

def move_center(grid, center):
    output_grid = np.copy(grid)
    rows, cols = grid.shape
    center_row, center_col = center

    new_center_row = rows // 2
    output_grid[center_row, center_col] = 0  # Clear original center
    output_grid[new_center_row, center_col] = 1 # Place in new center

    return output_grid

def transform(input_grid):
  # initialize output_grid
  output_grid = np.copy(input_grid)

  # Find the center (blue pixel)
  center = find_center(input_grid)
  if center is None:  # Handle cases where there's no blue pixel
      return output_grid
    
  # find red segments
  red_segments = find_adjacent_segments(input_grid, center, 2)

  # find yellow segments
  yellow_segments = find_adjacent_segments(input_grid,center, 4)
    
  # Replicate red and fill
  output_grid = replicate_red(output_grid, center, red_segments)

  # replicate yellow
  output_grid = replicate_yellow(output_grid, center, yellow_segments)

  # Move Blue to Vertical Center
  output_grid = move_center(output_grid, center)

  return output_grid
```
