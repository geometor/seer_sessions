import numpy as np
from collections import deque

"""
The transformation identifies a horizontal separator line (blue=1) dividing the grid into an upper 'key area' and a lower 'work area'.
It finds distinct colored shapes (key patterns) in the key area, recording their shapes (relative pixel coordinates) and colors.
It then finds all gray (5) shapes in the work area.
For each gray shape in the work area, if its shape exactly matches the shape of a key pattern from the key area, the gray pixels are replaced in the output grid with the color of the matching key pattern.
All other elements (key area, separator line, background pixels in work area, non-matching gray shapes) remain unchanged.
"""

def find_objects(grid, target_colors, bounds=None):
    """
    Finds all contiguous objects of specified colors within given bounds using Breadth-First Search.

    Args:
        grid (np.ndarray): The input grid.
        target_colors (list or set): The color(s) of the objects to find.
        bounds (tuple, optional): (min_row, max_row, min_col, max_col) defining the search area (exclusive max).
                                  Defaults to the whole grid if None.

    Returns:
        list: A list of objects. Each object is a tuple: (color, set_of_coordinates).
              Coordinates are (row, col) tuples relative to the original grid.
    """
    rows, cols = grid.shape
    if bounds:
        min_row, max_row, min_col, max_col = bounds
        # Ensure bounds are within grid dimensions
        min_row = max(0, min_row)
        max_row = min(rows, max_row)
        min_col = max(0, min_col)
        max_col = min(cols, max_col)
    else:
        min_row, max_row = 0, rows
        min_col, max_col = 0, cols

    # Visited array specific to the bounds to avoid redundant checks outside
    visited = np.zeros((rows, cols), dtype=bool) 
    objects = []

    for r in range(min_row, max_row):
        for c in range(min_col, max_col):
            # Check if the current cell is a target color and hasn't been visited yet
            if not visited[r, c] and grid[r, c] in target_colors:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True # Mark the starting cell as visited

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if the neighbor is within the defined bounds
                        if min_row <= nr < max_row and min_col <= nc < max_col:
                            # Check if the neighbor has the same color and hasn't been visited
                            if not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True # Mark neighbor as visited
                                q.append((nr, nc)) # Add neighbor to the queue

                # After BFS completes for an object, if coordinates were found, store it
                if obj_coords:
                    objects.append((color, obj_coords))

    return objects

def get_object_shape(obj_coords):
    """
    Calculates the normalized shape of an object based on its coordinates.
    The shape is represented by coordinates relative to the top-left corner of the object's bounding box.

    Args:
        obj_coords (set): A set of (row, col) coordinates representing the object.

    Returns:
        tuple: A tuple of sorted relative coordinates ((r1, c1), (r2, c2), ...),
               representing the shape normalized to (0,0).
               Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None

    # Find the minimum row and column to establish the top-left reference point
    min_r = min(r for r, c in obj_coords)
    min_c = min(c for r, c in obj_coords)

    # Calculate relative coordinates by subtracting the min row and col
    # Sort the coordinates to ensure a consistent representation regardless of traversal order
    relative_coords = sorted([(r - min_r, c - min_c) for r, c in obj_coords])

    # Return the sorted relative coordinates as a tuple (making it hashable)
    return tuple(relative_coords)

def transform(input_grid):
    """
    Transforms the input grid by replacing gray shapes in the lower part
    with colors based on matching shapes found in the upper part.
    """
    # Convert input to numpy array for efficient processing
    input_grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input structure
    output_grid_np = np.copy(input_grid_np)
    rows, cols = input_grid_np.shape

    # 1. Find the separator line (assuming blue=1 and full width)
    separator_row = -1
    for r in range(rows):
        # Check if the entire row consists of the separator color (blue=1)
        if np.all(input_grid_np[r, :] == 1):
            separator_row = r
            break

    # If no separator line is found, return the original grid (or handle as error)
    if separator_row == -1:
        # This case might indicate an unexpected input format
        # print("Warning: Separator line (blue=1) not found.")
        return input_grid # Return original list of lists

    # 2. Define key and work area boundaries
    # Key area is above the separator line
    key_area_bounds = (0, separator_row, 0, cols)
    # Work area is below the separator line
    work_area_bounds = (separator_row + 1, rows, 0, cols)

    # 3. Find key patterns (shapes and colors) in the key area
    # Define colors to look for in the key area (all except background 0 and separator 1)
    key_colors = set(range(10)) - {0, 1}
    key_objects = find_objects(input_grid_np, key_colors, key_area_bounds)

    # Store key patterns in a dictionary: shape -> color
    key_patterns = {}
    for color, coords in key_objects:
        shape = get_object_shape(coords)
        # Ensure shape is valid before adding to dictionary
        if shape:
            # If duplicate shapes exist, the last one encountered will overwrite previous ones.
            # This seems unlikely based on ARC task design but is handled.
            key_patterns[shape] = color

    # 4. Find gray (5) objects in the work area
    # Define the target color for the work area (gray=5)
    gray_color = {5}
    gray_objects = find_objects(input_grid_np, gray_color, work_area_bounds)

    # 5. Process gray objects: match shapes and replace colors in the output grid
    for _, gray_coords in gray_objects:
        # Calculate the normalized shape of the gray object
        gray_shape = get_object_shape(gray_coords)

        # Check if the shape is valid and if it exists in the key patterns dictionary
        if gray_shape and gray_shape in key_patterns:
            # Get the color associated with the matching key pattern
            replacement_color = key_patterns[gray_shape]
            # Update the output grid: replace gray pixels with the key pattern's color
            for r, c in gray_coords:
                # Double-check bounds, although coordinates should be within grid
                if 0 <= r < rows and 0 <= c < cols:
                    output_grid_np[r, c] = replacement_color

    # Convert the modified numpy array back to a list of lists for the final output
    return output_grid_np.tolist()