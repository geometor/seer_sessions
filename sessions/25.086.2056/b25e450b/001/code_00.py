"""
Identify contiguous areas (connected components) of white pixels (color 0). 
If such an area consists of more than 2 pixels, change all pixels within 
that area to orange (color 7). Leave all other pixels unchanged.
This rule is derived from examples train_2 and train_3. Example train_1 shows 
additional complexities or inconsistencies not captured by this rule.
"""

import copy
from collections import deque

def find_objects(grid, color):
    """
    Finds all connected components of a given color in the grid using BFS.
    Uses 4-way connectivity (up, down, left, right).
    
    Args:
        grid (list of lists): The input grid.
        color (int): The color of the objects to find.
        
    Returns:
        list of sets: A list where each set contains (row, col) tuples 
                      representing the pixels of a single connected component.
    """
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])
    if cols == 0:
        return []
        
    visited = set()
    objects = []

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            # If pixel is the target color and not yet visited, it's the start of a new object
            if grid[r][c] == color and (r, c) not in visited:
                current_object = set()
                queue = deque([(r, c)])
                visited.add((r, c))
                current_object.add((r, c))

                # Perform BFS to find all connected pixels of the same color
                while queue:
                    row, col = queue.popleft()

                    # Explore neighbors (4-way connectivity: right, left, down, up)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if the neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr][nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                current_object.add((nr, nc))
                                queue.append((nr, nc))
                
                # Add the completed object (set of coordinates) to the list of objects
                if current_object:
                    objects.append(current_object)
    
    return objects

def transform(input_grid):
    """
    Transforms the input grid by filling large white areas with orange.

    Identifies contiguous areas (connected components) of white pixels (color 0). 
    If such an area consists of more than 2 pixels (size > 2), changes all 
    pixels within that area to orange (color 7). Leaves all other pixels 
    unchanged.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # Create a deep copy of the input grid to avoid modifying the original
    # This ensures the transformation is applied based on the initial state
    output_grid = copy.deepcopy(input_grid) 
    
    # Define the target color (white), fill color (orange), and size threshold
    target_color = 0
    fill_color = 7
    min_size_threshold = 2 # Areas must be strictly larger than this size

    # Find all connected components (objects) of the target color (white)
    white_objects = find_objects(output_grid, target_color)

    # Iterate through each white object found
    for obj in white_objects:
        # Check if the size (number of pixels) of the object is greater than the threshold
        if len(obj) > min_size_threshold:
            # If the object is large enough, change all its pixels to the fill color (orange)
            for r, c in obj:
                output_grid[r][c] = fill_color

    # Return the modified grid
    return output_grid