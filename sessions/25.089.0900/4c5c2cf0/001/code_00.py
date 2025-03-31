import numpy as np
from collections import deque

"""
Identify the two distinct non-white objects in the input grid.
Determine which object is positioned entirely above the other. This upper object is the 'mirror'. The lower object is the 'mirrored object'.
Calculate the reflection axis based on the minimum and maximum row indices of the mirror object: axis_sum = min_row_mirror + max_row_mirror.
Create the output grid by copying the input grid initially.
Remove the original pixels of the mirrored object from the output grid (set them to the background color 0).
For each pixel (r, c) of the original mirrored object, calculate its reflected row position: r_new = axis_sum - r.
Place the color of the mirrored object at the new position (r_new, c) in the output grid.
The object identified as the mirror remains unchanged in its original position.
"""

def find_objects(grid, background_color=0):
    """
    Finds distinct contiguous objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.
        background_color (int): The value representing the background.

    Returns:
        list: A list of tuples, where each tuple is (color, set_of_coords).
              Returns None if not exactly two objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    
                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({'color': color, 'coords': obj_coords})

    # Expect exactly two objects for this task's logic
    if len(objects) == 2:
        return objects
    else:
        # Handle cases where the assumption of two objects isn't met
        # For this specific task, we expect exactly two. 
        # If not, the premise of the transformation is broken.
        # Returning None or raising an error might be appropriate depending on context.
        # For robustness in a broader system, more complex handling might be needed.
        print(f"Warning: Found {len(objects)} objects, expected 2.")
        return None # Indicate failure condition

def get_bounding_box(coords):
    """
    Calculates the min/max row/col for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col).
               Returns None if coords is empty.
    """
    if not coords:
        return None
    
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Transforms the input grid by reflecting one object vertically across the
    horizontal axis defined by the other object. The upper object acts as the
    mirror for the lower object.

    Args:
        input_grid (np.array): The input 2D numpy array.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    
    # Find the two objects in the input grid
    objects = find_objects(input_grid)
    if objects is None:
        # If exactly two objects weren't found, return the input unchanged
        # or handle as an error, depending on desired behavior.
        print("Error: Did not find exactly two objects. Returning input.")
        return input_grid.copy() 

    obj1 = objects[0]
    obj2 = objects[1]

    # Get bounding boxes to determine which object is above the other
    bb1 = get_bounding_box(obj1['coords'])
    bb2 = get_bounding_box(obj2['coords'])

    if bb1 is None or bb2 is None:
        print("Error: Could not determine bounding boxes. Returning input.")
        return input_grid.copy()

    min_r1, _, max_r1, _ = bb1
    min_r2, _, max_r2, _ = bb2

    mirror_object = None
    mirrored_object = None

    # Determine which object is the mirror (upper) and which is mirrored (lower)
    if max_r1 < min_r2: # Object 1 is entirely above Object 2
        mirror_object = obj1
        mirrored_object = obj2
        mirror_min_r, _, mirror_max_r, _ = bb1
    elif max_r2 < min_r1: # Object 2 is entirely above Object 1
        mirror_object = obj2
        mirrored_object = obj1
        mirror_min_r, _, mirror_max_r, _ = bb2
    else:
        # This case (objects overlapping vertically or side-by-side) 
        # is not covered by the training examples.
        # Returning input or raising error.
        print("Error: Objects are not clearly one above the other. Returning input.")
        return input_grid.copy()

    # Calculate the reflection axis sum
    axis_sum = mirror_min_r + mirror_max_r

    # Initialize the output grid as a copy of the input
    output_grid = input_grid.copy()

    # Erase the original mirrored object from the output grid
    for r, c in mirrored_object['coords']:
        output_grid[r, c] = 0 # Set to background color

    # Draw the reflected object
    mirrored_color = mirrored_object['color']
    for r, c in mirrored_object['coords']:
        # Calculate the new row for reflection
        r_new = axis_sum - r
        
        # Check bounds before drawing
        if 0 <= r_new < output_grid.shape[0]:
            output_grid[r_new, c] = mirrored_color
        else:
            # Handle cases where reflection goes out of bounds if necessary
            print(f"Warning: Reflected pixel ({r_new}, {c}) out of bounds.")


    return output_grid