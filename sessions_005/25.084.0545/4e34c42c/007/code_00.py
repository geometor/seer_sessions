"""
Identifies the bounding box of non-background pixels in the input grid and constructs a 5-row output grid. The top and bottom rows are created by extracting non-background pixels from the top and bottom rows of the bounding box, respectively.  The three middle rows are constructed by extracting all rows with non-background pixels. The selected rows are padded as required.
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

def get_row_within_bbox(grid, row_index, min_col, max_col, background_colors):
    """Extracts non-background pixels from a specified row within the bounding box."""

    row_pixels = []
    for col in range(min_col, max_col + 1):
        if grid[row_index, col] not in background_colors:
            row_pixels.append(grid[row_index, col])
    return row_pixels

def get_top_bottom_row(grid, min_row, max_row, min_col, max_col, background_colors):
    """Gets the top or bottom row based on non-background pixels."""

    # Find the first row with a non-background pixel within the bounding box.
    
    first_row = -1
    for r in range(min_row, max_row+1):
        for c in range(min_col, max_col + 1):
            if grid[r,c] not in background_colors:
                first_row = r
                break  # move to the next column
        if first_row >= 0:
            break
    
    last_row = -1
    for r in range(max_row, min_row-1, -1):
       for c in range(min_col, max_col + 1):
            if grid[r,c] not in background_colors:
                last_row = r
                break
       if last_row >= 0:
           break
    
    if first_row == -1:
        return [], [] # No non-background pixels

    top_row = get_row_within_bbox(grid, first_row, min_col, max_col, background_colors)
    bottom_row = get_row_within_bbox(grid, last_row, min_col, max_col, background_colors)
    return top_row, bottom_row


def pad_row(row, target_width, background_color):
    """Pads a row with the background color to reach the target width."""
    if not row:
      return [background_color] * target_width
    
    padding_needed = target_width - len(row)
    if padding_needed <= 0:
        return row[:target_width]  # Truncate if longer

    left_padding = padding_needed // 2
    right_padding = padding_needed - left_padding
    return [background_color] * left_padding + row + [background_color] * right_padding

def get_middle_rows(grid, min_row, max_row, min_col, max_col, background_colors, target_width):
    middle_rows_data = []
    for r in range(min_row, max_row + 1):
        row_pixels = []
        has_non_background = False
        for c in range(0, grid.shape[1]): # Iterate through the *entire* row
            pixel = grid[r, c]
            if pixel not in background_colors:
                has_non_background = True
                row_pixels.append(pixel)
            elif has_non_background: # and pixel in background_colors
                row_pixels.append(pixel) # include background after non-background

        if has_non_background:
              middle_rows_data.append(row_pixels)

    # ensure exactly 3 middle rows
    while len(middle_rows_data) < 3:
      if middle_rows_data:
        middle_rows_data.append(middle_rows_data[-1]) # Duplicate last if not enough
      else:
        middle_rows_data.append([background_colors[0]] * target_width)  # fill with background
    
    if len(middle_rows_data) > 3:
      middle_rows_data = middle_rows_data[:3]  # Truncate if there are more than 3
    
    padded_middle_rows = []
    for row in middle_rows_data:
      padded_middle_rows.append(pad_row(row, target_width, background_colors[0]))

    return padded_middle_rows



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

    # Get the top and bottom rows based on non-background pixels within the bounding box
    top_row, bottom_row = get_top_bottom_row(input_grid, min_row, max_row, min_col, max_col, background_colors)

    # Find max width - use max of top/bottom and full grid scan
    max_width_top_bottom = max(len(top_row), len(bottom_row))

     # Create the output grid
    output_grid = np.full((5, max_width_top_bottom), background_colors[0],  dtype=int)

    # Get Middle Rows
    middle_rows = get_middle_rows(input_grid, min_row, max_row, min_col, max_col, background_colors, max_width_top_bottom)

    output_grid_list = [pad_row(top_row, max_width_top_bottom, background_colors[0])] + middle_rows + [pad_row(bottom_row, max_width_top_bottom, background_colors[0])]

    output_grid = np.array(output_grid_list)
    
    return output_grid.tolist()