import numpy as np
from math import floor, ceil
from collections import deque

"""
This module transforms an input grid based on the following rules:

1.  Identifies all distinct connected components of red pixels (color 2) in the input grid. These components are assumed to be lines (horizontal or vertical).
2.  For each identified red line object:
    a. Calculates its length (L), which is the number of pixels in the line (or its maximum dimension).
    b. Calculates a radius value K = floor((L - 1) / 2).
    c. Determines the geometric center (center_r, center_c) of the line. If the average coordinate along the line's dimension is halfway between two integers (e.g., 8.5), it rounds up to the next integer (e.g., 9).
    d. Generates a diamond shape centered at (center_r, center_c) with radius K. The diamond includes all pixels (r, c) such that the Manhattan distance |r - center_r| + |c - center_c| <= K.
3.  Initializes the output grid as a copy of the input grid.
4.  For each generated diamond, iterates through its pixels. If a pixel within the diamond's bounds corresponds to a white pixel (color 0) in the current output grid state, that pixel's color is changed to azure (color 8). Red pixels and pixels already changed to azure remain unchanged.
5.  The final modified grid is returned as the output.
"""

def find_objects(grid, color):
    """
    Finds all connected components of a specified color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list[list[tuple[int, int]]]: A list where each element is a list
                                     of (row, col) coordinates for one object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start BFS to find a connected component
                component = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    curr_r, curr_c = q.popleft()
                    component.append((curr_r, curr_c))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        # Check bounds and if it's the target color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                if component:
                    objects.append(component)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by finding red lines and drawing azure diamonds
    around their centers based on their length.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid represented as a list of lists.
                         Or None if input is invalid.
    """
    if not input_grid or not isinstance(input_grid, list) or not isinstance(input_grid[0], list):
        print("Invalid input grid format.")
        return None
        
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    rows, cols = output_grid.shape
    
    # 1. Find all red objects (lines)
    red_objects = find_objects(input_np, 2) # 2 is red

    # 2. Process each red object
    for obj_coords in red_objects:
        if not obj_coords:
            continue

        # a. Calculate length L
        obj_length = len(obj_coords)
        
        # b. Calculate radius K
        radius_k = floor((obj_length - 1) / 2)

        # c. Calculate center (center_r, center_c)
        # Find min/max row and column for the object
        min_r = min(r for r, c in obj_coords)
        max_r = max(r for r, c in obj_coords)
        min_c = min(c for r, c in obj_coords)
        max_c = max(c for r, c in obj_coords)

        # Calculate average coordinates and round up (.5 case handled by ceil)
        # Use integer conversion after ceiling
        center_r = int(ceil((min_r + max_r) / 2))
        center_c = int(ceil((min_c + max_c) / 2))

        # d. & 4. Draw the azure diamond, modifying only white pixels
        # Iterate potential diamond coordinates based on radius K
        for r_offset in range(-radius_k, radius_k + 1):
            for c_offset in range(-radius_k, radius_k + 1):
                r, c = center_r + r_offset, center_c + c_offset
                
                # Calculate Manhattan distance
                dist = abs(r - center_r) + abs(c - center_c)

                # Check if within diamond radius and grid bounds
                if dist <= radius_k and 0 <= r < rows and 0 <= c < cols:
                    # Modify only if the pixel is currently white (0)
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = 8 # 8 is azure

    # Return the result as a list of lists
    return output_grid.tolist()