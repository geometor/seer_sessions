import numpy as np
from collections import Counter

"""
Identify a unique pixel (excluding background and white) in the input grid. 
Find the white (color 0) object closest to this unique pixel. 
If the unique pixel is horizontally to the right of the closest white object, change the rightmost column of that object to magenta (color 6).
If the unique pixel is horizontally to the left of the closest white object, change the leftmost column of that object to magenta (color 6).
The background color is assumed to be the most frequent color in the grid (orange, 7 in the examples).
Distance is measured as the minimum Manhattan distance between the unique pixel and any pixel of the white object.
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
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj:
                    objects.append(obj)
    return objects

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

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # 1. Determine background color (most frequent color)
    color_counts = Counter(grid.flatten())
    if not color_counts:
        return output_grid.tolist() # Handle empty grid case
    background_color = color_counts.most_common(1)[0][0]
    
    # 2. Find the unique activating pixel (color count == 1, not background, not white)
    unique_pixel_coord = None
    unique_pixel_color = -1
    
    # Adjust counts to exclude background and white (0)
    pixel_counts = Counter()
    for r in range(rows):
        for c in range(cols):
             val = grid[r, c]
             if val != background_color and val != 0:
                 pixel_counts[val] += 1

    unique_colors = [color for color, count in pixel_counts.items() if count == 1]

    if len(unique_colors) == 1:
        unique_pixel_color = unique_colors[0]
        # Find the coordinates of this unique pixel
        unique_pixel_coords_list = np.argwhere(grid == unique_pixel_color)
        if len(unique_pixel_coords_list) == 1:
             unique_pixel_coord = tuple(unique_pixel_coords_list[0])
    
    if unique_pixel_coord is None:
        # No unique pixel found, return original grid
        return output_grid.tolist()

    # 3. Find all white objects
    white_objects = find_objects(grid, 0)
    if not white_objects:
        # No white objects found, return original grid
        return output_grid.tolist()

    # 4. Find the white object closest to the unique pixel
    min_dist = float('inf')
    target_white_object = None
    for obj in white_objects:
        dist = find_closest_point_in_object(unique_pixel_coord, obj)
        if dist < min_dist:
            min_dist = dist
            target_white_object = obj
        # Tie-breaking: could add rules here if needed, e.g., top-most, left-most
        # For now, the first one found with the min distance is kept.

    if target_white_object is None:
         # Should not happen if white_objects is not empty, but good practice
        return output_grid.tolist()

    # 5. Get bounding box and relative position
    min_r, min_c, max_r, max_c = get_bounding_box(target_white_object)
    unique_r, unique_c = unique_pixel_coord

    # 6. Modify the output grid based on relative position
    modification_color = 6 # magenta
    
    if unique_c > max_c: # Unique pixel is to the right
        # Change rightmost column (max_c) of the object to magenta
        for r, c in target_white_object:
            if c == max_c:
                output_grid[r, c] = modification_color
                
    elif unique_c < min_c: # Unique pixel is to the left
        # Change leftmost column (min_c) of the object to magenta
        for r, c in target_white_object:
            if c == min_c:
                output_grid[r, c] = modification_color
                
    # If unique_c is between min_c and max_c (inclusive), no change happens per observed logic.

    return output_grid.tolist()
