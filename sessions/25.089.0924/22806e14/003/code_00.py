import numpy as np
from collections import deque

"""
Identifies the background color (assumed to be 7) and the two non-background colors (A and B) in the input grid.
Finds all connected objects for both Color A and Color B.
For each color, counts how many of its objects have a bounding box with both odd height and odd width.
Determines a 'target_color' and a 'replacement_color' based on these counts:
- If one color has more odd-dimensioned objects, it becomes the target_color, and the other becomes the replacement_color.
- If the counts are equal, the color with the higher numerical value becomes the target_color, and the lower becomes the replacement_color.
Creates an output grid initially as a copy of the input grid.
Processes the replacement_color: All pixels belonging to any object of the replacement_color in the input are changed to the background color in the output grid.
Processes the target_color: For each object of the target_color in the input:
    - Calculates its bounding box dimensions (height, width).
    - If both height and width are odd:
        - If the object is larger than 1x1 (height > 1 or width > 1):
            - Finds the center pixel of the bounding box.
            - Changes the color of this center pixel in the output grid to the replacement_color.
        - If the object is exactly 1x1:
            - The object remains unchanged in the output grid.
    - If either height or width is even, the object remains unchanged.
Returns the modified output grid.
"""

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid using BFS.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of the pixels belonging to one object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
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
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            queue.append((nr, nc))
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def get_bounding_box(obj_pixels):
    """
    Calculates the bounding box for a set of object pixels.

    Args:
        obj_pixels (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if empty.
    """
    if not obj_pixels:
        return None
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    return min(rows), min(cols), max(rows), max(cols)

def get_dimensions(bounding_box):
    """
    Calculates the height and width from a bounding box.

    Args:
        bounding_box (tuple): (min_row, min_col, max_row, max_col).

    Returns:
        tuple: (height, width).
    """
    if bounding_box is None:
        return 0, 0
    min_r, min_c, max_r, max_c = bounding_box
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def is_odd_dimension(dims):
    """
    Checks if both height and width are odd.

    Args:
        dims (tuple): (height, width).

    Returns:
        bool: True if both are odd, False otherwise.
    """
    height, width = dims
    return height > 0 and width > 0 and height % 2 != 0 and width % 2 != 0

def get_center(bounding_box):
    """
    Calculates the center coordinates for an odd-dimensioned bounding box.
    Assumes the dimensions are odd.

    Args:
        bounding_box (tuple): (min_row, min_col, max_row, max_col).

    Returns:
        tuple: (center_row, center_col).
    """
    min_r, min_c, max_r, max_c = bounding_box
    height, width = get_dimensions(bounding_box)
    center_r = min_r + height // 2
    center_c = min_c + width // 2
    return center_r, center_c


def transform(input_grid):
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    
    # Define background color (assumed from examples)
    bg_color = 7

    # Identify the two non-background colors
    unique_colors = np.unique(input_grid_np)
    non_bg_colors = [c for c in unique_colors if c != bg_color]
    
    # Expect exactly two non-background colors based on examples
    if len(non_bg_colors) != 2:
        # If not exactly two, return the original grid as per problem constraints/examples
        return input_grid 

    color_a, color_b = non_bg_colors[0], non_bg_colors[1]

    # Find all objects for each non-background color
    objects_a = find_objects(input_grid_np, color_a)
    objects_b = find_objects(input_grid_np, color_b)

    # Count objects with odd height AND odd width for each color
    count_odd_a = 0
    for obj in objects_a:
        bbox = get_bounding_box(obj)
        dims = get_dimensions(bbox)
        if is_odd_dimension(dims):
            count_odd_a += 1

    count_odd_b = 0
    for obj in objects_b:
        bbox = get_bounding_box(obj)
        dims = get_dimensions(bbox)
        if is_odd_dimension(dims):
            count_odd_b += 1

    # Determine target and replacement colors based on counts
    if count_odd_a > count_odd_b:
        target_color = color_a
        replacement_color = color_b
    elif count_odd_b > count_odd_a:
        target_color = color_b
        replacement_color = color_a
    else: # Counts are equal, use numerical value as tie-breaker
        target_color = max(color_a, color_b)
        replacement_color = min(color_a, color_b)
        
    # Apply Rule 1: Remove all objects of the replacement_color
    # Find all pixels belonging to replacement_color objects and set them to bg_color
    replacement_objects = objects_a if replacement_color == color_a else objects_b
    for obj in replacement_objects:
        for r, c in obj:
            output_grid[r, c] = bg_color

    # Apply Rule 2: Modify target_color objects based on dimensions
    target_objects = objects_a if target_color == color_a else objects_b
    for obj in target_objects:
        bbox = get_bounding_box(obj)
        dims = get_dimensions(bbox)
        
        # Check if dimensions are odd
        if is_odd_dimension(dims):
            height, width = dims
            # Only modify center if object is larger than 1x1
            if height > 1 or width > 1:
                center_r, center_c = get_center(bbox)
                # Check if the center pixel wasn't part of a replacement object that was removed
                # (This check might be redundant if target/replacement objects don't overlap, but safe to include)
                if input_grid_np[center_r, center_c] == target_color:
                     output_grid[center_r, center_c] = replacement_color
            # If it's 1x1 (h=1, w=1), do nothing (leave it as target_color)
        # If dimensions are not both odd, do nothing (leave object as is)
            
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()