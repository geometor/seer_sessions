import numpy as np
from collections import deque

"""
Transformation Rule Description:

1. Identify all contiguous blocks (objects) of Red (2), White (0), and Blue (1) pixels in the input grid. For each object, record its color, the coordinates of its pixels, and its dimensions (height and width).
2. Initialize the output grid as a copy of the input grid.
3. Process White Objects: For every White object found, change the color of all its constituent pixels in the output grid to Blue (1).
4. Process Red Objects: For every Red object found:
    a. Determine its dimensions (height, width).
    b. Count how many Blue objects share these exact dimensions.
    c. If exactly one Blue object matches the dimensions:
        i. Locate that unique matching Blue object.
        ii. Change the color of all its constituent pixels in the output grid to White (0).
    d. Otherwise (if zero or more than one Blue object matches the dimensions):
        i. Change the color of all the constituent pixels of the *current Red object* in the output grid to White (0).
5. Return the modified output grid. Green (3) pixels and Blue pixels not involved in the Red object matching process remain unchanged (unless they originated from White objects).
"""

def find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'coords' (list of (r, c) tuples),
              'height', and 'width'.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                # Start BFS to find the extent of the object
                q = deque([(r, c)])
                visited[r, c] = True
                object_coords = [(r, c)]
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    curr_r, curr_c = q.popleft()
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            object_coords.append((nr, nc))

                obj_height = max_r - min_r + 1
                obj_width = max_c - min_c + 1
                objects.append({
                    'color': target_color,
                    'coords': object_coords,
                    'height': obj_height,
                    'width': obj_width
                })
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    - White objects become Blue.
    - If a Red object has the same dimensions as exactly one Blue object, that Blue object becomes White.
    - Otherwise, the Red object itself becomes White.
    """
    # Convert input_grid list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy
    output_grid = np.copy(input_np)

    # Find all objects of relevant colors
    white_objects = find_objects(input_np, 0) # 0: White
    red_objects = find_objects(input_np, 2)   # 2: Red
    blue_objects = find_objects(input_np, 1)  # 1: Blue

    # Process White objects: Change White to Blue
    for obj in white_objects:
        for r, c in obj['coords']:
            output_grid[r, c] = 1 # Change to Blue

    # Process Red objects: Conditional change based on Blue object dimensions
    for red_obj in red_objects:
        red_h, red_w = red_obj['height'], red_obj['width']
        
        # Find Blue objects with matching dimensions
        matching_blue_objects = []
        for blue_obj in blue_objects:
            if blue_obj['height'] == red_h and blue_obj['width'] == red_w:
                matching_blue_objects.append(blue_obj)
        
        # Check condition: Exactly one matching Blue object
        if len(matching_blue_objects) == 1:
            # Change the unique matching Blue object to White
            target_blue_obj = matching_blue_objects[0]
            for r, c in target_blue_obj['coords']:
                # Important: Check if this blue pixel wasn't originally white
                # If it was originally white, it should end up blue as per step 1
                # This check prevents overwriting the white->blue change if the red trigger targets it.
                # However, the rules imply the red trigger takes precedence if there's a match.
                # So, if a white block became blue, and a red block matches its dimensions, it becomes white again.
                 output_grid[r, c] = 0 # Change to White
        else:
            # Change the Red object itself to White
            for r, c in red_obj['coords']:
                output_grid[r, c] = 0 # Change to White

    # Convert back to list of lists if necessary for the ARC framework
    return output_grid.tolist()