"""
1.  **Identify the Red Square:** Locate the red square object within the input grid.
2.  **Find Original Center and Color:** Determine the original center coordinates of the red square and the color of the pixel at that center.
3.  **Move the Red Square:** Move the entire red square upwards until the top of the square hits the top edge of the grid.
4.  **Preserve Center Color:** At the new center location of the moved red square, set the pixel's color to the *original* color of the center pixel (from step 2).  All other pixels of the red square will be red.
5. **Output**: Return the modified grid.
"""

import numpy as np

def find_object(grid, color, shape_type=None):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)


    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                if shape_type == "rectangle":
                    rows, cols = zip(*current_object)
                    min_row, max_row = min(rows), max(rows)
                    min_col, max_col = min(cols), max(cols)
                    if len(current_object) == (max_row - min_row + 1) * (max_col-min_col + 1):
                      objects.append(current_object)

                else:
                  objects.append(current_object)

    return objects

def move_object(grid, object_coords, dr, dc):
    new_object_coords = []
    for r, c in object_coords:
        new_object_coords.append((r + dr, c + dc))
    return new_object_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the red square.
    red_squares = find_object(input_grid, 2, "rectangle")
    red_square = None
    for square in red_squares:
        #check if it is really a square/rectangle
        rows, cols = zip(*square)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        if (max_row - min_row + 1) * (max_col - min_col + 1) == len(square):
            red_square = square
            break

    # Move the red square up by two rows, and preserve center color.
    if red_square:
       # Find original center and color
       rows, cols = zip(*red_square)
       min_row, max_row = min(rows), max(rows)
       min_col, max_col = min(cols), max(cols)
       center_row = (min_row + max_row) // 2
       center_col = (min_col + max_col) // 2
       original_center_color = input_grid[center_row, center_col]

       #move up to the top
       move_up_by = min_row #how many to move
       new_red_square = move_object(input_grid, red_square, -move_up_by, 0)

       #clear previous position from output
       for r,c in red_square:
          output_grid[r,c] = 0


       #apply to the new position
       for r, c in new_red_square:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
            output_grid[r, c] = 2 #set as red

       # Preserve the original center color
       new_center_row = center_row - move_up_by
       if 0 <= new_center_row < output_grid.shape[0] and 0 <= center_col < output_grid.shape[1]:
            output_grid[new_center_row, center_col] = original_center_color


    return output_grid