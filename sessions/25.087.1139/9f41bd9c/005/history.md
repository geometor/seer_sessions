
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
6. Draw the 'movable shape' at the new position: Copy the extracted `shape_content` (including any non-gray pixels within the original bounding box) onto the output grid, starting at the calculated `(target_row, target_col)`.
7. Modify the top row of the 'floor area': Iterate through each column index `c` from 0 to `grid_width - 1`. If the column `c` falls outside the horizontal range covered by the 'movable shape' in its *new* position (i.e., if `c < target_col` or `c >= target_col + shape_w`), change the pixel color at `(floor_top_row, c)` in the output grid to maroon (9). Pixels in `floor_top_row` that are under the moved shape remain magenta (6).
"""

# Helper functions
def find_object_bbox(grid, color):
    """Finds the bounding box of the first contiguous object of a given color."""
    rows, cols = np.where(grid == color)
    if rows.size == 0:
        return None # Object not found
    min_r, max_r = np.min(rows), np.max(rows)
    min_c, max_c = np.min(cols), np.max(cols)
    # Need to handle potentially multiple disconnected components,
    # but examples suggest one main gray object.
    # Assuming the bounding box covers all pixels of that color is sufficient here.
    return min_r, min_c, max_r, max_c

def get_object_pixels(grid, bbox):
    """Extracts the pixels within a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    return grid[min_r:max_r+1, min_c:max_c+1]

def clear_area(grid, bbox, fill_color):
    """Fills a specified bounding box area with a given color."""
    min_r, min_c, max_r, max_c = bbox
    grid[min_r:max_r+1, min_c:max_c+1] = fill_color

def draw_object(grid, obj_pixels, top_left_coord):
    """Draws the object pixels onto the grid at a new location."""
    r_start, c_start = top_left_coord
    obj_h, obj_w = obj_pixels.shape
    r_end = r_start + obj_h
    c_end = c_start + obj_w

    # Ensure we don't draw outside grid bounds (basic clipping)
    grid_h, grid_w = grid.shape
    view_h = min(obj_h, grid_h - r_start)
    view_w = min(obj_w, grid_w - c_start)
    grid_view = grid[r_start:r_start+view_h, c_start:c_start+view_w]
    obj_view = obj_pixels[:view_h, :view_w]

    # Only draw if the shapes match (avoid broadcasting errors if clipping occurred unexpectedly)
    if grid_view.shape == obj_view.shape:
        grid[r_start:r_start+view_h, c_start:c_start+view_w] = obj_view
    else:
        # This case might indicate an issue with target calculation or grid dimensions
        print(f"Warning: Shape mismatch during drawing. Grid view: {grid_view.shape}, Obj view: {obj_view.shape}")


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
        # If no gray object found, return the original grid (or handle as error)
        print("Warning: Gray object not found.")
        return output_grid

    min_r, min_c, max_r, max_c = movable_shape_bbox
    shape_h = max_r - min_r + 1
    shape_w = max_c - min_c + 1
    # Extract the actual content within the bounding box from the input grid
    shape_content = get_object_pixels(input_grid, movable_shape_bbox)

    # 3. Identify the 'floor area' top row
    magenta_rows, _ = np.where(input_grid == MAGENTA)
    if magenta_rows.size == 0:
        # If no magenta floor found, maybe return original grid or error
        print("Warning: Magenta floor area not found.")
        # Decide on behavior: return original, or perhaps define a default floor?
        # Based on examples, assuming it's always present.
        # As a fallback, maybe use the last row?
        # For now, returning grid as is if no magenta.
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

    # Check if target position is valid (e.g., target_row is not negative)
    if target_row < 0:
        print(f"Warning: Calculated target row ({target_row}) is out of bounds. Clamping to 0.")
        target_row = 0
    # Target column calculation already ensures it's within bounds based on width

    # 5. Clear the original position in the output grid
    clear_area(output_grid, movable_shape_bbox, BLUE)

    # 6. Draw the 'movable shape' content at the new position
    draw_object(output_grid, shape_content, (target_row, target_col))

    # 7. Modify the top row of the 'floor area'
    for c in range(grid_w):
        # Check if the column 'c' is *outside* the horizontal span of the moved object
        is_outside_object = c < target_col or c >= target_col + shape_w
        # Only change if it was originally magenta and is outside the new object span
        if is_outside_object and input_grid[floor_top_row, c] == MAGENTA:
             output_grid[floor_top_row, c] = MAROON
        # Pixels originally magenta under the object remain magenta (implicitly handled by copy)

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
