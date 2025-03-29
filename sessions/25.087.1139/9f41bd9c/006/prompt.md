
Previous Code:
```python
import numpy as np

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid. The background color is blue (1).
2. Identify the 'movable shape': Locate all gray (5) pixels and determine their bounding box (min/max row/col). Note the height (`shape_h`) and width (`shape_w`) of this bounding box. Extract the rectangular block of pixels (`shape_content`) from the input grid corresponding to this bounding box.
3. Identify the 'floor area': Find the uppermost row index (`floor_top_row`) that contains magenta (6) pixels. Assume this marks the top of a solid magenta block at the bottom.
4. Calculate the target destination for the 'movable shape':
    a. Calculate the target top row: `target_row = floor_top_row - shape_h`.
    b. Calculate the target left column: Find the horizontal center of the input grid (`grid_center_c = (grid_width - 1) / 2`) and the horizontal center of the 'movable shape's' initial bounding box (`shape_center_c = (min_col + max_col) / 2`). If `shape_center_c > grid_center_c`, set `target_col = 0`. Otherwise (if `shape_center_c <= grid_center_c`), set `target_col = grid_width - shape_w`.
5. Clear the original position of the 'movable shape' in the output grid: Fill the area defined by the original bounding box with the background color (blue 1).
6. Draw the 'movable shape' at the new position: Iterate through the pixels within the extracted `shape_content`. If a pixel's color is gray (5), copy it to the corresponding position relative to the calculated `(target_row, target_col)` in the output grid. Other pixels within the `shape_content` (e.g., background blue) are *not* copied; the destination grid retains its background color in those positions.
7. Modify the top row of the 'floor area': Iterate through each column index `c` from 0 to `grid_width - 1`. If the column `c` falls outside the horizontal range covered by the 'movable shape' in its *new* position (i.e., if `c < target_col` or `c >= target_col + shape_w`), change the pixel color at `(floor_top_row, c)` in the output grid to maroon (9). Pixels in `floor_top_row` that are under the moved shape remain magenta (6).
"""

# Imports
import numpy as np

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

def draw_object_selective(grid, obj_pixels, top_left_coord, object_color):
    """
    Draws only the pixels of 'object_color' from 'obj_pixels' onto the grid
    at the specified 'top_left_coord'. Other pixels in 'obj_pixels' are ignored,
    leaving the grid's existing background color intact.
    """
    r_start, c_start = top_left_coord
    obj_h, obj_w = obj_pixels.shape
    grid_h, grid_w = grid.shape

    for r_offset in range(obj_h):
        for c_offset in range(obj_w):
            # Calculate target grid coordinates
            target_r = r_start + r_offset
            target_c = c_start + c_offset

            # Check if the source pixel is the object color
            if obj_pixels[r_offset, c_offset] == object_color:
                # Check if the target coordinates are within grid bounds
                if 0 <= target_r < grid_h and 0 <= target_c < grid_w:
                    grid[target_r, target_c] = object_color


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Constants for colors
    BLUE = 1
    GRAY = 5
    MAGENTA = 6
    MAROON = 9

    # 1. Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    grid_h, grid_w = output_grid.shape

    # 2. Identify the 'movable shape' (gray object)
    movable_shape_bbox = find_object_bbox(input_grid, GRAY)
    if movable_shape_bbox is None:
        # If no gray object found, return the original grid
        # print("Warning: Gray object not found.") # Keep commented unless debugging
        return output_grid # Task seems to assume the object is always present

    min_r, min_c, max_r, max_c = movable_shape_bbox
    shape_h = max_r - min_r + 1
    shape_w = max_c - min_c + 1
    # Extract the content within the bounding box from the input grid
    shape_content = get_object_pixels(input_grid, movable_shape_bbox)

    # 3. Identify the 'floor area' top row
    magenta_rows, _ = np.where(input_grid == MAGENTA)
    if magenta_rows.size == 0:
        # If no magenta floor found, assume it's always present per examples.
        # print("Warning: Magenta floor area not found.") # Keep commented unless debugging
        return output_grid # Or handle error appropriately
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
    if target_row < 0:
        # print(f"Warning: Calculated target row ({target_row}) is out of bounds. Clamping to 0.") # Keep commented
        target_row = 0

    # 5. Clear the original position of the *bounding box* in the output grid
    #    We clear the whole bounding box area, not just gray pixels.
    clear_area(output_grid, movable_shape_bbox, BLUE)

    # 6. Draw only the gray parts of the 'movable shape' content at the new position
    draw_object_selective(output_grid, shape_content, (target_row, target_col), GRAY)

    # 7. Modify the top row of the 'floor area'
    for c in range(grid_w):
        # Check if the column 'c' is *outside* the horizontal span of the moved object's bounding box
        is_outside_object = c < target_col or c >= target_col + shape_w
        # Only change if it was originally magenta AND is outside the new object span
        # Note: We check the *original* grid for magenta color to avoid issues if
        # the object was initially overlapping the floor row.
        if is_outside_object and input_grid[floor_top_row, c] == MAGENTA:
             output_grid[floor_top_row, c] = MAROON
        # If the pixel was originally magenta and is *under* the object's new span,
        # it should remain magenta. The copy handles this unless the object overwrites it.
        # Our selective draw ensures the floor below the object isn't changed unless
        # the object itself lands on that row (which it does by definition here).
        # Let's ensure that if a pixel under the object *wasn't* magenta originally, it doesn't become magenta.
        elif not is_outside_object:
            # If under the object, ensure it's magenta ONLY IF it was originally magenta.
            # The initial copy handles this, but being explicit might prevent edge cases.
            # If the target_row happens to be the floor_top_row, draw_object_selective might
            # place gray pixels there. The floor modification happens after, so we need to ensure
            # the rule applies correctly: parts under the object stay magenta *if they were magenta*.
            # Let's refine the logic slightly:
            # The floor row modification only applies to pixels that were initially magenta.
            if input_grid[floor_top_row, c] == MAGENTA:
                 # If it was magenta and outside, it becomes maroon (handled above).
                 # If it was magenta and inside, it stays magenta (implicitly handled by copy,
                 # unless overwritten by the object itself landing exactly on this row,
                 # which shouldn't happen based on target_row calculation `floor_top_row - shape_h`).
                 # Let's ensure it stays magenta if under the object.
                 output_grid[floor_top_row, c] = MAGENTA
            # else: if it wasn't magenta originally, it stays whatever it became (likely blue from clearing).


    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 5 5 5 5 5
1 1 1 1 1 1 1 1 1 1 1 1 5 5 5 5 5
1 1 1 1 1 1 1 1 1 1 1 1 5 1 5 1 5
1 1 1 1 1 1 1 1 1 1 1 1 5 1 5 1 5
1 1 1 1 1 1 1 1 1 1 1 1 5 1 5 1 5
1 1 1 1 1 1 1 1 1 1 1 1 5 1 5 1 5
1 1 1 1 1 1 1 1 1 1 1 1 5 1 5 1 5
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
5 5 5 5 5 1 1 1 1 1 1 1 1 1 1 1 1
5 5 5 5 5 1 1 1 1 1 1 1 1 1 1 1 1
5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1 1
1 5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1
1 1 5 1 5 1 5 1 1 1 1 1 1 1 1 1 1
1 1 1 5 1 5 1 5 1 1 1 1 1 1 1 1 1
1 1 1 1 5 1 5 1 5 1 1 1 1 1 1 1 1
6 6 6 6 6 9 9 9 9 9 9 9 9 9 9 9 9
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
5 5 5 5 5 1 1 1 1 1 1 1 1 1 1 1 1
5 5 5 5 5 1 1 1 1 1 1 1 1 1 1 1 1
5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1 1
5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1 1
5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1 1
5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1 1
5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1 1
6 6 6 6 6 9 9 9 9 9 9 9 9 9 9 9 9
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Match: False
Pixels Off: 18
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 6.228373702422147

## Example 2:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
5 5 5 5 5 1 1 1 1 1 1 1 1 1 1 1
5 5 5 5 5 1 1 1 1 1 1 1 1 1 1 1
5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1
5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1
5 1 5 1 5 1 1 1 1 1 1 1 1 1 1 1
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 5 5 5 5 5
1 1 1 1 1 1 1 1 1 1 1 5 5 5 5 5
1 1 1 1 1 1 1 1 1 1 1 5 1 5 1 5
1 1 1 1 1 1 1 1 1 1 5 1 5 1 5 1
1 1 1 1 1 1 1 1 1 5 1 5 1 5 1 1
9 9 9 9 9 9 9 9 9 9 9 9 9 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Transformed Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 5 5 5 5 5
1 1 1 1 1 1 1 1 1 1 1 5 5 5 5 5
1 1 1 1 1 1 1 1 1 1 1 5 1 5 1 5
1 1 1 1 1 1 1 1 1 1 1 5 1 5 1 5
1 1 1 1 1 1 1 1 1 1 1 5 1 5 1 5
9 9 9 9 9 9 9 9 9 9 9 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 7.8125
