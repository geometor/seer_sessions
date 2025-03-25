"""
The input grid is transformed into a smaller, densely packed output grid.  Colored regions in the input are identified, their bounding boxes are determined, their colors are transformed according to a specific mapping, and then they are arranged as rectangles in the output grid, maintaining their relative spatial order. The output grid is condensed, removing any background space between the colored rectangles.
"""

import numpy as np

def get_objects(grid):
    """Find contiguous regions of non-zero pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    def dfs(r, c, color, obj_pixels):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj_pixels.append((r, c))
        dfs(r + 1, c, color, obj_pixels)
        dfs(r - 1, c, color, obj_pixels)
        dfs(r, c + 1, color, obj_pixels)
        dfs(r, c - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                objects.append(obj_pixels)
    return objects

def bounding_box(obj_pixels):
    """Calculate the bounding box of a set of pixels."""
    min_r = min(p[0] for p in obj_pixels)
    max_r = max(p[0] for p in obj_pixels)
    min_c = min(p[1] for p in obj_pixels)
    max_c = max(p[1] for p in obj_pixels)
    return min_r, min_c, max_r, max_c

def color_map(input_color):
    """Maps input colors to output colors."""
    mapping = {
        2: 1,
        5: 5,
        8: 1,
        9: 9,
        4: 9,
        7: 5,
        1: 1,
        6: 2,
        3: 3
    }
    return mapping.get(input_color, input_color) # Default to input color if not in map

def transform(input_grid):
    # Convert to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Colored Regions
    objects = get_objects(input_grid)

    # 2. & 3. Bounding Boxes and Color Mapping, and Sort.  Sort objects based on top-left corner
    # The objects returned are already in a raster scan order
    bbox_list = []
    for obj in objects:
        min_r, min_c, max_r, max_c = bounding_box(obj)
        input_color = input_grid[obj[0]]  # Get color from first pixel of object
        output_color = color_map(input_color)
        bbox_list.append((min_r, min_c, max_r - min_r + 1, max_c - min_c + 1, output_color))

    # 4. Condense and arrange
    # determine output grid size
    output_rows = 0
    output_cols = 0

    row_heights = []
    current_row_height = 0
    current_row_width = 0
    for min_r, min_c, height, width, _ in bbox_list:
      if current_row_width + width > 20:
        row_heights.append(current_row_height)
        output_cols = max(output_cols, current_row_width)
        current_row_width = width
        current_row_height = height
      else:
        current_row_width += width
        current_row_height = max(current_row_height, height)

    row_heights.append(current_row_height)
    output_cols = max(output_cols, current_row_width)
    output_rows = sum(row_heights)


    # 5. Output Grid Construction
    output_grid = np.zeros((output_rows, output_cols), dtype=int)
    current_row = 0
    current_col = 0
    row_index = 0

    for min_r, min_c, height, width, output_color in bbox_list:
        if current_col + width > output_cols:
            current_row += row_heights[row_index]
            row_index +=1
            current_col = 0
        output_grid[current_row:current_row + height, current_col:current_col + width] = output_color
        current_col += width

    return output_grid.tolist()