"""
The input grid is transformed into a smaller output grid by identifying contiguous colored regions, determining their bounding boxes, mapping their colors, sorting them by area (descending) and then top-left corner coordinates, and finally arranging them compactly in the output grid.
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
        1: 1,
        5: 5,
        7: 5,
        8: 8,
        9: 9,
        4: 9,
        3: 8  # Corrected mapping for 3
    }
    return mapping.get(input_color, input_color)

def transform(input_grid):
    # Convert to numpy array
    input_grid = np.array(input_grid)

    # 1. Identify Colored Regions
    objects = get_objects(input_grid)

    # 2. & 3. Bounding Boxes and Color Mapping, and Sort.
    bbox_list = []
    for obj in objects:
        min_r, min_c, max_r, max_c = bounding_box(obj)
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        area = len(obj)
        input_color = input_grid[obj[0]]  # Get color from first pixel of object
        output_color = color_map(input_color)
        bbox_list.append((min_r, min_c, height, width, output_color, area))

    # 4. Sort Objects by area (descending) then top-left corner
    bbox_list.sort(key=lambda x: (-x[5], x[0], x[1]))

    # 5. Arrange Objects in Output Grid
    output_grid = []
    current_row = []
    current_row_width = 0

    for min_r, min_c, height, width, output_color, _ in bbox_list:
        if current_row and current_row_width + width > 8: # Limiting to width of largest example
            output_grid.append(current_row)
            current_row = []
            current_row_width = 0

        if not current_row:
          row_height = height
        else:
          row_height = max(height, len(current_row))

        new_row = np.zeros((row_height, width), dtype=int)
        new_row[:] = output_color
        if not current_row:
            current_row = new_row
        else:
            # concatenate
            padding_rows = row_height - len(current_row)
            if padding_rows > 0:
              current_row = np.concatenate([current_row, np.zeros((padding_rows, current_row.shape[1]))], axis=0)

            padding_rows = row_height - len(new_row)
            if padding_rows > 0:
              new_row = np.concatenate([new_row, np.zeros((padding_rows, new_row.shape[1]))], axis=0)

            current_row = np.concatenate([current_row, new_row], axis=1)
        current_row_width += width

    if current_row.size: # any remaining
      output_grid.append(current_row)

    # stack rows to get the final result
    output_grid = np.vstack(output_grid).tolist()

    return output_grid