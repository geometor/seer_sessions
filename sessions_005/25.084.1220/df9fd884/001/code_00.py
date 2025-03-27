import numpy as np
from collections import deque

"""
Identify the background color (orange, 7). Identify the two static yellow (4) 
objects and the single moving object (a color other than orange or yellow).
Determine the relative configuration of the two yellow objects (top-left/bottom-right 
or top-right/bottom-left). Based on this configuration, determine a movement 
vector (delta_row, delta_col): (3, -5) for top-left/bottom-right, and (4, 5) 
for top-right/bottom-left. Create an output grid by copying the input. Erase 
the moving object from its original position in the output grid by filling its 
pixels with the background color. Calculate the new positions for the moving 
object's pixels by adding the movement vector to their original coordinates. 
Draw the moving object at its new position in the output grid using its 
original color.
"""

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid.
    
    Args:
        grid (np.array): The input grid.
        color (int): The target color.
        
    Returns:
        list: A list of objects, where each object is a list of (row, col) coordinates.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    current_object.append((row, col))
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                if current_object:
                    objects.append(current_object)
    return objects

def get_object_centroid(obj):
    """
    Calculates the centroid (average position) of an object.
    
    Args:
        obj (list): A list of (row, col) coordinates representing the object.
        
    Returns:
        tuple: (center_row, center_col)
    """
    if not obj:
        return (0, 0)
    sum_r = sum(r for r, c in obj)
    sum_c = sum(c for r, c in obj)
    count = len(obj)
    return (sum_r / count, sum_c / count)

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Define colors
    background_color = 7
    anchor_color = 4
    
    # Find the static anchor objects (yellow)
    anchor_objects = find_objects(input_grid, anchor_color)
    if len(anchor_objects) != 2:
        # Should not happen based on examples, but handle defensively
        return output_grid 
        
    # Find the moving object and its color
    moving_object = None
    moving_object_color = -1
    potential_colors = [c for c in range(10) if c != background_color and c != anchor_color]
    
    for color in potential_colors:
        objects = find_objects(input_grid, color)
        if len(objects) == 1:
            moving_object = objects[0]
            moving_object_color = color
            break
            
    if moving_object is None:
         # Should not happen based on examples
        return output_grid

    # Determine the configuration of anchor objects using centroids
    centroid1 = get_object_centroid(anchor_objects[0])
    centroid2 = get_object_centroid(anchor_objects[1])
    
    r1, c1 = centroid1
    r2, c2 = centroid2
    
    movement_vector = (0, 0) # Default (should be overwritten)
    
    # Configuration 1: Top-left / Bottom-right (relative)
    if (r1 < r2 and c1 < c2) or (r2 < r1 and c2 < c1):
        movement_vector = (3, -5) # delta_row, delta_col
    # Configuration 2: Top-right / Bottom-left (relative)
    elif (r1 < r2 and c1 > c2) or (r2 < r1 and c2 > c1):
         movement_vector = (4, 5) # delta_row, delta_col
    else:
        # Handle cases where centroids align perfectly vertically or horizontally
        # Based on examples, the diagonal configurations are expected.
        # If centroids are very close or aligned, default or error might be needed.
        # For now, let's assume diagonal separation holds true.
        # Fallback might be needed if test cases show otherwise.
        pass # Use default (0,0) or raise error? Let's stick with default for now.


    delta_row, delta_col = movement_vector

    # Erase the moving object from its original position
    for r, c in moving_object:
        if 0 <= r < rows and 0 <= c < cols:
             output_grid[r, c] = background_color

    # Draw the moving object at its new position
    for r, c in moving_object:
        new_r, new_c = r + delta_row, c + delta_col
        # Ensure the new position is within grid bounds
        if 0 <= new_r < rows and 0 <= new_c < cols:
            output_grid[new_r, new_c] = moving_object_color
        else:
            # Handle cases where object moves off-grid (optional, depends on task spec)
            # For now, pixels moving off-grid are simply lost.
            pass

    return output_grid