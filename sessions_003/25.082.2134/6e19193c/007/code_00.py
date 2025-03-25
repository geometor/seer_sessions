"""
1.  **Object Identification:** Identify all contiguous blocks of non-zero pixels. Each block is considered an object and is defined by its color and the coordinates of its pixels.

2.  **Center Lines:** Define a vertical and a horizontal center line dividing the grid into four quadrants.

3.  **Left-Side Transformation:**
    *   Condition: If all pixels of an object are entirely to the left of the vertical center line.
    *   Action: Move the object to the right such that the leftmost pixel of the object is one position left of the vertical center line. The row coordinates of all pixels within the object remain unchanged.

4.  **Right-Side Transformation:**
    *   Condition: If all pixels of an object are entirely to the right of the vertical center line.
    *   Action:
        1. Determine the top-right pixel (r, c) of the object.
        2.  Calculate the vertical distance (dv) from the horizontal center: `dv = horizontal_center - 1 - r`
        3.  Move the entire object down by `dv` rows.
        4. Calculate distance (original_dist) between the leftmost column of the object and vertical center.
        5. Move the entire object left such that the rightmost pixel of the transformed object is at `c = vertical_center - 1 - original_dist`.

5. **Horizontal Mirroring:**
    *    Condition: If an object contains one or more pixels with a row index of either `horizontal_center - 1` or `horizontal_center`.
    *     Action: For each pixel `(r, c)` in the object, create a new pixel at `(r, cols - 1 - c)` in the output. Note that other transformations are applied *before* the mirroring.

6.  **Output:** Create a new grid filled with zeros (white). Place the transformed objects onto this grid according to the transformations above. If multiple transformations apply, apply them in the order: Left-Side, Right-Side, then Horizontal Mirroring.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, obj_color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != obj_color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, obj_color, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append((grid[r,c], current_object))  # Store color and object
    return objects

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape
    vertical_center = cols // 2
    horizontal_center = rows // 2

    # Find objects
    objects = find_objects(input_grid)
    
    transformed_objects = []

    # Apply Left and Right transformations
    for color, obj in objects:
        # --- Left Side Transformation ---
        if all(c < vertical_center for _, c in obj):
            leftmost_col = min(c for _, c in obj)
            new_obj = []
            for r, c in obj:
                new_c = vertical_center - 1 - (leftmost_col - min(c_temp for _, c_temp in obj))
                new_obj.append((r, new_c))
            transformed_objects.append((color,new_obj))

        # --- Right Side Transformation ---
        elif all(c >= vertical_center for _, c in obj):
            top_right_r, top_right_c = max(obj, key=lambda item: (item[1], -item[0])) #fixed to use max
            dv = horizontal_center - 1 - top_right_r
            leftmost_col = min(c for _, c in obj) # find leftmost column
            original_dist = leftmost_col - vertical_center #find dist to vert center            
            new_obj = []

            for r, c in obj:
                new_r = r + dv
                new_c = vertical_center - 1- original_dist - (top_right_c - c)  # Corrected c calculation

                if 0 <= new_r < rows and 0 <= new_c < cols: # added bounds
                    new_obj.append((new_r,new_c))
            transformed_objects.append((color, new_obj))
        else:
             transformed_objects.append((color, obj)) #keep to apply horizontal

    # Apply horizontal mirroring and place on output
    for color, obj in transformed_objects:
        if any(r == horizontal_center - 1 or r == horizontal_center for r, _ in obj):
            for r_orig, c_orig in obj:
                output_grid[r_orig, cols - 1 - c_orig] = color  #horizontal
        else: #place all other objects
            for r, c in obj:
              if 0 <= r < rows and 0 <= c < cols: #added bounds
                output_grid[r,c] = color

    return output_grid