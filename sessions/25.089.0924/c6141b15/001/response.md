```python
import numpy as np
from collections import deque

"""
Transformation rule based on object detection, color mapping, shape transformation, and coordinate transposition with color-dependent placement adjustments.

1.  Identify all connected components (objects) of non-background colors in the input grid. The background color is orange (7).
2.  Create an output grid initialized with the background color.
3.  For each identified input object:
    a. Determine its color (`C_in`) and the top-left corner of its bounding box (`r_min`, `c_min`).
    b. Determine the output color (`C_out`) based on `C_in` using a predefined mapping (e.g., Red->Blue, Blue->Red, Gray->Gray, Maroon->Maroon, etc.).
    c. Determine the target output shape (`S_out`) based on `C_in` (e.g., Pixel, Line, Plus, L-shape, Scatter).
    d. Calculate the transposed reference point: `P_t = (c_min, r_min)`.
    e. Calculate the output reference point `P_out` by applying a color-dependent transformation/offset `T(C_in)` to `P_t`. 
        - For Maroon (9): `P_out = (P_t.row + 3, P_t.col + 3)`.
        - For other colors, the rule is complex or currently undetermined. As a placeholder, we might use the transposed position directly or apply a default offset, acknowledging this is likely incorrect. For Gray (5), the rule seems inconsistent in the examples. Let's use `P_out = (P_t.row - 3, P_t.col - 3)` based on one example pixel, but this is speculative. For others, default to `P_out = P_t`.
    f. Generate the pixel coordinates for the output shape `S_out` relative to `P_out`.
        - For Maroon (9): A horizontal line of length 5 starting at `P_out`.
        - For Gray (5): A single pixel at `P_out`.
        - For other colors, the exact output shape generation is complex. As a placeholder, we might try drawing the *transposed* original shape relative to `P_out`, acknowledging this is incorrect for cases like Red->Plus or Blue->L.
    g. Draw the generated output shape pixels with the `C_out` color onto the output grid, ensuring coordinates are within bounds.
"""

def find_objects(grid, background_color):
    """
    Finds connected components (objects) of the same non-background color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The color to ignore.

    Returns:
        list: A list of objects. Each object is a dictionary containing:
              'color': The color of the object.
              'pixels': A set of (row, col) tuples for the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col).
    """
    objects = []
    visited = np.zeros(grid.shape, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def draw_pixel(grid, r, c, color):
    """ Safely draws a pixel onto the grid. """
    rows, cols = grid.shape
    if 0 <= r < rows and 0 <= c < cols:
        grid[r, c] = color

def draw_horizontal_line(grid, r, c, length, color):
    """ Safely draws a horizontal line starting at (r, c). """
    for i in range(length):
        draw_pixel(grid, r, c + i, color)
        
def draw_transposed_object(grid, obj_pixels, r_out_ref, c_out_ref, r_in_ref, c_in_ref, color):
    """ 
    Placeholder: Draws the object transposed relative to the output ref point.
    Calculates relative positions from input ref, transposes them, applies to output ref.
    """
    for r_in, c_in in obj_pixels:
        rel_r = r_in - r_in_ref
        rel_c = c_in - c_in_ref
        # Transpose relative coordinates
        draw_pixel(grid, r_out_ref + rel_c, c_out_ref + rel_r, color)


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    background_color = 7
    output_grid = np.full(input_grid.shape, background_color, dtype=int)
    rows, cols = input_grid.shape

    # 1. Find all input objects
    objects = find_objects(input_grid, background_color)

    # 2. Process each object
    for obj in objects:
        c_in = obj['color']
        pixels_in = obj['pixels']
        r_min, c_min, _, _ = obj['bbox']

        # a. Determine output color
        if c_in == 2: c_out = 1
        elif c_in == 1: c_out = 2
        else: c_out = c_in # 5->5, 9->9, 8->8, 4->4

        # b. Calculate transposed reference point (using top-left)
        r_t, c_t = c_min, r_min

        # c. Calculate output reference point based on input color (T(C_in))
        # These rules are hypotheses based on limited examples and known inconsistencies
        if c_in == 9: # Maroon (Ex 2) - Seems consistent
            r_out, c_out_ref = r_t + 3, c_t + 3
        elif c_in == 5: # Gray (Ex 2) - Inconsistent, using rule from one pixel
             r_out, c_out_ref = r_t - 3, c_t - 3
        # Placeholder for other colors - use transposed coordinate directly
        # This is definitely wrong for Ex 1 (Red/Blue) and Ex 3 (Yellow/Azure) placement
        else: 
             r_out, c_out_ref = r_t, c_t


        # d. Draw the output shape relative to the output reference point
        # These shape rules are also hypotheses/placeholders
        if c_in == 9: # Maroon -> Horizontal Line Length 5
            draw_horizontal_line(output_grid, r_out, c_out_ref, 5, c_out)
        elif c_in == 5: # Gray -> Single Pixel
            draw_pixel(output_grid, r_out, c_out_ref, c_out)
        # Placeholder for other shapes: Draw the transposed original shape
        # This is definitely wrong for Red->Plus, Blue->L, Yellow->Scatter
        else:
             draw_transposed_object(output_grid, pixels_in, r_out, c_out_ref, r_min, c_min, c_out)
             
    return output_grid
```