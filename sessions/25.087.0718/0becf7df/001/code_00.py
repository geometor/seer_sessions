import numpy as np
from collections import deque

"""
Identify two distinct non-white objects in the input grid. One object's bounding 
box includes the top-left corner (0,0) (source object), and the other does not 
(target object). Extract the four unique non-white colors from the source object 
and sort them numerically: [c1, c2, c3, c4]. Determine the color swapping rule 
based on whether c1 + c4 == c2 + c3. If true, swaps are (c1, c4) and (c2, c3). 
If false, swaps are (c1, c3) and (c2, c4). Apply these swaps to the pixels 
within the target object only. The source object and background remain unchanged.
"""

def find_objects(grid):
    """
    Finds contiguous regions of non-white pixels (objects) in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of sets, where each set contains the (row, col) coordinates
              of the pixels belonging to one object.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS from an unvisited non-white pixel
            if grid[r, c] != 0 and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds and if neighbor is part of the same object
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] != 0 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                obj_coords.add((nr, nc))
                                q.append((nr, nc))
                objects.append(obj_coords)
    return objects

def get_bounding_box(object_coords):
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of coordinates.

    Args:
        object_coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) or None if coords is empty.
    """
    if not object_coords:
        return None
    rows = [r for r, c in object_coords]
    cols = [c for r, c in object_coords]
    return min(rows), min(cols), max(rows), max(cols)

def get_unique_colors(grid, object_coords):
    """
    Extracts unique non-white colors from specified coordinates within the grid.

    Args:
        grid (np.ndarray): The grid.
        object_coords (set): A set of (row, col) coordinates for the object.

    Returns:
        list: Sorted list of unique non-white colors.
    """
    colors = set()
    for r, c in object_coords:
        color = grid[r, c]
        if color != 0:
            colors.add(color)
    return sorted(list(colors))

def transform(input_grid):
    """
    Applies the color swapping transformation based on the rules derived from examples.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Initialize output as a copy of input

    # 1. Find all distinct non-white objects
    objects = find_objects(grid)

    if len(objects) != 2:
        # Assumption based on examples: there are always exactly two objects
        # If not, return the input unchanged or handle error appropriately
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning input.")
        return input_grid 

    # 2. & 3. Identify source and target objects
    source_object_coords = None
    target_object_coords = None

    for obj_coords in objects:
        bbox = get_bounding_box(obj_coords)
        if bbox is None: continue # Should not happen if find_objects works correctly
        min_r, min_c, _, _ = bbox
        # Check if the bounding box includes (0, 0)
        if min_r == 0 and min_c == 0:
            # Check if (0,0) itself is part of the object, not just the bbox
            if (0, 0) in obj_coords:
                 source_object_coords = obj_coords
            else: 
                # If (0,0) is not in the object but in the bbox, search further
                # Check if any coordinate in obj_coords is (0,0)
                is_source = False
                for r_coord, c_coord in obj_coords:
                    if r_coord == 0 and c_coord == 0:
                        is_source = True
                        break
                if is_source:
                    source_object_coords = obj_coords
                else:
                     target_object_coords = obj_coords # If not source, must be target
        else:
            target_object_coords = obj_coords

    if source_object_coords is None or target_object_coords is None:
        print("Warning: Could not identify both source and target objects. Returning input.")
        # Fallback: Try identifying based purely on bounding box including (0,0)
        # This might be needed if the (0,0) pixel itself is background
        source_object_coords = None
        target_object_coords = None
        for obj_coords in objects:
            bbox = get_bounding_box(obj_coords)
            if bbox is None: continue
            min_r, min_c, _, _ = bbox
            if min_r == 0 and min_c == 0:
                source_object_coords = obj_coords
            else:
                target_object_coords = obj_coords
        if source_object_coords is None or target_object_coords is None:
             print("Warning: Still could not identify both source and target objects. Returning input.")
             return input_grid


    # 4. & 5. Get and sort unique colors from the source object
    source_colors = get_unique_colors(grid, source_object_coords)

    if len(source_colors) != 4:
        # Assumption based on examples: source object always has 4 unique non-white colors
        print(f"Warning: Expected 4 unique colors in source object, found {len(source_colors)}. Returning input.")
        return input_grid

    c1, c2, c3, c4 = source_colors

    # 6. Determine swap pairs
    swap_map = {}
    if c1 + c4 == c2 + c3:
        # Pairs are (c1, c4) and (c2, c3)
        swap_map[c1] = c4
        swap_map[c4] = c1
        swap_map[c2] = c3
        swap_map[c3] = c2
    else:
        # Pairs are (c1, c3) and (c2, c4)
        swap_map[c1] = c3
        swap_map[c3] = c1
        swap_map[c2] = c4
        swap_map[c4] = c2

    # 7. & 8. Apply swaps to the target object in the output grid
    for r, c in target_object_coords:
        current_color = grid[r, c]
        if current_color in swap_map:
            output_grid[r, c] = swap_map[current_color]
        # If color is not in swap_map (e.g., it's 0, or not one of the 4 source colors),
        # it remains unchanged because output_grid started as a copy.

    # 9. Source object and background are already correct in the copied grid.

    # 10. Return the final grid
    return output_grid.tolist() # Convert back to list of lists if needed
