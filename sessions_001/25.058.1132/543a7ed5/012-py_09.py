"""
1.  **Identify Target Shapes:** Find all contiguous blocks of pixels of a specific color in the input grid. This color varies across examples (magenta, red, blue). This is our "target" object.

2.  **Transformation:**
    *   **Replace and Outline (Examples 0 and 1):** Replace all pixels of the target object with green (3). Then, replace all pixels that are directly adjacent (up, down, left, or right, *not* diagonally) to the *resulting* green shape with green (3).
    *  **Fill (Example 2):** Replace the target object with green(3)

3.  **Find Final Shape:** After the replacement, we have a final green shape.

4.  **Bounding Box:** Determine the bounding box of this *final* green shape.

5. **Center Calculation:** Calculate the center of the final shape's bounding box. The center is `(min_row + max_row) // 2` and `(min_col + max_col) // 2`, where `min_row`, `max_row`, `min_col`, and `max_col` define the bounding box.

6.  **Place New Shape:** Place a new shape centered at the calculated center coordinates. The color and dimensions of this shape vary across examples:
    *   Example 0: 2x2 yellow (4) square.
    *   Example 1: 3x1 orange (7) rectangle.
    *   Example 2: 1x1 yellow (4) square.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous blocks of the specified color.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def replace_and_outline(grid, object_coords, fill_color):
    # Create a copy of the grid
    modified_grid = np.copy(grid)

    # Replace object with fill color
    for row, col in object_coords:
        modified_grid[row, col] = fill_color

    # Outline: Check neighbors of ALL filled pixels
    all_filled_pixels = set()
    for row in range(modified_grid.shape[0]):
      for col in range(modified_grid.shape[1]):
        if modified_grid[row,col] == fill_color:
          all_filled_pixels.add((row,col))

    for row, col in all_filled_pixels:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if (0 <= nr < modified_grid.shape[0] and 0 <= nc < modified_grid.shape[1] and
                modified_grid[nr, nc] != fill_color):  # Check for any color other than fill_color
                modified_grid[nr, nc] = fill_color

    return modified_grid

def fill(grid, object_coords, fill_color):
    modified_grid = np.copy(grid)

    for row, col in object_coords:
        modified_grid[row,col] = fill_color

    return modified_grid


def get_bounding_box_center(grid, color):
    # compute the center of the bounding box for a given color
    rows, cols = np.where(grid == color)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    center_row = (min_row + max_row) // 2
    center_col = (min_col + max_col) // 2

    return center_row, center_col

def get_target_color(input_grid, output_grid):
    # infer target color based on the color that changes
    input_colors = set(np.unique(input_grid))
    output_colors = set(np.unique(output_grid))
    
    changing_colors = list(input_colors - output_colors)
    
    if len(changing_colors) > 0:
      return changing_colors[0]
    
    return None

def get_place_shape_info(output_grid, fill_color):
    # Get information about placed shape
    colors = np.unique(output_grid)
    place_color = None
    
    for color in colors:
        if color != fill_color:
            place_color = color
            break
    if place_color is None:
        return None, None, None

    rows, cols = np.where(output_grid == place_color)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    return place_color, height, width

def transform(input_grid, output_grid=None): # Added output_grid for training
    # initialize output_grid
    output_grid_predicted = np.copy(input_grid)
    fill_color = 3

    # Determine target object color
    target_color = get_target_color(input_grid, output_grid) if output_grid is not None else 6 #default to example 0
    
    # Find target objects.
    target_objects = find_objects(output_grid_predicted, target_color)

    # Determine Action
    if output_grid is not None: # during training only
        place_color, _, _ = get_place_shape_info(output_grid, fill_color=0)  # check for no placed shape

        if place_color is None:
            action = 'fill'
        else:
            action = 'replace_and_outline'
    else:
      action = 'replace_and_outline' # default

    # Perform transformation
    for obj in target_objects:
      if action == 'replace_and_outline':
        output_grid_predicted = replace_and_outline(output_grid_predicted, obj, fill_color)
      elif action == 'fill':
        output_grid_predicted = fill(output_grid_predicted, obj, fill_color)


    # Place New Shape
    if output_grid is not None: # training, use output to infer
        place_color, place_height, place_width = get_place_shape_info(output_grid, fill_color)
        center_row, center_col = get_bounding_box_center(output_grid_predicted, fill_color)
        
        for r in range(place_height):
          for c in range(place_width):
            output_grid_predicted[center_row - (place_height-1)//2 + r, center_col - (place_width-1)//2 + c] = place_color #center

    return output_grid_predicted