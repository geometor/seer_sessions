# ecdecbb3 • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify:** Locate the two vertical azure (8) lines and the single red (2) pixel in the input grid.
2.  **Expand:** Horizontally expand the red pixel to the left and right until it is adjacent to the azure vertical lines.
3. **Fill**: In the row of the expanded red region, fill the cells that are directly adjacent on the left and right of the expanded region, with azure(8).
4.  **Preserve:** Keep the original azure lines unchanged. All other white pixels remain white.
"""

import numpy as np

def find_vertical_lines(grid, color):
    lines = []
    for col in range(grid.shape[1]):
        if all(grid[:, col] == color):
            lines.append(col)
    return lines

def find_pixel(grid, color):
    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color:
                return row, col
    return None

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    
    # find azure lines
    azure_lines = find_vertical_lines(input_grid, 8)

    # find the red pixel
    red_pixel_pos = find_pixel(input_grid, 2)

    if red_pixel_pos and len(azure_lines) == 2:
        red_row, red_col = red_pixel_pos

        # Expand red pixel horizontally
        left_expansion = red_col - 1
        while left_expansion >= 0 and input_grid[red_row, left_expansion] != 8:
            output_grid[red_row, left_expansion] = 2
            left_expansion -= 1
        
        right_expansion = red_col + 1
        while right_expansion < input_grid.shape[1] and input_grid[red_row, right_expansion] != 8:
            output_grid[red_row, right_expansion] = 2
            right_expansion += 1
            
        # fill azure beside expanded region
        
        left_fill = left_expansion
        if left_fill>=0:
            if input_grid[red_row, left_fill] == 8:
              output_grid[red_row, left_fill+1] = 8

        right_fill = right_expansion
        if right_fill < input_grid.shape[1]:
          if input_grid[red_row, right_fill] == 8:
            output_grid[red_row, right_fill-1] = 8

    return output_grid
```
