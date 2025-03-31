import numpy as np
from typing import List, Tuple, Set

"""
Recolors distinct gray (5) objects in an input grid based on their scan order (top-to-bottom, left-to-right) and relative vertical positions.

1. Finds all connected components (objects) of gray pixels (color 5), considering 8-way adjacency (including diagonals).
2. Sorts these objects based on their top-most, then left-most pixel.
3. The first object in the sorted list is colored blue (1).
4. The second and third objects are colored red (2) and yellow (4). The assignment depends on their relative vertical position:
   - If the second object is entirely above the third object (its maximum row index is less than the third object's minimum row index), the second becomes red (2) and the third becomes yellow (4).
   - Otherwise, the second becomes yellow (4) and the third becomes red (2).
5. All other pixels remain unchanged. Assumes exactly three gray objects are present based on the training examples.
"""

def find_objects(grid: np.ndarray, color: int) -> List[Set[Tuple[int, int]]]:
    """
    Finds all connected objects of a given color in the grid.
    Connectivity includes diagonal neighbors (8-way adjacency).

    Args:
        grid: The input numpy array representing the grid.
        color: The color of the objects to find.

    Returns:
        A list of sets, where each set contains the (row, col) coordinates
        of the pixels belonging to one object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) for a new object
                obj_coords = set()
                queue = [(r, c)]
                visited[r, c] = True
                
                while queue:
                    curr_r, curr_c = queue.pop(0)
                    obj_coords.add((curr_r, curr_c))

                    # Check all 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds and if neighbor is the correct color and not visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                queue.append((nr, nc))
                
                if obj_coords:
                    objects.append(obj_coords)
    
    return objects

def get_object_scan_order_key(obj_coords: Set[Tuple[int, int]]) -> Tuple[int, int]:
    """
    Determines the sorting key for an object based on its top-most, left-most pixel.

    Args:
        obj_coords: A set of (row, col) coordinates for the object.

    Returns:
        A tuple (min_row, min_col) representing the scan order key.
    """
    min_row = float('inf')
    min_col_at_min_row = float('inf')

    for r, c in obj_coords:
        if r < min_row:
            min_row = r
            min_col_at_min_row = c
        elif r == min_row and c < min_col_at_min_row:
            min_col_at_min_row = c
            
    return min_row, min_col_at_min_row

def get_bounding_box(obj_coords: Set[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """
    Calculates the bounding box of an object.

    Args:
        obj_coords: A set of (row, col) coordinates for the object.

    Returns:
        A tuple (min_row, min_col, max_row, max_col). Returns (-1,-1,-1,-1) if coords empty.
    """
    if not obj_coords:
        return -1, -1, -1, -1
    
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    
    return min(rows), min(cols), max(rows), max(cols)

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by recoloring gray objects based on scan order
    and relative vertical positions.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    gray_color = 5
    blue_color = 1
    red_color = 2
    yellow_color = 4

    # Find all gray objects
    gray_objects = find_objects(output_grid, gray_color)

    # Sort objects by scan order (top-most, then left-most pixel)
    gray_objects.sort(key=get_object_scan_order_key)

    # Check if we found the expected number of objects (based on training examples)
    if len(gray_objects) != 3:
        # If not exactly 3 objects, return the original grid or handle error.
        # For this specific task, based on examples, we assume 3 objects.
        # If this assumption is wrong for test cases, this might need adjustment.
        print(f"Warning: Expected 3 gray objects, but found {len(gray_objects)}. Returning original grid.")
        return output_grid 

    # Assign objects based on sorted order
    obj1_coords = gray_objects[0]
    obj2_coords = gray_objects[1]
    obj3_coords = gray_objects[2]

    # Recolor the first object to blue
    for r, c in obj1_coords:
        output_grid[r, c] = blue_color

    # Determine bounding boxes for the second and third objects
    min_r2, min_c2, max_r2, max_c2 = get_bounding_box(obj2_coords)
    min_r3, min_c3, max_r3, max_c3 = get_bounding_box(obj3_coords)

    # Check relative vertical position and assign colors accordingly
    color2 = yellow_color
    color3 = red_color
    if max_r2 < min_r3: # Object 2 is entirely above Object 3
        color2 = red_color
        color3 = yellow_color
        
    # Recolor the second object
    for r, c in obj2_coords:
        output_grid[r, c] = color2
        
    # Recolor the third object
    for r, c in obj3_coords:
        output_grid[r, c] = color3

    return output_grid