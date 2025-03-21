# b527c5c6 • 008 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Rectangles:** Locate all green (3) rectangles within the input grid.
2.  **Locate Red Pixels:** Within each identified green rectangle, find the single red (2) pixel.
3.  **Horizontal Rectangle Transformation**: For the upper horizontal green rectangle copy its red pixel to all of the empty space of the rectangle to the left, keeping its original position, and copy it to the bottom part from end to end of the rectangle..
4.  **Vertical Rectangle Transformation**: For the vertical green rectangle copy its red pixel. The copy is created above the input red pixel, keeping its original position.
"""

import numpy as np

def find_rectangles(grid, color):
    rectangles = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Found a potential start of a rectangle, try to expand
                width = 0
                while c + width < cols and grid[r, c + width] == color and not visited[r, c + width]:
                    width += 1
                height = 0
                while r + height < rows and all(grid[r + height, c + i] == color for i in range(width)) and not any(visited[r + height, c + i] for i in range(width)):
                    height += 1

                # Check to make sure no more matching color:
                good = True
                if r+height < rows:
                    for i in range(width):
                        if grid[r+height,c+i] == color:
                            good = False
                            break
                if c + width < cols:
                    for i in range(height):
                        if grid[r+i,c+width] == color:
                            good = False
                            break

                if good:
                    # Mark as visited
                    for i in range(height):
                        for j in range(width):
                            visited[r + i, c + j] = True
                    rectangles.append((r, c, width, height))
    return rectangles

def find_red_pixel(grid, rectangle, red_color=2):
    r, c, width, height = rectangle
    for i in range(height):
        for j in range(width):
            if grid[r + i, c + j] == red_color:
                return r + i, c + j
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    green_rectangles = find_rectangles(input_grid, 3)

    for rect in green_rectangles:
        red_pixel_pos = find_red_pixel(input_grid, rect)
        if red_pixel_pos:
            red_row, red_col = red_pixel_pos
            r, c, width, height = rect

            # Horizontal Rectangle (top)
            if r < input_grid.shape[0] / 2:
                #copy to the left
                for i in range(c,red_col):
                    output_grid[red_row,i] = 2

                # copy to lower section:
                new_row = r + height -1

                while new_row < input_grid.shape[0] and not np.any(input_grid[new_row,:]==1):
                    for i in range(width):
                      output_grid[new_row,r+c+i]=2
                    if np.any(find_rectangles(output_grid,3)):
                         break;
                    new_row +=1

            # Vertical Rectangle. (bottom)
            else:
                output_grid[red_row - 1, red_col] = 2

    return output_grid
```
