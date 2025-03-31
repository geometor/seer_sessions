import numpy as np
from collections import deque

"""
Transformation Rule Natural Language Description:

1.  Initialize Output: Create an output grid as a copy of the input grid.
2.  Identify Background: Determine the background color, defined as the most frequent color in the input grid.
3.  Find Objects: Identify all distinct contiguous objects composed of non-background colored pixels. Use 4-way adjacency (pixels are connected if they share an edge, not just a corner).
4.  Process Each Object: Iterate through each identified object and apply the first matching rule:
    *   Rule A (Bottom Line Removal):
        *   Check: Is the object exactly 1 pixel high and 5 pixels wide (total 5 pixels)? AND Is the object located entirely within the bottom-most row of the grid (its minimum and maximum row index equals the grid height minus 1)?
        *   Action: If both conditions are true, change all pixels belonging to this object in the output grid to the background color. Then, proceed to the next object.
    *   Rule B (Plus Sign Color Change):
        *   Check: Does the object have a bounding box of 3x3 pixels? AND Does the object consist of exactly 5 pixels? AND Does the shape correspond to a central pixel plus its four orthogonal neighbors? AND Is the color of the object Maroon (9), Magenta (6), or Green (3)?
        *   Action: If all conditions are true, change all 5 pixels belonging to this object in the output grid to Gray (5). Then, proceed to the next object.
    *   Rule C (No Change):
        *   Check: Does the object not meet the criteria for Rule A or Rule B?
        *   Action: If true, leave the object's pixels unchanged in the output grid (they retain their original color from the initial copy).
5.  Return Result: After processing all objects, return the modified output grid.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    if counts.size == 0:
        return 0 # Default background if grid is empty, though ARC constraints likely prevent this
    return colors[np.argmax(counts)]

def find_objects_bfs(grid, background_color):
    """
    Finds all connected objects of non-background color using BFS (4-way adjacency).

    Args:
        grid (np.array): The input grid.
        background_color (int): The background color to ignore.

    Returns:
        list: A list of dictionaries, each representing an object with its
              properties (coords, color, bbox, dimensions, pixel_count).
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            # If this pixel is part of the background or already visited, skip
            if grid[r, c] == background_color or visited[r, c]:
                continue

            # Start BFS from this pixel to find a new object
            obj_color = grid[r, c]
            obj_coords = []
            q = deque([(r, c)])
            visited[r, c] = True
            min_r, max_r = r, r
            min_c, max_c = c, c

            while q:
                row, col = q.popleft()
                obj_coords.append((row, col))
                min_r = min(min_r, row)
                max_r = max(max_r, row)
                min_c = min(min_c, col)
                max_c = max(max_c, col)

                # Explore neighbors (4-way adjacency)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    # Check bounds, if visited, or if not the object's color
                    if (0 <= nr < height and 0 <= nc < width and
                            not visited[nr, nc] and
                            grid[nr, nc] == obj_color):
                        visited[nr, nc] = True
                        q.append((nr, nc))

            # Store object properties
            obj_height = max_r - min_r + 1
            obj_width = max_c - min_c + 1
            objects.append({
                'coords': set(obj_coords), # Use set for faster lookups later
                'color': obj_color,
                'min_row': min_r,
                'max_row': max_r,
                'min_col': min_c,
                'max_col': max_c,
                'height': obj_height,
                'width': obj_width,
                'num_pixels': len(obj_coords)
            })
            
    return objects

def is_plus_sign(obj):
    """Checks if an object dictionary represents a 3x3 plus sign."""
    # Basic checks first
    if not (obj['height'] == 3 and obj['width'] == 3 and obj['num_pixels'] == 5):
        return False
        
    # Calculate potential center
    center_r = obj['min_row'] + 1
    center_c = obj['min_col'] + 1
    
    # Define expected coordinates based on center
    expected_coords = {
        (center_r, center_c),        # Center
        (center_r - 1, center_c),    # Top
        (center_r + 1, center_c),    # Bottom
        (center_r, center_c - 1),    # Left
        (center_r, center_c + 1)     # Right
    }
    
    # Check if the object's coordinates exactly match the expected plus shape
    return obj['coords'] == expected_coords


def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    Rule A: Removes 1x5 horizontal lines from the bottom row.
    Rule B: Changes the color of specific 3x3 plus-shaped objects (Maroon, Magenta, Green -> Gray).
    """
    # Convert input list of lists to a numpy array if necessary
    if isinstance(input_grid, list):
        input_array = np.array(input_grid, dtype=int)
    else:
        input_array = input_grid # Assume it's already a numpy array

    # 1. Initialize Output
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # 2. Identify Background color
    background_color = find_background_color(input_array)

    # 3. Find Objects
    objects = find_objects_bfs(input_array, background_color)

    # 4. Process Each Object
    for obj in objects:
        obj_color = obj['color']
        obj_coords_list = list(obj['coords']) # Convert set to list for iteration

        # Rule A: Bottom Line Removal Check
        is_bottom_row = (obj['min_row'] == height - 1) and (obj['max_row'] == height - 1)
        is_1x5_line = (obj['height'] == 1 and obj['width'] == 5 and obj['num_pixels'] == 5)

        if is_1x5_line and is_bottom_row:
            # Action A: Change object pixels to background color
            for r, c in obj_coords_list:
                output_array[r, c] = background_color
            continue # Move to the next object

        # Rule B: Plus Sign Color Change Check
        if is_plus_sign(obj):
             # Check if this specific object color needs changing
            if obj_color in [9, 6, 3]: # Maroon, Magenta, Green
                # Action B: Change the 5 pixels to Gray (5)
                for r, c in obj_coords_list:
                    output_array[r, c] = 5
            # Else: If it's a plus sign but not one of the target colors, do nothing (Rule C implicitly applied)
            continue # Move to the next object

        # Rule C: No Change (Implicit)
        # If neither Rule A nor Rule B applied, the object pixels remain
        # as they were in the initial copy of the input grid.

    # 5. Return Result
    # Convert the final numpy array back to a list of lists
    output_grid = output_array.tolist()
    return output_grid