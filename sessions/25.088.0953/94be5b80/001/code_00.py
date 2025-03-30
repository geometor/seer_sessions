import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify a palette object, which is a small line (horizontal or vertical) of unique, adjacent, non-background colors [C1, C2, ..., CN].
2. Identify core objects Obj2, Obj3, ..., Obj(N-1) in the input grid, where each Obj_i has the color C_i from the *inner* part of the palette sequence.
3. Calculate the vertical displacement (delta_y) between the top rows of the first two core objects (Obj2 and Obj3).
4. Create an output grid initialized with the background color (0).
5. Copy all identified core objects (Obj2 through Obj(N-1)) to the output grid at their original positions.
6. Create a new object using the shape of Obj2 but colored with the first palette color (C1). Place this new object on the output grid, vertically shifted *up* by delta_y relative to Obj2's original position.
7. If the palette has more than 3 colors (N > 3), create another new object using the shape of the *last* core object (Obj(N-1)) but colored with the last palette color (CN). Place this new object on the output grid, vertically shifted *down* by delta_y relative to Obj(N-1)'s original position.
8. The resulting grid with the original core objects and the newly created/colored/shifted objects is the final output. The original palette object is not copied.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects found. Each object is a dictionary containing:
              'color': The color of the object.
              'pixels': A set of (row, col) tuples representing the object's pixels.
              'bounds': A tuple (min_row, min_col, max_row, max_col).
              'shape_mask': A np.array representing the object's shape relative to its bounding box.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
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
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_pixels:
                    obj_height = max_r - min_r + 1
                    obj_width = max_c - min_c + 1
                    shape_mask = np.zeros((obj_height, obj_width), dtype=int)
                    for p_r, p_c in obj_pixels:
                        shape_mask[p_r - min_r, p_c - min_c] = color

                    objects.append({
                        'color': color,
                        'pixels': obj_pixels,
                        'bounds': (min_r, min_c, max_r, max_c),
                        'shape_mask': shape_mask
                    })
    return objects

def find_palette(grid):
    """
    Finds the palette object (a horizontal or vertical line of unique non-zero colors).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: The sequence of colors in the palette, or None if not found.
    """
    height, width = grid.shape
    background_color = 0

    # Check horizontal lines
    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color:
                palette = []
                cc = c
                while cc < width and grid[r, cc] != background_color:
                    color = grid[r, cc]
                    # Check uniqueness and non-zero
                    if color in palette or color == background_color:
                         palette = None # Invalid palette
                         break
                    # Check if part of a larger vertical structure (not just a line)
                    if (r > 0 and grid[r-1, cc] != background_color) or \
                       (r < height - 1 and grid[r+1, cc] != background_color):
                        palette = None # Not just a line
                        break
                    palette.append(color)
                    cc += 1

                if palette and len(palette) > 1:
                    # Verify it's not part of a larger horizontal structure immediately adjacent
                    is_isolated_line = True
                    for pc in range(c, cc):
                       # Check left/right immediate neighbors (should be background or edge)
                       if pc > 0 and grid[r, pc-1] != background_color and pc-1 < c:
                           is_isolated_line = False
                           break
                       if pc < width - 1 and grid[r, pc+1] != background_color and pc+1 >= cc:
                           is_isolated_line = False
                           break
                    if is_isolated_line:
                       return palette

    # Check vertical lines
    for c in range(width):
        for r in range(height):
             if grid[r, c] != background_color:
                palette = []
                rr = r
                while rr < height and grid[rr, c] != background_color:
                    color = grid[rr, c]
                    # Check uniqueness and non-zero
                    if color in palette or color == background_color:
                        palette = None
                        break
                    # Check if part of a larger horizontal structure (not just a line)
                    if (c > 0 and grid[rr, c-1] != background_color) or \
                       (c < width - 1 and grid[rr, c+1] != background_color):
                        palette = None
                        break
                    palette.append(color)
                    rr += 1

                if palette and len(palette) > 1:
                    # Verify it's not part of a larger vertical structure immediately adjacent
                    is_isolated_line = True
                    for pr in range(r, rr):
                        # Check up/down immediate neighbors (should be background or edge)
                        if pr > 0 and grid[pr-1, c] != background_color and pr-1 < r:
                           is_isolated_line = False
                           break
                        if pr < height - 1 and grid[pr+1, c] != background_color and pr+1 >= rr:
                           is_isolated_line = False
                           break
                    if is_isolated_line:
                       return palette

    return None # No palette found

def draw_object(grid, shape_mask, top_left_r, top_left_c, color):
    """Draws an object onto the grid using its shape mask and color."""
    obj_h, obj_w = shape_mask.shape
    grid_h, grid_w = grid.shape

    for r_offset in range(obj_h):
        for c_offset in range(obj_w):
            if shape_mask[r_offset, c_offset] != 0: # Use the original color in the mask to determine shape
                target_r = top_left_r + r_offset
                target_c = top_left_c + c_offset
                # Check grid boundaries
                if 0 <= target_r < grid_h and 0 <= target_c < grid_w:
                    grid[target_r, target_c] = color # Draw with the new color

def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    output_grid = np.zeros_like(input_grid) # Initialize with background color 0

    # 1. Find the palette
    palette = find_palette(input_grid)
    if not palette or len(palette) < 3:
        # If no valid palette (or too short), maybe return input or empty?
        # Based on examples, we expect a palette and core objects.
        # Returning input might be safer if logic isn't found. Let's try that.
        print("Warning: Palette not found or too short. Returning input.")
        return input_grid_list

    num_palette_colors = len(palette)
    c1 = palette[0]
    cn = palette[-1]

    # 2. Find the core objects
    core_objects_data = {} # Store by color for easy access
    core_object_list_ordered = [] # Store in palette order
    found_all_core = True
    for i in range(1, num_palette_colors - 1):
        core_color = palette[i]
        objects = find_objects(input_grid, core_color)
        if not objects:
            # Could not find a required core object
            print(f"Warning: Core object for color {core_color} not found.")
            found_all_core = False
            break
        # Assume only one object per core color as per examples
        if len(objects) > 1:
             print(f"Warning: Found multiple objects for core color {core_color}. Using the first one.")
        core_objects_data[core_color] = objects[0]
        core_object_list_ordered.append(objects[0])

    if not found_all_core or not core_object_list_ordered:
         print("Warning: Could not find all required core objects. Returning input.")
         return input_grid_list

    obj2_data = core_object_list_ordered[0] # Corresponds to C2
    obj3_data = core_object_list_ordered[1] # Corresponds to C3
    obj_last_core_data = core_object_list_ordered[-1] # Corresponds to C(N-1)

    # 3. Calculate vertical displacement
    delta_y = obj3_data['bounds'][0] - obj2_data['bounds'][0] # min_row(Obj3) - min_row(Obj2)

    # 4. Initialize output grid (already done)

    # 5. Copy all core objects to output grid
    for obj_data in core_object_list_ordered:
        min_r, min_c, _, _ = obj_data['bounds']
        draw_object(output_grid, obj_data['shape_mask'], min_r, min_c, obj_data['color'])

    # 6. Create and draw the first generated object (color C1, shape Obj2)
    obj2_min_r, obj2_min_c, _, _ = obj2_data['bounds']
    new_obj1_top_r = obj2_min_r - delta_y
    new_obj1_top_c = obj2_min_c
    # Use obj2's shape mask but draw with color C1
    draw_object(output_grid, obj2_data['shape_mask'], new_obj1_top_r, new_obj1_top_c, c1)

    # 7. Create and draw the second generated object if N > 3
    if num_palette_colors > 3:
        obj_last_core_min_r, obj_last_core_min_c, _, _ = obj_last_core_data['bounds']
        new_obj2_top_r = obj_last_core_min_r + delta_y
        new_obj2_top_c = obj_last_core_min_c
         # Use last core object's shape mask but draw with color CN
        draw_object(output_grid, obj_last_core_data['shape_mask'], new_obj2_top_r, new_obj2_top_c, cn)

    # 8. Return the final grid
    return output_grid.tolist()