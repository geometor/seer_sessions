```python
"""
Transforms the input grid by identifying objects, determining a new background color,
and rearranging the objects within a new grid size based on the original positioning
of objects of color 3, while preserving the relative sizes and positions of other colored objects.
"""

import numpy as np

def get_objects(grid):
    """Find contiguous blocks of the same color."""
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    def dfs(row, col, color, obj):
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
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                if obj: # avoid empty objects
                   objects.append((grid[row, col], obj))
    return objects

def get_bounding_box(obj):
    """Calculates the bounding box for set of pixels"""
    min_row = min(p[0] for p in obj)
    min_col = min(p[1] for p in obj)
    max_row = max(p[0] for p in obj)
    max_col = max(p[1] for p in obj)
    return min_row, min_col, max_row, max_col

def get_output_size(input_grid):
    """Determine output grid size based on longest runs of color 3 and object sizes"""
    grid = np.array(input_grid)
    objects = get_objects(grid)

    # Find longest vertical and horizontal runs of 3s if they exists
    max_vertical = 0
    max_horizontal = 0

    for color, obj_pixels in objects:
       if color == 3:
           min_row, min_col, max_row, max_col = get_bounding_box(obj_pixels)
           max_vertical = max(max_vertical, max_row - min_row + 1)
           max_horizontal = max(max_horizontal, max_col - min_col+1)
           

    # Add extra space for other objects.  This is a heuristic and might need adjustment.
    extra_height = 0
    extra_width = 0
    for color, obj_pixels in objects:
        if color != 3:  # Don't double-count the 3s
            min_row, min_col, max_row, max_col = get_bounding_box(obj_pixels)
            extra_height = max(extra_height, max_row - min_row + 1)
            extra_width = max(extra_width, max_col-min_col + 1)

    if max_vertical == 0: # color 3 not found, return the input size
        height = input_grid.shape[0]
        width = input_grid.shape[1]

    else: # example 2 case
        #find the biggest object by color
        color_sizes = {}
        for color, obj_pixels in objects:
            if color !=3:
                min_row, min_col, max_row, max_col = get_bounding_box(obj_pixels)
                height = max_row - min_row + 1
                width = max_col - min_col + 1
                if color not in color_sizes:
                    color_sizes[color] = (height, width)
                else:
                    color_sizes[color] = (max(color_sizes[color][0],height),max(color_sizes[color][1], width) )

        height = max_vertical
        width = max_horizontal

        for color in color_sizes:
           height = max(color_sizes[color][0] + max_vertical , height)
           width = max(color_sizes[color][1] + max_horizontal , width )
        height += extra_height + 2
        width += extra_width + 2

    return height, width


def transform(input_grid):
    input_grid = np.array(input_grid)
    objects = get_objects(input_grid)

    # Determine output size and background
    output_height, output_width = get_output_size(input_grid)

    # Determine background color and removed colors.
    background_color = 2  # Default to 2
    removed_colors = {0, 7}
    if any(c == 3 for c, _ in objects):
        background_color = 3
        removed_colors = {0, 8}

    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    # Place objects, preserving relative positions and sizes.
    for color, obj_pixels in objects:
        if color not in removed_colors:
            min_row, min_col, max_row, max_col = get_bounding_box(obj_pixels)
            obj_height = max_row - min_row + 1
            obj_width = max_col - min_col + 1

            if background_color == 3: # use color 3 objects as base
                # find the object 3 with largest area
                color3_max_area = 0
                color3_top_left = (0,0)

                for color2, obj_pixels2 in objects:
                    if color2 == 3:
                        min_row2, min_col2, max_row2, max_col2 = get_bounding_box(obj_pixels2)
                        area = (max_row2-min_row2) * (max_col2-min_col2)
                        if area > color3_max_area:
                            color3_max_area = area
                            color3_top_left = (min_row2, min_col2)

                # place relative to color 3 top left
                new_row = min_row - color3_top_left[0]
                new_col = min_col - color3_top_left[1]

                # make sure it does not overflow
                new_row = min(new_row, output_height-obj_height)
                new_col = min(new_col, output_width - obj_width)


                for r in range(obj_height):
                    for c in range(obj_width):
                        if 0 <= new_row + r < output_height and 0 <= new_col + c < output_width:
                            output_grid[new_row + r, new_col + c] = color

            else:  # Example 1 logic (background is 2)
                #find the biggest object with color 2
                color2_max_area = 0
                color2_top_left = (0,0)

                for color2, obj_pixels2 in objects:
                    if color2 == 2:
                        min_row2, min_col2, max_row2, max_col2 = get_bounding_box(obj_pixels2)
                        area = (max_row2-min_row2) * (max_col2-min_col2)
                        if area>color2_max_area:
                            color2_max_area = area
                            color2_top_left = (min_row2,min_col2)

                # place relative to color 2 objects
                new_row = min_row - color2_top_left[0]
                new_col = min_col - color2_top_left[1]
                for r in range(obj_height):
                    for c in range(obj_width):
                            if 0 <= new_row + r < output_height and 0 <= new_col + c < output_width:
                                output_grid[new_row + r, new_col + c] = color

    return output_grid.tolist()
```