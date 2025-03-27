```python
"""
Identifies objects in the input grid, identifies relevant rows based on color changes, and constructs a new grid by combining and arranging these rows.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous objects in a grid.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def get_background_colors(grid, objects):
    """
    Get background color by finding largest objects
    """
    objects_by_size = sorted(objects, key=len, reverse=True)
    background_colors = []
    for obj in objects_by_size:
      if len(obj) > .10 * grid.size:
        background_colors.append(grid[obj[0][0], obj[0][1]])
    return background_colors


def get_object_bounding_box(objects):
    """Calculates the bounding box encompassing all given objects."""
    if not objects:
        return (0, 0, 0, 0)  # Empty case

    min_row = float('inf')
    max_row = float('-inf')
    min_col = float('inf')
    max_col = float('-inf')

    for obj in objects:
        for row, col in obj:
            min_row = min(min_row, row)
            max_row = max(max_row, row)
            min_col = min(min_col, col)
            max_col = max(max_col, col)

    return (min_row, max_row, min_col, max_col)

def transform(input_grid):
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find objects
    objects = find_objects(input_grid)

    # Find background
    background_colors = get_background_colors(input_grid, objects)

    # Identify non-background objects
    non_background_objects = [obj for obj in objects if input_grid[obj[0][0], obj[0][1]] not in background_colors]


    # Get bounding box of the non-background objects
    min_row, max_row, min_col, max_col = get_object_bounding_box(non_background_objects)
    
    # print(f"bounding box min/max: {min_row, max_row, min_col, max_col}")

    # 1. First/Last Row: Topmost line of combined shape
    first_row = []
    for c in range(min_col, max_col + 1):
        for r in range(min_row, max_row+1):
            if (input_grid[r,c] not in background_colors):
                first_row.append(input_grid[r,c])
                break  # move to the next column
        else: # no break, meaning all background
           first_row.append(background_colors[0]) # Pick the first by default

    # 2. Middle Rows: Rows with significant color changes within the bounding box
    middle_rows = []

    for r in range(min_row, max_row + 1):
        row_colors = []
        has_non_background = False

        for c in range(min_col, max_col + 1):
            
            pixel = input_grid[r,c]
            # print(f'{pixel=}')
            if pixel not in background_colors:
                has_non_background = True
                row_colors.append(pixel)
            elif has_non_background:
               row_colors.append(background_colors[0])  # default background
        if has_non_background:
            middle_rows.append(row_colors)

    # ensure exactly 3 middle rows
    while len(middle_rows) < 3:
      if middle_rows:
        middle_rows.append(middle_rows[-1]) # Duplicate last if not enough
      else:
        middle_rows.append([background_colors[0]] * len(first_row))  # fill with background


    if len(middle_rows) > 3:
      middle_rows = middle_rows[:3]  # Truncate if there are more than 3

    # 3. Last Row
    last_row = first_row

    # Combine all rows for output
    output_grid_list = [first_row] + middle_rows + [last_row]

    # Find max width
    max_width = max(len(row) for row in output_grid_list) if output_grid_list else 0

     # Create the output grid
    output_grid = np.full((len(output_grid_list), max_width), background_colors[0],  dtype=int)


    for row_idx, row_pixels in enumerate(output_grid_list):
        for col_idx, pixel in enumerate(row_pixels):
            # print(output_grid.shape, len(row_pixels))
            if col_idx < output_grid.shape[1]:  # Prevent out-of-bounds
                output_grid[row_idx, col_idx] = pixel

    return output_grid.tolist()
```