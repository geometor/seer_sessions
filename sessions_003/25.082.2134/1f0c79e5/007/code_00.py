"""
The transformation rule involves identifying a contiguous object in the input grid, determining its core and unique colors, and then performing a mirroring operation based on the unique color's position relative to the object's bounding box. If a unique color exists and is on an edge, the object is mirrored along that edge. If the unique color is in a corner, a diagonal mirror is performed. The output grid's dimensions are two greater in both height and width than the bounding box, or size adjusted to contain object. If there is only one pixel, a 3x3 is produced. If there is only a row, a 3 high grid is returned, and if there is only a column, a 3 wide grid is returned.

"""

import numpy as np

def find_object_and_bbox(grid):
    """Finds the object (non-zero pixels) and its bounding box."""
    non_zero_pixels = np.argwhere(grid != 0)
    if len(non_zero_pixels) == 0:
        return [], None  # No object found

    min_row, min_col = np.min(non_zero_pixels, axis=0)
    max_row, max_col = np.max(non_zero_pixels, axis=0)
    object_pixels = [(r, c) for r in range(min_row, max_row + 1)
                     for c in range(min_col, max_col + 1)
                     if grid[r, c] != 0]
    bbox = ((min_row, max_row), (min_col, max_col))
    return object_pixels, bbox

def get_core_and_unique_colors(grid, object_pixels):
    """Identifies the core and unique/pseudo-unique colors within the object."""
    if not object_pixels:
        return None, None, None

    color_counts = {}
    for r, c in object_pixels:
        color = grid[r, c]
        color_counts[color] = color_counts.get(color, 0) + 1

    sorted_colors = sorted(color_counts.items(), key=lambda item: item[1], reverse=True)
    core_color = sorted_colors[0][0]
    unique_color = None
    pseudo_unique_color = None

    if len(sorted_colors) > 1:
      min_count = min(count for _, count in sorted_colors)
      min_colors = [color for color, count in sorted_colors if count == min_count]
      if len(min_colors) == 1 and min_count == 1:
        unique_color = min_colors[0]
      elif len(min_colors) >= 1:
        pseudo_unique_color = min_colors[0]

    return core_color, unique_color, pseudo_unique_color

def find_pixel_location(grid, object_pixels, color):
    """Finds the first location of a given color within the object."""
    if color is None:
        return None
    for r, c in object_pixels:
        if grid[r, c] == color:
            return (r, c)
    return None

def determine_mirroring(bbox, unique_pixel_loc, core_color, input_grid):
    """Determines mirroring operations based on unique pixel location."""
    if unique_pixel_loc is None:
        return "none", None  # No mirroring

    (min_row, max_row), (min_col, max_col) = bbox
    row, col = unique_pixel_loc

    obj_h = max_row - min_row + 1
    obj_w = max_col - min_col + 1

    # check for simple extension
    if obj_h == 1 and obj_w == 1:
        return "extend_all", None
    # Check for horizontal extension
    if obj_h == 1:
        return "extend_horizontal", obj_w
    # Check for vertical extension
    if obj_w == 1:
        return "extend_vertical", obj_h

    # Check if unique color is on any edge
    if col == max_col:
       return "horizontal", "right"
    if col == min_col:
        return "horizontal", "left"
    if row == max_row:
        return "vertical", "up"
    if row == min_row:
        return "vertical", "down"

    # Corner mirroring
    if row == min_row and col == min_col:
        return "diagonal", "top_left"
    if row == min_row and col == max_col:
       return "diagonal", "top_right"
    if row == max_row and col == min_col:
        return "diagonal", "bottom_left"
    if row == max_row and col == max_col:
        return "diagonal", "bottom_right"

    return "unknown", None # this case should be investigated

def transform(input_grid):
    # Find the object and its bounding box
    object_pixels, bbox = find_object_and_bbox(input_grid)

    # Get the core and unique/pseudo colors
    core_color, unique_color, pseudo_unique_color = get_core_and_unique_colors(input_grid, object_pixels)

    # Find the location of the unique or pseudo-unique pixel
    unique_pixel_loc = find_pixel_location(input_grid, object_pixels, unique_color)
    if unique_pixel_loc is None:
        unique_pixel_loc = find_pixel_location(input_grid, object_pixels, pseudo_unique_color)

    # Determine mirroring direction and details
    mirror_type, mirror_details = determine_mirroring(bbox, unique_pixel_loc, core_color, input_grid)

    if mirror_type == "extend_all":
        output_grid = np.full((3, 3), core_color)

    elif mirror_type == "extend_horizontal":
        extended = np.tile(input_grid[unique_pixel_loc[0],:], (1, mirror_details + 2))
        output_grid = np.vstack([extended, input_grid, extended])

    elif mirror_type == "extend_vertical":
        extended = np.tile(input_grid[:,unique_pixel_loc[1]].reshape(-1,1), (mirror_details + 2, 1))
        output_grid = np.hstack([extended, input_grid, extended])

    elif mirror_type == "horizontal":
        (min_row, max_row), (min_col, max_col) = bbox
        obj = input_grid[min_row:max_row+1, min_col:max_col+1]
        h, w = obj.shape

        if mirror_details == "right":
            output_grid = np.hstack([np.fliplr(obj), obj[:, 1:]])

        elif mirror_details == "left":
            output_grid = np.hstack([obj[:, :-1], np.fliplr(obj)])
        output_grid = np.pad(output_grid, pad_width=1, mode='constant', constant_values=0)

    elif mirror_type == "vertical":
        (min_row, max_row), (min_col, max_col) = bbox
        obj = input_grid[min_row:max_row+1, min_col:max_col+1]
        h, w = obj.shape
        if mirror_details == "up":
            output_grid = np.vstack([np.flipud(obj), obj[1:, :]])
        elif mirror_details == "down":
            output_grid = np.vstack([obj[:-1,:], np.flipud(obj)])

        output_grid = np.pad(output_grid, pad_width=1, mode='constant', constant_values=0)

    elif mirror_type == "diagonal":
        (min_row, max_row), (min_col, max_col) = bbox
        obj = input_grid[min_row:max_row+1, min_col:max_col+1]
        h, w = obj.shape
        flipped_obj = np.transpose(obj)

        if mirror_details == "top_left":
            output_grid = np.block([[obj, np.fliplr(obj)], [np.flipud(obj), flipped_obj]])
        elif mirror_details == "top_right":
           output_grid = np.block([[np.fliplr(obj),obj], [np.fliplr(np.flipud(obj)), np.flipud(obj)]])
        elif mirror_details == "bottom_left":
           output_grid = np.block([[np.flipud(obj), np.fliplr(np.flipud(obj))], [obj, np.fliplr(obj)]])
        elif mirror_details == "bottom_right":
            output_grid = np.block([[np.fliplr(obj), np.fliplr(np.flipud(obj))], [np.flipud(obj), obj]])

        # find object and pad
        output_grid = np.pad(output_grid[1:-1, 1:-1], pad_width=1, mode='constant', constant_values=0)

    else: # case "unknown"
        # default empty grid of max size
        output_grid = np.zeros((9,9), dtype=int)


    return output_grid