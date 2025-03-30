
Previous Code:
```python
import numpy as np

"""
This transformation identifies a single non-white 'template' object in the input grid. 
It then tiles this object across the grid according to specific rules:

1. Horizontal Tiling (First Row):
   - The original object remains in place.
   - Copies are placed horizontally to the right with a fixed gap of 4 columns between their starting positions.
   - The color of the copies follows a repeating pattern: [original_color, original_color, magenta].
   - Tiling stops if the next copy would extend beyond the grid's width.

2. Vertical Tiling (Subsequent Rows):
   - The entire pattern generated in the first row (including the original object and its horizontal copies) acts as a template for vertical replication.
   - Rows are replicated downwards with a fixed vertical gap equal to the template object's height plus one row.
   - Crucially, only the *magenta* colored objects from the first row's pattern are copied into the subsequent rows. The original colored objects are skipped.
   - Tiling stops if the next row would extend beyond the grid's height.

The output grid contains the original object and all generated copies.
"""

def find_template_object(grid, background_color=0):
    """
    Finds the first contiguous non-background object and returns its properties.
    Assumes there is only one such object in the input.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color considered background.

    Returns:
        dict: A dictionary containing object properties:
              'r0', 'c0': top-left coordinates
              'h', 'w': height and width
              'color': the object's color
              'pattern': list of (dr, dc) relative coordinates of object pixels
              Returns None if no object is found.
    """
    non_bg_coords = np.argwhere(grid != background_color)
    if non_bg_coords.size == 0:
        return None # No object found

    # Find the coordinates of the first non-background pixel found during standard iteration
    # This assumes the first pixel belongs to the single object we care about.
    first_pixel_r, first_pixel_c = non_bg_coords[0]
    obj_color = grid[first_pixel_r, first_pixel_c]

    # Find all pixels belonging to this object (same color, contiguous)
    q = [(first_pixel_r, first_pixel_c)]
    visited = set(q)
    obj_pixels_abs = list(q) # Store absolute coordinates first

    while q:
        r, c = q.pop(0)

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # 4-connectivity
            nr, nc = r + dr, c + dc
            if (0 <= nr < grid.shape[0] and
                0 <= nc < grid.shape[1] and
                grid[nr, nc] == obj_color and
                (nr, nc) not in visited):
                visited.add((nr, nc))
                q.append((nr, nc))
                obj_pixels_abs.append((nr, nc))

    if not obj_pixels_abs: # Should not happen if non_bg_coords was found
         return None

    # Determine bounding box from the collected object pixels
    rows, cols = zip(*obj_pixels_abs)
    r0 = min(rows)
    c0 = min(cols)
    r1 = max(rows)
    c1 = max(cols)
    h = r1 - r0 + 1
    w = c1 - c0 + 1

    # Extract relative pattern pixels
    pattern_pixels_relative = []
    for r_abs, c_abs in obj_pixels_abs:
         pattern_pixels_relative.append((r_abs - r0, c_abs - c0))

    return {
        "r0": r0, "c0": c0, "h": h, "w": w,
        "color": obj_color, "pattern": pattern_pixels_relative
    }


def place_pattern(grid, r_start, c_start, pattern_pixels, color):
    """
    Places the object pattern onto the grid at the specified location and color.

    Args:
        grid (np.array): The target grid (modified in place).
        r_start (int): Top row for placing the pattern.
        c_start (int): Left column for placing the pattern.
        pattern_pixels (list): List of (dr, dc) relative coordinates.
        color (int): The color to draw the pattern with.
    """
    grid_height, grid_width = grid.shape
    for dr, dc in pattern_pixels:
        r, c = r_start + dr, c_start + dc
        # Check bounds before drawing
        if 0 <= r < grid_height and 0 <= c < grid_width:
            grid[r, c] = color


def transform(input_grid):
    """
    Applies the described tiling transformation to the input grid.

    Args:
        input_grid (np.array): The 2D input grid.

    Returns:
        np.array: The transformed 2D output grid.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    grid_height, grid_width = output_grid.shape

    # --- Step 1: Find the template object ---
    template_obj = find_template_object(output_grid)
    if template_obj is None:
        return output_grid # Return copy of input if no object found

    r0, c0 = template_obj["r0"], template_obj["c0"]
    h, w = template_obj["h"], template_obj["w"]
    template_color = template_obj["color"]
    pattern = template_obj["pattern"]

    # --- Step 2: Define constants and parameters ---
    magenta_color = 6
    horizontal_gap = 4
    vertical_gap = h + 1
    color_sequence = [template_color, template_color, magenta_color]

    # --- Step 3: Generate First Row ---
    first_row_objects = [] # Store info needed for vertical tiling: (col_start, color)
    # The original object is implicitly the first in the row
    first_row_objects.append({"c": c0, "color": template_color})

    current_c = c0 + horizontal_gap
    copy_index = 1 # Start counting copies from 1

    while current_c + w <= grid_width:
        # Determine color for this copy
        copy_color = color_sequence[copy_index % len(color_sequence)]

        # Place the copy
        place_pattern(output_grid, r0, current_c, pattern, copy_color)

        # Store info for vertical tiling
        first_row_objects.append({"c": current_c, "color": copy_color})

        # Move to the next potential position
        current_c += horizontal_gap
        copy_index += 1

    # --- Step 4: Generate Subsequent Rows ---
    current_r = r0 + vertical_gap

    while current_r + h <= grid_height:
        # Iterate through the objects placed in the first row
        for obj_info in first_row_objects:
            # Only copy if the object in the first row was magenta
            if obj_info["color"] == magenta_color:
                obj_c = obj_info["c"]
                # Place a magenta copy in the current row
                place_pattern(output_grid, current_r, obj_c, pattern, magenta_color)

        # Move to the next potential row position
        current_r += vertical_gap

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 7 7 7 0 6 6 6 0 7 7 7 0 7 7 7 0 6 6 6 0 7
0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6 0 7
0 0 0 7 7 7 0 7 7 7 0 6 6 6 0 7 7 7 0 7 7 7 0 6 6 6 0 7
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 7 7 7 0 6 6 6 0 7 7 7 0 7 7 7 0 6 6 6 0 0
0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6 0 0
0 0 0 7 7 7 0 7 7 7 0 6 6 6 0 7 7 7 0 7 7 7 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 4.037267080745352

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6
0 0 0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6
0 0 0 0 0 7 7 7 0 7 7 7 0 6 6 6 0 7 7 7 0 7 7 7 0 6 6 6
0 0 0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6
0 0 0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6
0 0 0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6
0 0 0 0 0 7 7 7 0 7 7 7 0 6 6 6 0 7 7 7 0 7 7 7 0 6 6 6
0 0 0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6
0 0 0 0 0 7 0 7 0 7 0 7 0 6 0 6 0 7 0 7 0 7 0 7 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 6 0 0 0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 1.2422360248447148
