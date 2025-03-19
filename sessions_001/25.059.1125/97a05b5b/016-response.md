# 97a05b5b • 016 • refine_coder

---
```python
"""
1.  **Identify the Repeating Pattern:** Within the input grid, locate the largest repeating subgrid pattern consisting of green (3) and yellow (4) pixels, bordered by red (2) pixels. This pattern appears to always have two rows.
2.  **Find the Top Border:** Find the continuous horizontal line of red (2) pixels immediately *above* the identified repeating pattern.
3.  **Extract:** Extract the section of the input grid, beginning with the row of the top red border.  The height and width of this extraction will be determined in the next step.
4. **Determine the output size:** The output size is the height and width of the repeating pattern and the bordering red rows above and below.
5.  **Output:** The extracted subgrid *is* the output.
"""

import numpy as np

def find_repeating_pattern(grid):
    # Find coordinates of all green (3) and yellow (4) pixels.
    pattern_coords = np.argwhere((grid == 3) | (grid == 4))

    if pattern_coords.size == 0:
        return None, None, None

    min_row = np.min(pattern_coords[:, 0])
    max_row = np.max(pattern_coords[:, 0])
    min_col = np.min(pattern_coords[:, 1])
    max_col = np.max(pattern_coords[:, 1])

    # assume the pattern is two rows, calculate the height.
    pattern_height = max_row - min_row + 1
    if pattern_height != 2:
      return None,None,None # pattern must be two rows

    pattern = grid[min_row:max_row + 1, min_col:max_col + 1]
    return pattern, min_row, min_col

def find_top_border(grid, pattern_row, pattern_col):
   # Search upwards from the pattern's starting row.
   for row in range(pattern_row - 1, -1, -1):
        # check the entire row for red
        if np.all(grid[row, :] == 2):
            return row
   return None # should not happen

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the repeating pattern and its location
    pattern, pattern_row, pattern_col = find_repeating_pattern(input_grid)
    
    # handle edge case
    if pattern is None:
      return []

    # find top border
    top_border_row = find_top_border(input_grid, pattern_row, pattern_col)
    
    # handle edge case
    if top_border_row is None:
      return []

    # get pattern height and width
    pattern_height, pattern_width = pattern.shape

    # Extract the pattern and its border
    # height includes the border rows above and below (+2)
    output_grid = input_grid[top_border_row:top_border_row + pattern_height + 2, :]

    return output_grid
```
