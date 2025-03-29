import numpy as np

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid. The background color is assumed to be blue (1).
2. Identify the 'movable shape': Locate all gray (5) pixels and determine their bounding box (min/max row/col). Note the height (`shape_h`) and width (`shape_w`) of this bounding box. Extract the rectangular block of pixels (`shape_content`) from the input grid corresponding to this bounding box. This block includes any background (blue) pixels within the bounding box.
3. Identify the 'floor area': Find the uppermost row index (`floor_top_row`) that contains magenta (6) pixels. Assume this marks the top of a solid magenta block at the bottom.
4. Calculate the target destination for the 'movable shape':
    a. Calculate the target top row: `target_row = floor_top_row - shape_h`.
    b. Calculate the target left column: Find the horizontal center of the input grid (`grid_center_c = (grid_width - 1) / 2`) and the horizontal center of the 'movable shape's' initial bounding box (`shape_center_c = (min_col + max_col) / 2`). If `shape_center_c > grid_center_c` (shape starts on the right side), set `target_col = 0` (move to left edge). Otherwise (if `shape_center_c <= grid_center_c`, shape starts on the left or center), set `target_col = grid_width - shape_w` (move to right edge).
5. Clear the original position of the 'movable shape' in the output grid: Fill the area defined by the original bounding box with the background color (blue 1).
6. Draw the 'movable shape' at the new position: Copy the entire extracted `shape_content` (including gray and any internal blue pixels) to the output grid, with its top-left corner at the calculated `(target_row, target_col)`.
7. Modify the top row of the 'floor area': Iterate through each column index `c` from 0 to `grid_width - 1`. If the column `c` falls outside the horizontal range covered by the 'movable shape' in its *new* position (i.e., if `c < target_col` or `c >= target_col + shape_w`) AND the pixel at `(floor_top_row, c)` in the *input* grid was magenta (6), change the pixel color at `(floor_top_row, c)` in the *output* grid to maroon (9). Pixels in `floor_top_row` that were originally magenta and are now under the moved shape remain magenta (6).
"""

# Imports
import numpy as np

# Constants for colors
BLUE = 1
GRAY = 5
MAGENTA = 6
MAROON = 9

# Helper functions
def find_object_bbox(grid, color):
    """Finds the bounding box of all pixels of a given color."""
    rows, cols = np.where(grid == color)
    if rows.size == 0:
        return None # Object color not found
    min_r, max_r = np.min(rows), np.max(rows)
    min_c, max_c = np.min(cols), np.max(cols)
    return min_r, min_c, max_r, max_c

def get_object_pixels(grid, bbox):
    """Extracts the pixels within a bounding box."""
    if bbox is None:
        return None
    min_r, min_c, max_r, max_c = bbox
    return grid[min_r:max_r+1, min_c:max_c+1]

def clear_area(grid, bbox, fill_color):
    """Fills a specified bounding box area with a given color."""
    if bbox is None:
        return
    min_r, min_c, max_r, max_c = bbox
    grid[min_r:max_r+1, min_c:max_c+1] = fill_color

def draw_object(grid, obj_pixels, top_left_coord):
    """
    Draws the entire obj_pixels block onto the grid
    at the specified top_left_coord.
    Overwrites existing pixels.
    """
    r_start, c_start = top_left_coord
    obj_h, obj_w = obj_pixels.shape
    grid_h, grid_w = grid.shape

    # Calculate the destination slice boundaries
    r_end = r_start + obj_h
    c_end = c_start + obj_w

    # Ensure boundaries are within the grid
    r_end = min(r_end, grid_h)
    c_end = min(c_end, grid_w)
    r_start = max(r_start, 0)
    c_start = max(c_start, 0)

    # Calculate the source slice boundaries (if object partially off grid)
    src_r_start = max(0, -top_left_coord[0])
    src_c_start = max(0, -top_left_coord[1])
    src_r_end = obj_h - max(0, r_end - grid_h)
    src_c_end = obj_w - max(0, c_end - grid_w)
    
    # Check if there is anything to draw within bounds
    if r_start < r_end and c_start < c_end:
        grid[r_start:r_end, c_start:c_end] = obj_pixels[src_r_start:src_r_end, src_c_start:src_c_end]


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    grid_h, grid_w = output_grid.shape

    # 2. Identify the 'movable shape' (gray object)
    movable_shape_bbox = find_object_bbox(input_grid, GRAY)
    if movable_shape_bbox is None:
        # If no gray object found, return the original grid (as per observed behavior)
        return output_grid 

    min_r, min_c, max_r, max_c = movable_shape_bbox
    shape_h = max_r - min_r + 1
    shape_w = max_c - min_c + 1
    # Extract the content (including background) within the bounding box
    shape_content = get_object_pixels(input_grid, movable_shape_bbox)

    # 3. Identify the 'floor area' top row
    magenta_rows, _ = np.where(input_grid == MAGENTA)
    if magenta_rows.size == 0:
        # If no magenta floor found, return original (as per observed behavior)
        return output_grid 
    floor_top_row = np.min(magenta_rows)

    # 4. Calculate the target destination
    # 4a. Target row
    target_row = floor_top_row - shape_h

    # 4b. Target column
    grid_center_c = (grid_w - 1) / 2.0
    shape_center_c = (min_c + max_c) / 2.0

    if shape_center_c > grid_center_c:
        # Initial position is right-biased, move to left edge
        target_col = 0
    else:
        # Initial position is left-biased or centered, move to right edge
        target_col = grid_w - shape_w

    # Ensure target row is not negative (clamp if necessary)
    # Although calculation seems to avoid this in examples, good practice.
    target_row = max(0, target_row) 

    # 5. Clear the original position of the *bounding box* in the output grid
    clear_area(output_grid, movable_shape_bbox, BLUE)

    # 6. Draw the entire 'movable shape' content (including internal blue) at the new position
    draw_object(output_grid, shape_content, (target_row, target_col))

    # 7. Modify the top row of the 'floor area'
    for c in range(grid_w):
        # Check if the column 'c' is *outside* the horizontal span of the moved object's bounding box
        is_outside_object = c < target_col or c >= target_col + shape_w
        
        # Check the color in the *original* grid at this position
        original_color_at_floor = input_grid[floor_top_row, c]

        # Only change to maroon if it was originally magenta AND is outside the new object span
        if is_outside_object and original_color_at_floor == MAGENTA:
             output_grid[floor_top_row, c] = MAROON
        # Note: If it was originally magenta and is *under* the object's new span,
        # it should remain magenta. The initial copy handles this base case.
        # The draw_object function might overwrite it with gray/blue from the shape,
        # but the floor modification step itself doesn't change these pixels back to magenta.
        # This behavior matches the examples.

    return output_grid