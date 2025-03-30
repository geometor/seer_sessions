import numpy as np
from collections import Counter

"""
1. Determine the background color (most frequent).
2. Find all "activator pixels": isolated pixels (no neighbors, including diagonals, of the same color) that are not background and not white (0).
3. If multiple activators exist, select the one closest (Manhattan distance) to its individually nearest white object.
4. Identify the target white object: the white object closest (minimum Manhattan distance) to the selected activator pixel.
5. If the activator pixel is horizontally to the right of the target white object's bounding box, change the rightmost column of the object to magenta (6).
6. If the activator pixel is horizontally to the left of the target white object's bounding box, change the leftmost column of the object to magenta (6).
7. Otherwise, make no changes.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[set[tuple[int, int]]]: A list of objects, where each object is a
                                      set of (row, col) coordinates.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = set()
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    obj.add((row, col))
                    # Use 4-connectivity for finding objects
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj:
                    objects.append(obj)
    return objects

def is_isolated(grid, r, c):
    """
    Checks if a pixel at (r, c) is isolated from pixels of the same color.
    Isolation means no neighbors (including diagonals) have the same color.

    Args:
        grid (np.ndarray): The input grid.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.

    Returns:
        bool: True if the pixel is isolated, False otherwise.
    """
    rows, cols = grid.shape
    pixel_color = grid[r, c]
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == pixel_color:
                return False
    return True

def get_bounding_box(obj):
    """
    Calculates the bounding box of an object.

    Args:
        obj (set[tuple[int, int]]): The object (set of coordinates).

    Returns:
        tuple[int, int, int, int]: (min_row, min_col, max_row, max_col)
    """
    if not obj:
        return None
    rows = [r for r, c in obj]
    cols = [c for r, c in obj]
    return min(rows), min(cols), max(rows), max(cols)

def manhattan_distance(p1, p2):
    """
    Calculates the Manhattan distance between two points.

    Args:
        p1 (tuple[int, int]): First point (row, col).
        p2 (tuple[int, int]): Second point (row, col).

    Returns:
        int: The Manhattan distance.
    """
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_closest_point_in_object(point, obj):
    """
    Finds the minimum Manhattan distance from a point to any point in an object.

    Args:
        point (tuple[int, int]): The reference point (row, col).
        obj (set[tuple[int, int]]): The object (set of coordinates).

    Returns:
        int: The minimum Manhattan distance. Returns infinity if object is empty.
    """
    if not obj:
        return float('inf')
    min_dist = float('inf')
    for obj_point in obj:
        dist = manhattan_distance(point, obj_point)
        min_dist = min(min_dist, dist)
    return min_dist

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # 1. Determine background color (most frequent color)
    color_counts = Counter(grid.flatten())
    if not color_counts:
        return output_grid.tolist() # Handle empty grid case
    background_color = color_counts.most_common(1)[0][0]

    # 2. Find potential activator pixels (isolated, not background, not white)
    potential_activators = []
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != background_color and color != 0:
                if is_isolated(grid, r, c):
                    potential_activators.append(((r, c), color))

    # 3. If no potential activators, return original grid
    if not potential_activators:
        return output_grid.tolist()

    # 4. Find all white objects
    white_objects = find_objects(grid, 0)
    if not white_objects:
        return output_grid.tolist() # No white objects, return original grid

    # 5. Select the main activator
    selected_activator_coord = None
    if len(potential_activators) == 1:
        selected_activator_coord = potential_activators[0][0]
    else:
        # 6. If multiple activators, find the one closest to its nearest white object
        min_overall_dist = float('inf')
        best_activator_coord = None
        for activator_coord, _ in potential_activators:
            min_dist_to_any_white = float('inf')
            for white_obj in white_objects:
                dist = find_closest_point_in_object(activator_coord, white_obj)
                min_dist_to_any_white = min(min_dist_to_any_white, dist)

            if min_dist_to_any_white < min_overall_dist:
                 min_overall_dist = min_dist_to_any_white
                 best_activator_coord = activator_coord
            # Tie-breaking: Current logic takes the first one found with the min distance.
            # More sophisticated tie-breaking (e.g., top-left) could be added if needed.

        selected_activator_coord = best_activator_coord

    if selected_activator_coord is None:
         # This case might occur if multiple activators exist but tie-breaking fails or an edge case.
         # Or if somehow no best activator was found despite multiple potentials.
         return output_grid.tolist() # Return original if no activator could be definitively selected

    # 7. Find the target white object (closest to the *selected* activator)
    min_dist_to_selected = float('inf')
    target_white_object = None
    for obj in white_objects:
        dist = find_closest_point_in_object(selected_activator_coord, obj)
        if dist < min_dist_to_selected:
            min_dist_to_selected = dist
            target_white_object = obj
        # Tie-breaking: again, takes the first found closest object.

    if target_white_object is None:
         # Should not happen if white_objects is not empty, but good practice
        return output_grid.tolist()

    # 8. Get bounding box of the target white object
    min_r, min_c, max_r, max_c = get_bounding_box(target_white_object)
    activator_r, activator_c = selected_activator_coord

    # 9. Modify the output grid based on relative position
    modification_color = 6 # magenta

    # 10. Apply modification logic
    if activator_c > max_c: # Activator is strictly to the right
        # Change rightmost column (max_c) of the object to magenta
        for r, c in target_white_object:
            if c == max_c:
                output_grid[r, c] = modification_color

    elif activator_c < min_c: # Activator is strictly to the left
        # Change leftmost column (min_c) of the object to magenta
        for r, c in target_white_object:
            if c == min_c:
                output_grid[r, c] = modification_color

    # Otherwise (activator column within or equal to min/max bounds), no change

    # 11. Return the modified grid
    return output_grid.tolist()