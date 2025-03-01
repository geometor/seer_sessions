"""
1.  **Identify the Yellow Object:** Find the contiguous yellow (4) object within the input grid. If no yellow object exists, terminate.

2.  **Insert Colors Inside Yellow Object:**
    *   Locate the second row from the bottom of the yellow object. Insert a blue (1) pixel in this row, maintaining the original column.
    *   Locate the third row from the top of the yellow object. Insert a green (3) pixel in this row, maintaining the original column.

3.  **Add Colors Adjacent to Yellow Object:**
      * Find the top row and rightmost column of the yellow shape. Add a blue pixel directly above the yellow shape at this position.
    *   Find top row of the leftmost column of the yellow shape.  Add a green(3) pixel directly above this.
    *   Find the bottom row of the leftmost column of the yellow shape.  Add a green(3) pixel directly below.

4.  **Add "L" shape:** Add an "L"-shaped object consisting of green(3) and yellow(4) pixels to the bottom left of the image. The "L" should consist of two rows, the yellow pixels should be adjacent, and the green should be adjacent.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects of the same color in a grid.
    Returns a dictionary where keys are colors and values are lists of object coordinates.
    Each object is represented as a dictionary with 'coords' and other properties.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []
        visited.add((row, col))
        coords = [(row, col)]
        coords.extend(dfs(row + 1, col, color))
        coords.extend(dfs(row - 1, col, color))
        coords.extend(dfs(row, col + 1, color))
        coords.extend(dfs(row, col - 1, color))
        return coords

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                coords = dfs(row, col, color)
                if color not in objects:
                    objects[color] = []

                # Store as a dictionary with properties
                obj_dict = {
                    'coords': coords,
                    'top_left': (min(r for r, c in coords), min(c for r, c in coords)),
                    'bottom_right': (max(r for r, c in coords), max(c for r, c in coords))
                }
                objects[color].append(obj_dict)

    return objects

def transform(input_grid):
    # initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # Find objects
    objects = find_objects(input_grid)

    # Locate yellow shape
    yellow_shapes = objects.get(4, [])
    if yellow_shapes:
        #In this case, we don't want to assume there will be more than one yellow shape
        yellow_shape = yellow_shapes[0]
        yellow_coords = yellow_shape['coords']

        # Insert blue (1) inside, second row from bottom.
        yellow_bottom_row = max(row for row, col in yellow_coords)
        second_bottom_yellow = [(r,c) for r, c in yellow_coords if r == yellow_bottom_row - 1]
        #Handle edge case where yellow shape only has one row.
        if second_bottom_yellow:
          blue_insert_col = second_bottom_yellow[0][1]
          output_grid[yellow_bottom_row - 1, blue_insert_col] = 1
        else: #If there is only 1 row, insert blue in the first row.
           blue_insert_col = yellow_coords[0][1]
           output_grid[yellow_bottom_row, blue_insert_col] = 1

        # Insert green (3) inside, third row from top
        yellow_top_row = min(row for row, col in yellow_coords)
        third_top_yellow = [(r, c) for r, c in yellow_coords if r == yellow_top_row + 2]
        #Handle edge case where yellow shape has less than 3 rows.
        if third_top_yellow:
            green_insert_col = third_top_yellow[0][1]
            output_grid[yellow_top_row + 2, green_insert_col] = 3
        else: #If not three rows, insert on existing row.
          green_insert_col = yellow_coords[0][1]
          output_grid[yellow_top_row, green_insert_col] = 3

        # Add blue (1) above rightmost column
        yellow_rightmost_col = max(col for row, col in yellow_coords)
        top_right_yellow = min([(r,c) for r, c in yellow_coords if c == yellow_rightmost_col], key=lambda x: x[0])
        #Handle case where the yellow is on the top edge
        if top_right_yellow[0] > 0:
            output_grid[top_right_yellow[0]-1, top_right_yellow[1]] = 1

        # Add green (3) above and below leftmost column
        yellow_leftmost_col = min(col for row, col in yellow_coords)
        top_left_yellow = min([(r,c) for r, c in yellow_coords if c == yellow_leftmost_col], key=lambda x: x[0])
        bottom_left_yellow = max([(r,c) for r,c in yellow_coords if c == yellow_leftmost_col], key=lambda x: x[0])
        #Handle case where yellow shape is at the top or bottom
        if top_left_yellow[0] > 0:
            output_grid[top_left_yellow[0]-1, top_left_yellow[1]] = 3
        if bottom_left_yellow[0] < output_grid.shape[0]-1:
            output_grid[bottom_left_yellow[0]+1, bottom_left_yellow[1]] = 3

    # Add "L" shape at bottom left, two rows.
    rows, cols = output_grid.shape
    #Find a spot that is empty
    start_row = rows - 2
    start_col = 0
    while output_grid[start_row, start_col]!= 0:
        start_col = start_col + 1
    output_grid[start_row, start_col] = 3
    output_grid[start_row, start_col+1] = 4
    output_grid[start_row, start_col+2] = 3
    output_grid[start_row, start_col+3] = 3
    output_grid[start_row+1, start_col] = 3
    output_grid[start_row+1, start_col+1] = 4
    output_grid[start_row+1, start_col+2] = 3
    output_grid[start_row+1, start_col+3] = 3

    return output_grid