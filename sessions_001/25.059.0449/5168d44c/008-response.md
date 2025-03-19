# 5168d44c • 008 • refine_coder

---
```python
"""
1.  **Identify Objects:**
    *   Find the horizontal "red_block" of contiguous red (2) pixels.
    *   Find the "alternating_row" containing alternating green (3) and red (2) pixels.

2.  **Identify Segment:**
    *   Within the "alternating_row", identify the "segment" of pixels that are *horizontally adjacent* to the "red_block".

3.  **Shift Segment:**
    *   Shift the red (2) pixels within the identified "segment" one position to the right. If a position to be moved to is currently green, the green pixel becomes red, if a position to be moved to is red, then it remains red.

4.  **Output:** The modified grid is the output.
"""

import numpy as np

def find_object(grid, color=None, object_type="contiguous_block"):
    """Finds objects in the grid based on color and type."""
    if object_type == "contiguous_block":
        rows, cols = np.where(grid == color)
        if len(rows) == 0:
            return None

        min_row, max_row = np.min(rows), np.max(rows)
        min_col, max_col = np.min(cols), np.max(cols)

        # Check if it's contiguous
        if (max_row - min_row + 1) * (max_col - min_col + 1) == len(rows):
            return (min_row, max_row, min_col, max_col)  # Return boundaries
        else:
            return None

    elif object_type == "alternating_row":
        for row_index in range(grid.shape[0]):
            row = grid[row_index]
            if is_alternating(row):
                cols = np.where(row != 0)[0] # get all non-zero columns in this row
                return row_index, cols
        return None

def is_alternating(row):
    """Checks if a row has an alternating pattern of green and red (3 and 2)."""
    non_zero_elements = row[row != 0]
    if len(non_zero_elements) < 2:
        return False

    # Check for strict alternation starting with either green or red
    for start_color in [2, 3]:
       is_valid = True
       for i in range(len(non_zero_elements)):
          expected_color = start_color if (i % 2 == 0) else (5 - start_color)
          if non_zero_elements[i] != expected_color:
              is_valid = False
              break
       if is_valid:
           return True
           
    return False

def get_segment(grid, red_block_bounds, alternating_row_coords):
    """Extracts the segment of the alternating row adjacent to the red block."""
    if red_block_bounds is None or alternating_row_coords is None:
        return None

    red_row_start, _, red_col_start, red_col_end = red_block_bounds
    alt_row, alt_cols = alternating_row_coords

    # Check if the alternating row is directly below the red block
    if alt_row != red_row_start + 1:
        return None

    segment_cols = []
    for col in alt_cols:
        if col >= red_col_start -1 and col <= red_col_end + 1: # adjacent, including diagonals
           segment_cols.append(col)
    
    return alt_row, np.array(segment_cols)

def shift_segment(grid, segment_coords):
    """Shifts the red pixels in the identified segment one position to the right."""
    if segment_coords is None:
        return grid

    alt_row, segment_cols = segment_coords
    new_grid = np.copy(grid)

    red_cols_in_segment = segment_cols[new_grid[alt_row, segment_cols] == 2]

    for col in reversed(red_cols_in_segment):  # Iterate in reverse to avoid overwriting
        if col + 1 < grid.shape[1]:  # Boundary check
            new_grid[alt_row, col + 1] = 2  # Always set to red
            if col not in red_cols_in_segment:
              new_grid[alt_row,col] = grid[alt_row,col] # original value
            else:
               # if original was red and now empty, make sure its not still original color
               if not (col+1 in red_cols_in_segment and new_grid[alt_row,col+1] == 2):
                  new_grid[alt_row,col] = grid[alt_row,col] # put back original color

    return new_grid

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    # 1. Identify Objects
    red_block_bounds = find_object(input_grid, color=2, object_type="contiguous_block")
    alternating_row_coords = find_object(input_grid, object_type="alternating_row")

    # 2. Segment Identification
    segment_coords = get_segment(input_grid, red_block_bounds, alternating_row_coords)

    # 3. Shift Segment
    output_grid = shift_segment(input_grid, segment_coords)

    # 4. Return output grid
    return output_grid
```
