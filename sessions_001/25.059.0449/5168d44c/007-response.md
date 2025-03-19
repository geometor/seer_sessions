# 5168d44c • 007 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find a rectangular block of *red* pixels.  Also, find a single row where two colors alternate (e.g., green, red, green, red).
2.  **Find Intersection:** Determine the segment of the alternating row that horizontally overlaps with the red block. Consider only the columns where both the red block and the alternating row exist.
3.  **Conditional Shift:** Within the identified segment of the alternating row, shift any *red* pixels one position to the *right*, but *only* if the position to the right is empty (white).
"""

import numpy as np

def find_object(grid, color, object_type="contiguous_block"):
    """Finds objects in the grid based on color and type."""
    if object_type == "contiguous_block":
        rows, cols = np.where(grid == color)
        if len(rows) == 0:
            return None
        
        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)

        # Check if it's contiguous
        if (max_row - min_row + 1) * (max_col - min_col + 1) == len(rows):
           return (min_row, max_row, min_col, max_col) # return boundaries of object
        else:
          return None

    return None

def find_alternating_row(grid):
    """Finds a row with a strict alternating two-color pattern."""
    for row_index in range(grid.shape[0]):
        row = grid[row_index]
        
        # Find unique non-zero colors
        unique_colors = np.unique(row[row != 0])
        if len(unique_colors) != 2:
            continue

        color1, color2 = unique_colors
        
        # Create the expected alternating pattern
        expected_pattern1 = np.tile([color1, color2], grid.shape[1])[:grid.shape[1]]
        expected_pattern2 = np.tile([color2, color1], grid.shape[1])[:grid.shape[1]]

        # Compare and return row info if match
        if np.array_equal(row, expected_pattern1) or np.array_equal(row, expected_pattern2):
          cols = np.where(row != 0)[0]
          return row_index, cols

    return None

def get_segment(grid, red_block_bounds, alternating_row_coords):
   """Extracts the segment of the alternating row that interacts with the red block"""
   
   if red_block_bounds is None or alternating_row_coords is None:
      return None

   _, _, red_min_col, red_max_col = red_block_bounds
   alt_row, alt_cols = alternating_row_coords

   # get the segment of the alternating_row that has columns with the red block
   segment_cols = alt_cols[(alt_cols >= red_min_col) & (alt_cols <= red_max_col)]
   if segment_cols.size == 0:
      return None
   
   return alt_row, segment_cols
   

def shift_segment(grid, segment_coords):
    """Shifts the red pixels in the identified segment one position to the right."""

    if segment_coords is None:
       return grid
    
    alt_row, segment_cols = segment_coords

    new_grid = np.copy(grid)

    # Filter only the red pixels within segment
    red_cols_in_segment = segment_cols[new_grid[alt_row,segment_cols] == 2]

    
    for col in reversed(red_cols_in_segment):  # Iterate in reverse to avoid overwriting
        if col + 1 < grid.shape[1]: # boundary check
          if grid[alt_row,col+1] == 0: # only move on empty
            new_grid[alt_row, col + 1] = 2
            new_grid[alt_row, col] = 0
    return new_grid

def transform(input_grid):
    """Transforms the input grid according to the described rule."""

    # 1. Identify Objects
    red_block_bounds = find_object(input_grid, color=2, object_type="contiguous_block")
    alternating_row_coords = find_alternating_row(input_grid)

    # 2. Segment Identification
    segment_coords = get_segment(input_grid, red_block_bounds, alternating_row_coords)
   
    # 3. Shift Segment
    output_grid = shift_segment(input_grid, segment_coords)

    # 4. return output grid

       
    return output_grid
```
