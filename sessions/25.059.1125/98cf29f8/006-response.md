# 98cf29f8 • 006 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find a yellow (color 4) rectangle and a gray (color 5) object. The yellow rectangle remains unchanged.

2.  **Segment Gray Object:** Divide the gray object into two parts:
    *   **Vertical Line:** The longest vertical line of contiguous gray pixels within the gray object.
    *   **Remaining Pixels:** All gray pixels that are not part of the identified vertical line.

3.  **Remove Vertical Line:** Remove the vertical line part of the gray object from the grid (set pixels to black/0).

4.  **Reshape Remaining Pixels:** Reshape the remaining gray pixels into a 3x4 rectangle.

5.  **Position New Rectangle:** Place the newly formed 3x4 gray rectangle adjacent to the left of the yellow rectangle, aligned vertically with the yellow rectangle's top edge. If the gray rectangle is too large and would cover yellow, only fill in to the left, preserving the shape and size of the gray rectangle.
"""

import numpy as np

def find_object(grid, color):
    """Finds the bounding box of an object with the given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    return (min_row, min_col), (max_row, max_col)

def get_longest_vertical_line(grid, color):
    """Extracts coordinates of the longest gray vertical line."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return []

    col_counts = np.bincount(cols)
    if len(np.where(col_counts == np.max(col_counts))[0]) > 0:
       vertical_col = np.where(col_counts == np.max(col_counts))[0][0]
    else:
        return []
        
    coords = []
    min_row = -1

    for r in rows:
      if grid[r, vertical_col] == color:
         if min_row == -1:
            min_row = r
         coords.append((r, vertical_col))
      elif min_row != -1:
          break;
            
    return coords

def get_remaining_pixels(grid, color, vertical_line_coords):
    """Gets coordinates of gray pixels excluding the vertical line."""
    all_coords = list(zip(*np.where(grid == color)))
    remaining_coords = [coord for coord in all_coords if coord not in vertical_line_coords]
    return remaining_coords

def transform(input_grid):
    """Transforms the input grid according to the described rules."""
    
    output_grid = np.copy(input_grid)
    
    # Find the yellow rectangle (it remains unchanged)
    yellow_object = find_object(input_grid, 4)

    # Find and process gray structure
    gray_object = find_object(input_grid, 5)
   
    if gray_object:
        
      # Segment the gray object
      vertical_line_coords = get_longest_vertical_line(input_grid, 5)
      remaining_gray_coords = get_remaining_pixels(input_grid, 5, vertical_line_coords)

      # Remove vertical line
      for r, c in vertical_line_coords:
        output_grid[r, c] = 0

      # Create the new gray rectangle (3x4) from remaining pixels
      if remaining_gray_coords and yellow_object:
          #remove old gray object
          for r,c in remaining_gray_coords:
              output_grid[r,c] = 0

          yellow_top_left, _ = yellow_object
          new_top_left_row = yellow_top_left[0]
          new_top_left_col = yellow_top_left[1] - 4 #adjacent and left

          #make sure we don't go out of bounds
          new_top_left_col = max(0, new_top_left_col)


          for i in range(min(12, len(remaining_gray_coords))): #limit to 12
            row = new_top_left_row + i // 4
            col = new_top_left_col + i % 4
            if row < output_grid.shape[0] and col < output_grid.shape[1]:
              output_grid[row,col] = 5

    return output_grid
```
