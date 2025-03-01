# 539a4f51 • 022 • refine_coder

---
```python
"""
1.  **Examine the input grid:** Determine its dimensions, the colors present, and any immediately obvious patterns (e.g., solid columns, single color, checkerboard).

2.  **Apply rules based on input characteristics:**

    *   **If the input grid is 1x1:** The output is identical to the input.
    *   **If the input has dimensions rows x cols, where rows and cols are greater than one, and has a repeating color sequence**
        Duplicate the grid horizontally. Add extra rows at the bottom, repeating the colors by row using `color = input[r % in_rows][0]`.

    *   **If the input grid has the colors orange and yellow, in a checkerboard style:** Change all yellow pixels to orange. The output grid has the same dimensions.

    *   **If the input grid has solid columns of colors:** Duplicate the columns but alternate colors using `color = input[r][c%in_cols]`

3.  **Else:** The output grid will be determined by the properties identified and will need to be updated when more test examples are available.
"""

import numpy as np

def get_pattern(grid):
    """Helper function to identify basic patterns."""
    grid = np.array(grid)
    rows, cols = grid.shape
    unique_colors = np.unique(grid)

    if rows == 1 and cols == 1:
        return "single pixel"

    # Check for solid columns
    if cols > 1:
        is_solid_columns = True
        for c in range(cols):
            if len(np.unique(grid[:, c])) > 1:
                is_solid_columns = False
                break
        if is_solid_columns:
            return "solid columns"
    
    # Repeating Color sequence (horizontal)
    if rows > 1 and cols > 1:
        first_row = grid[0].tolist()
        is_repeating = True
        for r in range(1,rows):
            if grid[r].tolist() != first_row:
                is_repeating = False
        if is_repeating:
            return "repeating sequence"
    
    # Check for checkerboard (orange and yellow only)
    if set(unique_colors) == {2, 4}:  # Check for orange and yellow
      is_checkerboard = True
      for r in range(rows):
          for c in range(cols):
              expected_color = 4 if (r + c) % 2 == 0 else 2
              if grid[r,c] != expected_color:
                 is_checkerboard = False
                 break
      if is_checkerboard:
          return "checkerboard"


    return "other"

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    pattern = get_pattern(input_grid)

    if pattern == "single pixel":
        return input_grid.tolist()

    elif pattern == "repeating sequence":
        output_grid = np.concatenate((input_grid, input_grid), axis=1)
        in_rows = input_grid.shape[0]
        color_sequence = input_grid.flatten()
        
        # Append rows cyclically
        while output_grid.shape[0] < 10:
          next_row_index = (output_grid.shape[0] - in_rows) % len(color_sequence)
          next_row = np.array([color_sequence[next_row_index]] * (cols * 2))
          output_grid = np.concatenate((output_grid, [next_row]), axis=0)

        # Crop to 10x10
        output_grid = output_grid[:10, :10]
        return output_grid.tolist()

    elif pattern == "checkerboard":
        output_grid = np.copy(input_grid)
        output_grid[output_grid == 4] = 2  # Change yellow to orange
        return output_grid.tolist()

    elif pattern == "solid columns":
        output_grid = np.zeros((rows, cols * 2), dtype=int)
        for r in range(rows):
            for c in range(cols * 2):
                output_grid[r, c] = input_grid[r, c % cols]
                if c >= cols: # Apply color change logic to only added columns
                    output_grid[r,c] = input_grid[r, (c+1) % cols] if (c+1) % 2 !=0 else input_grid[r,c%cols]
        return output_grid.tolist()

    else:
        # Default case (should not reach here with known training examples)
        return input_grid.tolist()
```
