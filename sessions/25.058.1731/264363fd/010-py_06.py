"""
1.  **Identify Objects:** Find all red rectangles, a green cross shape, and green horizontal and vertical lines within the grid. Note the blue background, and single yellow pixels.

2.  **Remove**: Remove all blue background and single yellow pixels.

3.  **Shift Rectangles:** Shift all identified red rectangles to the leftmost possible position within their original rows, while maintaining their shape.

4.  **Alternate Line Colors:** For the rows that contained the green horizontal/vertical lines, starting with the first line, alternate the colors of the pixels between red and green, and fill any positions that contained an initial green value.

5.  **Output the modified grid**
"""

import numpy as np

def find_rectangles(grid, color):
    rectangles = []
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_rectangle):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_rectangle.append((r, c))
        dfs(r + 1, c, current_rectangle)
        dfs(r - 1, c, current_rectangle)
        dfs(r, c + 1, current_rectangle)
        dfs(r, c - 1, current_rectangle)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_rectangle = []
                dfs(r, c, current_rectangle)
                rectangles.append(current_rectangle)
    return rectangles

def shift_rectangle_left(grid, rectangle):
    min_col = min(c for r, c in rectangle)
    for r, c in rectangle:
        grid[r, c - min_col] = grid[r,c] #fill new spot
        if (c-min_col) != c:
            grid[r, c] = 1 #erase old by setting to background, to be removed
    return grid

def find_lines(grid, color):
    lines = []
    rows, cols = grid.shape
    for r in range(rows):
      row_line = []
      for c in range(cols):
        if grid[r,c] == color:
          row_line.append((r,c))
      if row_line:
        lines.append(row_line)

    for c in range(cols):
      col_line = []
      for r in range(rows):
        if grid[r,c] == color:
          col_line.append((r,c))
      if col_line:
        lines.append(col_line)
    return lines

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Remove blue background
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 1:
                output_grid[r, c] = 0

    # Find and remove single yellow pixels.
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 4:
                output_grid[r, c] = 0


    # Find red rectangles.
    red_rectangles = find_rectangles(output_grid, 2)

    # Shift rectangles left.
    for rectangle in red_rectangles:
        output_grid = shift_rectangle_left(output_grid, rectangle)
        
    #Find green lines
    green_lines = find_lines(input_grid, 3) #use input_grid to find original positions

    #Alternate colors in lines
    for line in green_lines:
        color_switch = 2 #start with red
        for r,c in line:
            output_grid[r,c] = color_switch
            color_switch = 5 - color_switch #switch between 2 and 3


    # Remove blue background again (created by shift)
    for r in range(rows):
        for c in range(cols):
            if output_grid[r,c] == 1:
                output_grid[r, c] = 0

    return output_grid