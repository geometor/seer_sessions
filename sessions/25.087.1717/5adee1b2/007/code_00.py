import numpy as np
from collections import deque

"""
Transforms an input grid by:
1. Initializing an output grid as a copy of the input.
2. Finding a color map from marker pairs in the bottom-left corner (cols 0, 1), read bottom-up.
3. Identifying all distinct connected non-white objects (4-connectivity).
4. For each object whose color is a key in the color map:
    a. Find its minimal bounding box.
    b. Fill the bounding box area in the output grid with the mapped color.
    c. Restore the original object pixels within the filled bounding box.
5. Return the modified output grid.
"""

def find_marker_pairs(grid):
    """
    Finds horizontal marker pairs in the bottom-left corner (cols 0 and 1)
    and returns a dictionary mapping left_color -> right_color.
    It iterates from the bottom row upwards, prioritizing lower rows for mapping.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        dict: A dictionary mapping source colors to target colors.
    """
    color_map = {}
    height, width = grid.shape

    # Only proceed if there are at least 2 columns for horizontal pairs
    if width < 2:
        return color_map

    # Search columns 0 and 1, from bottom row up
    for r in range(height - 1, -1, -1): # Iterate from bottom row up to 0
        left_color = grid[r, 0]
        right_color = grid[r, 1]

        # Check if both are non-white (not 0)
        if left_color != 0 and right_color != 0:
            # If this left_color hasn't been mapped yet, add the mapping
            if left_color not in color_map:
                color_map[left_color] = right_color
                
    return color_map

def find_objects(grid):
    """
    Finds all distinct non-white objects (connected components using 4-connectivity) in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains (object_color, object_coords).
              object_coords is a set of (row, col) tuples for the pixels of that object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If pixel is non-white and not yet visited
            if grid[r, c] != 0 and not visited[r, c]:
                object_color = grid[r, c]
                object_coords = set()
                q = deque([(r, c)])
                visited[r,c] = True # Mark starting point visited
                object_coords.add((r,c))
                
                # Perform BFS to find all connected pixels of the same object_color
                while q:
                    row, col = q.popleft()

                    # Add neighbors to queue (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Bounds check
                        if not (0 <= nr < height and 0 <= nc < width):
                            continue
                        
                        # Visited check and Color check
                        if not visited[nr, nc] and grid[nr, nc] == object_color:
                             visited[nr, nc] = True
                             object_coords.add((nr, nc))
                             q.append((nr, nc))
                
                # Add the found object to the list if it has coordinates
                if object_coords:
                     objects.append((object_color, object_coords))

    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input list of lists to numpy array for efficient manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # 1. Initialize output grid as a copy of the input
    output_np = np.copy(input_np)

    # 2. Find the color mapping from horizontal marker pairs
    color_map = find_marker_pairs(input_np)

    # 3. Identify all distinct non-white objects
    objects = find_objects(input_np)

    # 4. Process each object
    for object_color, object_coords in objects:
        
        # 4a/b. Check if the object's color has a mapping
        if object_color in color_map:
            # 4c.i. Get the target fill color
            fill_color = color_map[object_color]
            
            # Ensure object_coords is not empty before calculating bounds
            if not object_coords:
                continue

            # 4c.ii. Calculate the minimal bounding box
            rows = [r for r, c in object_coords]
            cols = [c for r, c in object_coords]
            min_r = min(rows)
            max_r = max(rows)
            min_c = min(cols)
            max_c = max(cols)

            # 4c.iii. Fill the entire bounding box area in the output grid with the fill_color
            # Numpy slicing is [start:end], where end is exclusive. Add 1 to max indices.
            output_np[min_r : max_r + 1, min_c : max_c + 1] = fill_color
            
            # 4c.iv. Restore the original object pixels
            for r_obj, c_obj in object_coords:
                output_np[r_obj, c_obj] = object_color

        # 4d. If no mapping exists, do nothing (object pixels are already preserved from the initial copy)

    # 5. Convert back to list of lists for the expected output format
    return output_np.tolist()