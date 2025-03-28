```python
"""
Identify all unique colors in the input grid, excluding white (0) and gray (5).
Record the first appearance (top-to-bottom, left-to-right) coordinate for each relevant color.
Count the number of unique relevant colors, N.
Find all connected objects formed by these relevant colors.
Determine the overall orientation: 'Vertical' if all objects have height >= width, 'Horizontal' otherwise.
Create an N x N output grid.
Sort the relevant colors based on their first appearance coordinate:
- If orientation is 'Horizontal', sort primarily by row, secondarily by column.
- If orientation is 'Vertical', sort primarily by column, secondarily by row.
Populate the output grid:
- If orientation is 'Horizontal', fill the i-th row with the i-th sorted color.
- If orientation is 'Vertical', fill the j-th column with the j-th sorted color.
"""

import numpy as np
from collections import deque

def find_objects(grid, colors_to_find):
    """
    Finds all connected components (objects) of the specified colors in the grid.
    Uses 4-directional connectivity (von Neumann neighborhood).

    Args:
        grid (np.array): The input grid.
        colors_to_find (set): A set of integer colors to search for.

    Returns:
        list: A list of objects, where each object is a set of (row, col) tuples.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Check if the current cell contains a relevant color and hasn't been visited
            if color in colors_to_find and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)]) # Use deque for efficient BFS queue
                visited[r, c] = True

                # Breadth-First Search to find all connected cells of the same color
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, visit status, and color match
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Add the found object (set of coordinates) to the list if not empty
                if obj_coords:
                    objects.append(obj_coords)

    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box of an object represented by a set of coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if obj_coords is empty.
    """
    if not obj_coords:
        return None

    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]

    return min(rows), min(cols), max(rows), max(cols)

def get_object_dimensions(obj_coords):
    """
    Calculates the height and width of an object based on its bounding box.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object.

    Returns:
        tuple: (height, width). Returns (0, 0) if obj_coords is empty.
    """
    if not obj_coords:
        return 0, 0

    bbox = get_bounding_box(obj_coords)
    if bbox is None:
        return 0, 0

    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height, width

def transform(input_grid):
    """
    Transforms the input grid based on identified colors, their order,
    object orientation, and constructs the output grid accordingly.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # 1. Identify relevant colors (non-white, non-gray) and find their first appearance
    relevant_colors_first_pos = {} # color -> (min_row, min_col)
    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Ignore background (0) and gray (5)
            if color != 0 and color != 5:
                # Record the first position (top-leftmost) where each relevant color appears
                if color not in relevant_colors_first_pos:
                    relevant_colors_first_pos[color] = (r, c)

    # If no relevant colors are found, return an empty grid or handle appropriately.
    # Based on examples, N should be >= 1. Returning empty list if no colors found.
    if not relevant_colors_first_pos:
        return []

    # 2. Count relevant colors (N)
    n = len(relevant_colors_first_pos) # Size of the output grid side

    # 3. Find all objects formed by the relevant colors
    relevant_color_set = set(relevant_colors_first_pos.keys())
    all_objects = find_objects(grid, relevant_color_set)

    # 4. Determine the overall orientation
    # Assume vertical orientation unless a horizontally oriented object is found
    is_vertical_orientation = True
    if not all_objects:
         # If colors exist but form no connected objects (e.g., single pixels),
         # treat them as 1x1 objects. Since height >= width (1 >= 1), default remains Vertical.
         # However, let's reconsider this based on example failure. If isolated pixels, treat as horizontal?
         # Example 1 has clear vertical objects. Examples 2 & 3 have clear horizontal ones.
         # Let's stick to the rule: if ANY object has height < width, it's Horizontal.
         pass # Default is vertical, only change if condition met below

    for obj_coords in all_objects:
        obj_height, obj_width = get_object_dimensions(obj_coords)
        # If any object is wider than it is tall, the overall orientation is Horizontal
        if obj_height < obj_width:
            is_vertical_orientation = False
            break # No need to check further

    # 5. Sort the relevant colors based on orientation and first appearance
    if is_vertical_orientation:
        # Sort by column first, then row for Vertical orientation
        sorted_colors = sorted(relevant_colors_first_pos.keys(),
                               key=lambda color: (relevant_colors_first_pos[color][1], relevant_colors_first_pos[color][0]))
    else:
        # Sort by row first, then column for Horizontal orientation
        sorted_colors = sorted(relevant_colors_first_pos.keys(),
                               key=lambda color: relevant_colors_first_pos[color]) # default sort by (row, col) tuple


    # 6. Construct the N x N output grid, initialized to white (0)
    output_grid = np.zeros((n, n), dtype=int)

    # 7. Populate the output grid based on the determined orientation and sorted colors
    for idx, color in enumerate(sorted_colors):
        if is_vertical_orientation:
            # Fill the entire column 'idx' with the current color
            output_grid[:, idx] = color
        else:
            # Fill the entire row 'idx' with the current color
            output_grid[idx, :] = color

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()
```