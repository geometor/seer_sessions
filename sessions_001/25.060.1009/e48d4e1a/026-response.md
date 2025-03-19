# e48d4e1a • 026 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find green lines. Also, find a single gray pixel.
2.  **Delete Object:** Delete the single gray pixel, if present.
3.  **Shift Green Pixel:** If there is a green pixel that's part of a horizontal line and a vertical line, shift that specific green pixel one position to the left.
4.   **Output:** Produce the transformed grid.
"""

import numpy as np

def find_green_lines(grid):
    rows, cols = grid.shape
    green_lines = []
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 3:
                green_lines.append((r,c))
    return green_lines

def find_gray_pixel(grid):
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == 5:
                return (r, c)
    return None

def is_part_of_horizontal_line(grid, r, c):
    if grid[r,c] != 3:
        return False
    rows, cols = grid.shape
    count = 0
    if c > 0 and grid[r, c-1] == 3:
        count += 1
    if c < cols - 1 and grid[r, c+1] == 3:
        count += 1
    return count > 0

def is_part_of_vertical_line(grid, r, c):
    if grid[r,c] != 3:
        return False
    rows, cols = grid.shape
    count = 0
    if r > 0 and grid[r-1, c] == 3:
        count += 1
    if r < rows - 1 and grid[r+1, c] == 3:
        count += 1
    return count > 0
    

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    
    # Delete grey pixel
    gray_pixel = find_gray_pixel(output_grid)
    if gray_pixel:
        output_grid[gray_pixel] = 0

    # Find green lines
    green_lines = find_green_lines(input_grid)

    # Shift Green Pixel
    for r, c in green_lines:
        if is_part_of_horizontal_line(output_grid,r,c) and is_part_of_vertical_line(output_grid, r,c):
            output_grid[r, c] = 0
            if c > 0:
                output_grid[r, c - 1] = 3
            
    return output_grid
```
