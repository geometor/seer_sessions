import numpy as np
from collections import deque

"""
Identifies exactly three distinct gray (5) objects in the input grid.
These objects are assumed to be either horizontal lines (height=1, width>1) or vertical lines (width=1, height>1).
The objects are sorted based on their top-leftmost pixel coordinate (row-major order).
The first object (Obj1) is always recolored blue (1).
The second (Obj2) and third (Obj3) objects are recolored based on their shapes:
- If both Obj2 and Obj3 are horizontal lines, Obj2 becomes red (2) and Obj3 becomes yellow (4).
- Otherwise (any other combination of shapes), Obj2 becomes yellow (4) and Obj3 becomes red (2).
The background and any other pixels remain unchanged.
"""

def find_objects(grid, color):
    """
    Finds all connected components of a given color in the grid using BFS.
    Connectivity is based on 4 neighbors (up, down, left, right).

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) coordinates
              of the pixels belonging to one object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            # If the cell has the target color and hasn't been visited yet
            if grid[r, c] == color and (r, c) not in visited:
                # Start a new object search (BFS)
                current_object_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_coords.add((curr_r, curr_c))
                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check if neighbor is within bounds, has the target color, and hasn't been visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                # Add the found object's coordinates to the list if it's not empty
                if current_object_coords:
                    objects.append(current_object_coords)
    return objects

def get_object_properties(obj_coords):
    """
    Calculates properties (top-left coord, height, width) for an object.

    Args:
        obj_coords (set): A set of (row, col) coordinates for the object.

    Returns:
        dict: A dictionary containing 'top_left' (tuple), 'height' (int),
              and 'width' (int). Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None
    
    # Extract all row and column indices
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    
    # Find bounding box limits
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    
    # Calculate height and width
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    # Determine the top-left coordinate: minimum row, then minimum column within that row
    min_row_coords = [(r,c) for r,c in obj_coords if r == min_row]
    top_left_col = min(c for r,c in min_row_coords)
    top_left = (min_row, top_left_col)

    return {'top_left': top_left, 'height': height, 'width': width}

def transform(input_grid):
    """
    Transforms the input grid based on the identified rules.

    Args:
        input_grid (np.array): The input 2D grid.

    Returns:
        np.array: The transformed 2D grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    
    # 1. Identify all distinct groups of connected gray (5) pixels
    gray_objects_coords = find_objects(output_grid, 5)

    # 2. Calculate properties for each object
    object_data = []
    for coords in gray_objects_coords:
        if not coords: continue # Skip if coordinates set is empty
        props = get_object_properties(coords)
        if props:
             object_data.append({'coords': coords, 'properties': props})

    # 3. Sort objects based on top-left coordinates (row-major)
    object_data.sort(key=lambda obj: obj['properties']['top_left'])

    # Check if exactly 3 objects were found, as assumed from examples
    if len(object_data) != 3:
        # If not 3 objects, return the original grid or handle error appropriately.
        # Based on the examples, the rule requires exactly 3 objects.
        print(f"Warning/Error: Expected 3 gray objects, but found {len(object_data)}. Returning input grid.")
        return input_grid 

    # Assign sorted objects
    obj1, obj2, obj3 = object_data[0], object_data[1], object_data[2]

    # 4. Determine the shape (H-line or V-line) for each object
    def get_shape(props):
        h, w = props['height'], props['width']
        if h == 1 and w > 1: return "H-line"
        if w == 1 and h > 1: return "V-line"
        # Consider single pixel objects or other shapes if necessary
        # For this problem, based on examples, only H/V lines > 1 size are expected
        return "Other" 

    shape1 = get_shape(obj1['properties']) # Not strictly needed by rule, but good for consistency
    shape2 = get_shape(obj2['properties'])
    shape3 = get_shape(obj3['properties'])
    
    # 5. Recolor Object 1 to blue (1)
    for r, c in obj1['coords']:
        output_grid[r, c] = 1

    # 6. Recolor Object 2 and Object 3 based on their shapes
    if shape2 == "H-line" and shape3 == "H-line":
        # If Obj2 is H-line AND Obj3 is H-line:
        # Recolor Obj2 to red (2)
        for r, c in obj2['coords']:
            output_grid[r, c] = 2
        # Recolor Obj3 to yellow (4)
        for r, c in obj3['coords']:
            output_grid[r, c] = 4
    else:
        # Else (any other combination):
        # Recolor Obj2 to yellow (4)
        for r, c in obj2['coords']:
            output_grid[r, c] = 4
        # Recolor Obj3 to red (2)
        for r, c in obj3['coords']:
            output_grid[r, c] = 2

    # 7. Return the modified grid
    return output_grid