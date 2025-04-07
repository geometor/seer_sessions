import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify the background color (most frequent color) in the input grid.
2. Find all distinct connected objects (4-connectivity) of non-background colors.
3. Identify two key objects:
    a. The 'pattern' object: Contains the color azure (8). Extract the rectangular region defined by its bounding box; this is the 'pattern_tile'.
    b. The 'shape' object: The other object, which is monochromatic (single color, not azure). Extract the rectangular region defined by its bounding box ('shape_bbox_content'). The dimensions of this bounding box determine the tiling factors ('tile_rows', 'tile_cols').
4. Create an output grid with dimensions calculated by multiplying the shape object's bounding box dimensions (tile_rows, tile_cols) with the pattern_tile's dimensions (pattern_height, pattern_width). Initialize this grid with the background color.
5. Iterate through each cell (r_shape, c_shape) within the shape object's bounding box ('shape_bbox_content').
6. If the color at (r_shape, c_shape) in 'shape_bbox_content' is *not* the background color, place a copy of the 'pattern_tile' onto the output grid at the position starting at (r_shape * pattern_height, c_shape * pattern_width).
7. The final output grid consists of 'pattern_tile' copies placed according to the non-background pixels in the 'shape_bbox_content', with the remaining areas filled by the background color.
"""

def find_objects_pixels(grid):
    """
    Finds distinct connected objects in the grid, ignoring the background color.

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (list of object details, background_color)
               Each object detail is a dict: {'pixels': set, 'colors': set, 'bbox': tuple,
                                             'height': int, 'width': int, 'bbox_content': np.array}
               background_color (int): The identified background color.
    """
    rows, cols = grid.shape
    # Identify background color dynamically
    colors, counts = np.unique(grid, return_counts=True)
    if not colors.size: # Handle empty grid case
        return [], 0
    background_color = colors[np.argmax(counts)]

    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS if pixel is not background and not visited
            if grid[r, c] != background_color and not visited[r, c]:
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))

                    # Check 4-connected neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] != background_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_pixels:
                    # Calculate details for the found object
                    pixels_list = list(obj_pixels)
                    obj_colors = set(grid[r_pix, c_pix] for r_pix, c_pix in pixels_list)
                    rows_idx = [r_pix for r_pix, c_pix in pixels_list]
                    cols_idx = [c_pix for r_pix, c_pix in pixels_list]
                    min_r, max_r = min(rows_idx), max(rows_idx)
                    min_c, max_c = min(cols_idx), max(cols_idx)
                    bbox = (min_r, max_r, min_c, max_c)
                    height = max_r - min_r + 1
                    width = max_c - min_c + 1
                    bbox_content = grid[min_r:max_r + 1, min_c:max_c + 1]

                    objects.append({
                        'pixels': obj_pixels,
                        'colors': obj_colors,
                        'bbox': bbox,
                        'height': height,
                        'width': width,
                        'bbox_content': bbox_content
                    })

    return objects, background_color


def transform(input_grid_list):
    """
    Transforms the input grid based on identified pattern and shape objects,
    using the shape object's bounding box content to conditionally tile the pattern.

    Args:
        input_grid_list (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the output grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)

    # 1. Find objects and background color
    objects, background_color = find_objects_pixels(input_grid)

    # 2. Identify pattern and shape objects
    pattern_obj = None
    shape_obj = None
    for obj in objects:
        if 8 in obj['colors']:  # Azure (8) identifies the pattern object
            pattern_obj = obj
        elif len(obj['colors']) == 1 and 8 not in obj['colors']: # Monochromatic, not azure
            shape_obj = obj

    # Add a fallback check in case the primary identification fails but exactly two objects exist
    if (pattern_obj is None or shape_obj is None) and len(objects) == 2:
         obj1, obj2 = objects
         is_obj1_pattern = 8 in obj1['colors']
         is_obj2_shape = len(obj2['colors']) == 1 and 8 not in obj2['colors']
         if is_obj1_pattern and is_obj2_shape:
             pattern_obj, shape_obj = obj1, obj2
         else:
             is_obj2_pattern = 8 in obj2['colors']
             is_obj1_shape = len(obj1['colors']) == 1 and 8 not in obj1['colors']
             if is_obj2_pattern and is_obj1_shape:
                 pattern_obj, shape_obj = obj2, obj1


    # Ensure both objects were successfully identified
    if pattern_obj is None or shape_obj is None:
        # Handle error: couldn't find the necessary objects
        # Returning the input grid or an empty grid might be options.
        # For this task structure, it implies an issue matching the pattern.
        print("Error: Could not identify both pattern and shape objects.")
        # Return empty grid as a signal of failure
        return [] 

    # 3. Extract necessary properties
    pattern_tile = pattern_obj['bbox_content']
    pattern_height = pattern_obj['height']
    pattern_width = pattern_obj['width']

    shape_bbox_content = shape_obj['bbox_content']
    tile_rows = shape_obj['height'] # Height of shape bbox determines rows of tiles
    tile_cols = shape_obj['width']  # Width of shape bbox determines columns of tiles

    # 4. Calculate output grid dimensions and initialize with background color
    output_height = tile_rows * pattern_height
    output_width = tile_cols * pattern_width
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    # 5. Conditionally tile the pattern based on shape_bbox_content
    for r_shape in range(tile_rows):
        for c_shape in range(tile_cols):
            # Check the color in the shape's bounding box content at this relative position
            if shape_bbox_content[r_shape, c_shape] != background_color:
                # If not background, place the pattern tile in the output grid
                start_row = r_shape * pattern_height
                end_row = start_row + pattern_height
                start_col = c_shape * pattern_width
                end_col = start_col + pattern_width

                # Ensure slicing dimensions match before assignment
                if output_grid[start_row:end_row, start_col:end_col].shape == pattern_tile.shape:
                    output_grid[start_row:end_row, start_col:end_col] = pattern_tile
                else:
                     print(f"Warning: Shape mismatch during tiling at ({r_shape},{c_shape}). Target shape: {output_grid[start_row:end_row, start_col:end_col].shape}, Pattern shape: {pattern_tile.shape}")
                     # Handle potential off-by-one or boundary issues if necessary

    # 6. Return the final grid as a list of lists
    return output_grid.tolist()