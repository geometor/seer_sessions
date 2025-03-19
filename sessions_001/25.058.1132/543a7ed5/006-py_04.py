"""
1.  **Identify Magenta Rectangles:** Find all rectangular shapes composed of contiguous magenta (6) pixels.

2.  **Check for Enclosed Azure:** For each magenta rectangle, determine if it *completely* encloses one or more azure (8) pixels.  A pixel is considered "enclosed" if it is inside the rectangle and *not* part of the rectangle's border.

3.  **Conditional Outline Modification:**
    *   If a magenta rectangle *does not* completely enclose any azure (8) pixels, change *all* its magenta (6) pixels to green (3).
    *   If a magenta rectangle *does* enclose azure pixels and those azure are not part of the border, proceed to step 4.

4.  **Conditional Center Filling:** If a magenta rectangle completely encloses azure (8) pixels (and the enclosed pixels are not part of the border), replace the largest possible square of those "inner" azure pixels with yellow (4). The yellow square should be as large as possible while maintaining equal distance to all edges. If all azure pixels are part of the magenta border, this step is skipped.

5.  **Adjacent Color Change:** Any azure (8) pixel that is directly adjacent (horizontally or vertically, *not* diagonally) to a green (3) or yellow (4) pixel is changed to green (3).

6. **Preserve Unchanged:** Pixels that do not meet the above condition, remain unchanged.
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
    # Check only the inner pixels, not the border
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if grid[r,c] == color:
                return True
    return False

def get_center_square(obj, grid):
    min_row, max_row, min_col, max_col = get_rectangle_bounds(obj)
    
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    if height < 3 or width < 3:
        return []  # No center if smaller than 3x3

    # Define interior boundaries (excluding the border)
    center_min_row = min_row + 1
    center_max_row = max_row - 1
    center_min_col = min_col + 1
    center_max_col = max_col - 1
    

    # Shrink from all sides to find largest azure center.
    while (center_max_row > center_min_row and center_max_col > center_min_col):
          temp = grid[center_min_row:center_max_row+1, center_min_col:center_max_col+1]
          if not np.all(temp == 8):
             break
          else:
            center_min_row += 1
            center_max_row -= 1
            center_min_col += 1
            center_max_col -= 1

    center_square = []
    for r in range(center_min_row, center_max_row + 1):
        for c in range(center_min_col, center_max_col + 1):
                center_square.append((r,c))

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
                output_grid[r, c] = 3  # Change to green
        #Fill Interior
        elif encloses_color(input_grid,rect, 8):
            center_square = get_center_square(rect, input_grid)
            for r, c in center_square:
                output_grid[r,c] = 4

    #Background Modification
    for r in range(output_grid.shape[0]):
        for c in range(output_grid.shape[1]):
            if output_grid[r,c] == 8:
                if is_adjacent(output_grid, r, c, [3, 4]):
                  output_grid[r,c] = 3

    return output_grid