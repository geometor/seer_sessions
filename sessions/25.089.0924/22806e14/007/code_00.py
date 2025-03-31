import numpy as np
from collections import deque

"""
Transforms the input grid based on the following rules:

1.  Identifies the background color (assumed to be 7) and the two unique non-background colors (Color A, Color B).
2.  Finds all connected objects for both Color A and Color B.
3.  For each object, determines its bounding box and calculates its height and width.
4.  Counts how many objects of Color A have both odd height and odd width (`countA`).
5.  Counts how many objects of Color B have both odd height and odd width (`countB`).
6.  Determines a 'target_color' and a 'replacement_color' based on the comparison of `countA` and `countB`:
    - If `countA > countB`, target = A, replacement = B.
    - If `countB > countA`, target = B, replacement = A.
    - If `countA == countB`, target = max(A, B), replacement = min(A, B).
7.  Modifies an output grid (initially a copy of the input):
    - For each object of the `target_color`, if its bounding box has odd height and odd width, its exact center pixel is changed to the `replacement_color`.
    - All other pixels retain their original color from the input grid.
8.  Returns the modified grid.
"""

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid using BFS.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of the pixels belonging to one object. Returns an empty list
              if no objects of the specified color are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS from an unvisited pixel of the target color
            if grid[r, c] == color and not visited[r, c]:
                obj_pixels = set()
                queue = deque([(r, c)])
                visited[r, c] = True
                while queue:
                    row, col = queue.popleft()
                    obj_pixels.add((row, col))
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor is the same color and unvisited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            queue.append((nr, nc))
                # Add the found object's pixels to the list if it's not empty
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def get_bounding_box(obj_pixels):
    """
    Calculates the bounding box for a set of object pixels.

    Args:
        obj_pixels (set): A set of (row, col) tuples representing an object.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if the set is empty.
    """
    if not obj_pixels:
        return None
    # Find the min/max row and column from the pixel coordinates
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    return min(rows), min(cols), max(rows), max(cols)

def get_dimensions(bounding_box):
    """
    Calculates the height and width from a bounding box tuple.

    Args:
        bounding_box (tuple): (min_row, min_col, max_row, max_col).

    Returns:
        tuple: (height, width). Returns (0, 0) if bounding_box is None.
    """
    if bounding_box is None:
        return 0, 0
    min_r, min_c, max_r, max_c = bounding_box
    # Height and width are inclusive ranges
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def is_odd_dimension(dims):
    """
    Checks if both height and width are positive odd numbers.

    Args:
        dims (tuple): (height, width).

    Returns:
        bool: True if both height and width are positive and odd, False otherwise.
    """
    height, width = dims
    # Dimensions must be positive and odd
    return height > 0 and width > 0 and height % 2 != 0 and width % 2 != 0

def get_center(bounding_box):
    """
    Calculates the center coordinates for a bounding box.
    Assumes the dimensions are odd when called in the main logic.

    Args:
        bounding_box (tuple): (min_row, min_col, max_row, max_col).

    Returns:
        tuple: (center_row, center_col).
    """
    min_r, min_c, max_r, max_c = bounding_box
    height, width = get_dimensions(bounding_box)
    # Integer division finds the middle index for odd dimensions
    center_r = min_r + height // 2
    center_c = min_c + width // 2
    return center_r, center_c


def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    
    # Define background color (assumed to be 7 based on examples)
    bg_color = 7

    # Identify the unique colors present and filter out the background color
    unique_colors = np.unique(input_grid_np)
    non_bg_colors = [c for c in unique_colors if c != bg_color]
    
    # Check if exactly two non-background colors are present, as required by the rule
    if len(non_bg_colors) != 2:
        # If not, return the original grid (transformation is undefined)
        return input_grid 

    color_a, color_b = non_bg_colors[0], non_bg_colors[1]

    # --- Analyze Objects for Each Color ---
    # Store properties: (set of pixels, has odd/odd dimensions, bounding box)
    objects_a_props = [] 
    objects_a = find_objects(input_grid_np, color_a)
    count_odd_a = 0
    for obj_pixels in objects_a:
        bbox = get_bounding_box(obj_pixels)
        dims = get_dimensions(bbox)
        is_odd = is_odd_dimension(dims)
        objects_a_props.append((obj_pixels, is_odd, bbox))
        if is_odd:
            count_odd_a += 1 # Increment count if dimensions are odd/odd

    objects_b_props = []
    objects_b = find_objects(input_grid_np, color_b)
    count_odd_b = 0
    for obj_pixels in objects_b:
        bbox = get_bounding_box(obj_pixels)
        dims = get_dimensions(bbox)
        is_odd = is_odd_dimension(dims)
        objects_b_props.append((obj_pixels, is_odd, bbox))
        if is_odd:
            count_odd_b += 1 # Increment count if dimensions are odd/odd

    # --- Determine Target and Replacement Colors based on counts ---
    if count_odd_a > count_odd_b:
        target_color = color_a
        replacement_color = color_b
        target_objects_props = objects_a_props # Assign properties list for the target color
    elif count_odd_b > count_odd_a:
        target_color = color_b
        replacement_color = color_a
        target_objects_props = objects_b_props # Assign properties list for the target color
    else: # Counts are equal, use numerical value as tie-breaker
        target_color = max(color_a, color_b)
        replacement_color = min(color_a, color_b)
        # Assign the correct properties list based on the tie-breaker result
        if target_color == color_a:
             target_objects_props = objects_a_props
        else:
             target_objects_props = objects_b_props

    # --- Apply Transformation: Modify Center Pixel ---
    # Iterate through the properties of objects belonging to the target color
    for obj_pixels, is_odd, bbox in target_objects_props:
        # Check if the object has odd/odd dimensions
        if is_odd:
            # Calculate the center coordinates of its bounding box
            center_r, center_c = get_center(bbox)
            # Modify the pixel at the center coordinates in the output grid
            # No need to check original color, as we only modify target objects
            # and the output grid starts as a copy.
            output_grid[center_r, center_c] = replacement_color
            
    # Convert the final numpy array back to a list of lists for the expected format
    return output_grid.tolist()