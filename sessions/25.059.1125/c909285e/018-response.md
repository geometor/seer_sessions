# c909285e • 018 • refine_coder

---
```python
"""
1.  **Identify Line:** Locate the lowest horizontal line of a single, uniform color within the input grid. The length of this line can vary.
2.  **Define Subgrid:** The subgrid starts at the beginning (leftmost pixel) of this line. The subgrid's dimensions matches the extent of the solid line of pixels.
3. **Extract Subgrid**: copy this subgrid for the output
4.  **Output:** The output is this extracted subgrid.
"""

import numpy as np

def find_lowest_line(grid):
    """Finds the lowest horizontal line of uniform color."""
    rows, cols = grid.shape
    for r in range(rows - 1, -1, -1):
        first_color = grid[r, 0]
        if first_color == 0:
          continue
        
        line_length = 0
        for c in range(cols):
            if grid[r, c] == first_color:
                line_length += 1
            else:
                break
        if line_length > 1 and all(grid[r,c] == first_color for c in range(line_length)):
            return r, 0, line_length #row, start_col, length
    return None, None, None

def transform(input_grid):
    """Transforms the input grid according to the identified rules."""

    # Find the lowest horizontal line.
    start_row, start_col, line_length = find_lowest_line(input_grid)

    if start_row is None:
        return None  # Or handle the case where no line is found

    # Define subgrid dimensions.
    subgrid_height = 0
    for r in range(start_row, -1, -1):
      first_color = input_grid[r, 0]
      if first_color == input_grid[start_row, 0]:
        subgrid_height += 1
      else:
        break;

    subgrid_width = line_length

    # Extract the subgrid.
    output_grid = input_grid[start_row - subgrid_height + 1:start_row + 1, start_col:start_col + subgrid_width]

    return output_grid
```
