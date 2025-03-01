"""
The transformation identifies all magenta (6) rectangles in the input grid. The largest magenta rectangle is identified.  The *other* magenta rectangles are then copied to the output grid, but their position is determined by treating the *largest* rectangle's position in the input grid as the origin (0,0) in the output grid.

"""

import numpy as np

def find_magenta_rectangles(grid):
    """Finds all rectangular blocks of magenta (6) pixels."""
    magenta_rectangles = []
    rows, cols = len(grid), len(grid[0])
    visited = set()

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_rectangle):
        if (r, c) in visited or not is_valid(r, c) or grid[r][c] != 6:
            return

        visited.add((r, c))
        current_rectangle.append((r, c))

        # Explore adjacent cells
        dfs(r + 1, c, current_rectangle)
        dfs(r - 1, c, current_rectangle)
        dfs(r, c + 1, current_rectangle)
        dfs(r, c - 1, current_rectangle)


    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 6 and (r, c) not in visited:
                current_rectangle = []
                dfs(r, c, current_rectangle)

                # Check if the found region is a rectangle
                if current_rectangle:
                    min_row = min(p[0] for p in current_rectangle)
                    max_row = max(p[0] for p in current_rectangle)
                    min_col = min(p[1] for p in current_rectangle)
                    max_col = max(p[1] for p in current_rectangle)

                    # Verify rectangle property:
                    is_rectangle = True
                    for row in range(min_row, max_row + 1):
                        for col in range(min_col, max_col + 1):
                            if (row, col) not in current_rectangle:
                                is_rectangle = False
                                break
                        if not is_rectangle:
                            break
                    
                    if is_rectangle:
                      magenta_rectangles.append({
                          "row_start": min_row,
                          "row_end": max_row,
                          "col_start": min_col,
                          "col_end": max_col,
                          "height": max_row - min_row + 1,
                          "width": max_col - min_col + 1
                      })
    return magenta_rectangles

def find_largest_rectangle(rectangles):
    """Finds the largest rectangle in a list of rectangles."""
    largest_rectangle = None
    max_area = 0
    for rect in rectangles:
        area = rect["height"] * rect["width"]
        if area > max_area:
            max_area = area
            largest_rectangle = rect
    return largest_rectangle

def transform(input_grid):
    """Transforms the input grid by copying all magenta rectangles, repositioning based on largest."""
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find all magenta rectangles
    magenta_rectangles = find_magenta_rectangles(input_grid)
    
    # Find largest magenta rectangle
    largest_rectangle = find_largest_rectangle(magenta_rectangles)

    # Reposition and copy other rectangles
    for rect in magenta_rectangles:
        if rect is not largest_rectangle:
            # Calculate relative offset
            row_offset = rect["row_start"] - largest_rectangle["row_start"]
            col_offset = rect["col_start"] - largest_rectangle["col_start"]

            # Copy with offset
            for r in range(rect["height"]):
                for c in range(rect["width"]):
                    output_row = row_offset + r
                    output_col = col_offset + c
                    if 0 <= output_row < output_grid.shape[0] and 0 <= output_col < output_grid.shape[1]:
                      output_grid[output_row][output_col] = 6
    
    return output_grid