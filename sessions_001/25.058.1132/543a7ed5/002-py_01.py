"""
1.  **Identify Magenta Rectangles:** Locate all rectangular shapes formed by contiguous magenta (6) pixels. These can be either outlines or filled rectangles.

2.  **Outline Modification - color change:** all magenta(6) pixels that are part of rectangles, that do *not* fully enclose azure(8) pixels, become green(3)

3.  **Fill Interior (Conditional):** If a magenta rectangle completely encloses one or more azure(8) pixels, replace azure(8) pixels in its center, with a yellow (4) square. *Center* means the inner object maintains the same rows/cols between all four sides of the outer rectangle.

4. **Background Modification - color change:** all azure(8) pixels adjacent to green(3) and/or yellow(4) pixels, becomes green(3).

5. **No change to azure background**: any azure(8) pixels not adjacent to other colors remain unchanged.
"""

import numpy as np

def find_objects(grid, color):
    objects = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def is_rectangle(obj):
    rows, cols = zip(*obj)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return len(obj) == (max_row - min_row + 1) * (max_col - min_col + 1)

def get_rectangle_bounds(obj):
    rows, cols = zip(*obj)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, max_row, min_col, max_col

def encloses_color(grid, obj, color):
    min_row, max_row, min_col, max_col = get_rectangle_bounds(obj)
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if grid[r,c] == color:
                return True
    return False

def get_center_square(obj):
    min_row, max_row, min_col, max_col = get_rectangle_bounds(obj)
    
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    if height < 3 or width < 3:
        return []  # No center if smaller than 3x3
    
    center_min_row = min_row + 1
    center_max_row = max_row - 1
    center_min_col = min_col + 1
    center_max_col = max_col - 1
    

    # Adjust to the center if there's even size (keep equal size from borders)
    while (center_max_row - center_min_row) > 1:
       center_min_row +=1
       center_max_row -=1
       
    while (center_max_col - center_min_col) > 1:
       center_min_col +=1
       center_max_col -=1

    center_square = []
    for r in range(center_min_row, center_max_row + 1):
        for c in range(center_min_col, center_max_col + 1):
            center_square.append((r, c))
    return center_square

def is_adjacent(grid, r, c, colors):
    for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1] and grid[nr, nc] in colors:
            return True
    return False
    

def transform(input_grid):
    output_grid = np.copy(input_grid)
    magenta_objects = find_objects(input_grid, 6)
    rectangles = [obj for obj in magenta_objects if is_rectangle(obj)]
    
    for rect in rectangles:
        #Outline Modification
        if not encloses_color(input_grid, rect, 8):
             for r, c in rect:
                output_grid[r, c] = 3
        #Fill Interior
        if encloses_color(input_grid,rect, 8):
            center_square = get_center_square(rect)
            for r, c in center_square:
                output_grid[r,c] = 4

    #Background Modification
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r,c] == 8:
                if is_adjacent(output_grid, r, c, [3, 4]):
                  output_grid[r,c] = 3

    return output_grid