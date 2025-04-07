import numpy as np
from typing import List, Tuple, Set

"""
Transformation Rule:

1. Identify all distinct objects in the input grid. An object is a connected 
   component of pixels (adjacent horizontally, vertically, or diagonally) that 
   are not the background color (orange, 7).
2. For each identified object:
   a. Check if it contains at least one white pixel (0).
   b. Check if it is entirely surrounded by the background color (orange, 7). 
      This means no pixel of the object touches the grid boundary or is adjacent 
      (horizontally, vertically, or diagonally) to a non-background pixel that 
      is not part of the same object.
3. If both conditions (contains white AND is surrounded by orange) are true 
   for an object, replace all pixels belonging to that object with the 
   background color (orange, 7).
4. Otherwise, the object remains unchanged.
5. Pixels that are initially the background color also remain unchanged.
"""

def find_objects(grid: np.ndarray, background_color: int) -> List[Set[Tuple[int, int]]]:
    """
    Finds all connected objects of non-background pixels in the grid.
    Connectivity includes diagonals.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                # Start a Breadth-First Search (BFS) for a new object
                current_object = set()
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    current_object.add((row, col))

                    # Check all 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = row + dr, col + dc

                            # Check bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is part of the object and not visited
                                if grid[nr, nc] != background_color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                
                if current_object:
                    objects.append(current_object)
                    
    return objects

def is_surrounded(grid: np.ndarray, obj: Set[Tuple[int, int]], background_color: int) -> bool:
    """
    Checks if an object is completely surrounded by the background color or grid boundaries.
    """
    height, width = grid.shape
    
    for r, c in obj:
        # Check all 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self
                
                nr, nc = r + dr, c + dc

                # Check if neighbor is out of bounds
                if not (0 <= nr < height and 0 <= nc < width):
                    return False # Touches boundary

                # Check if neighbor is inside bounds but not background and not part of the object
                if (nr, nc) not in obj and grid[nr, nc] != background_color:
                    return False # Touches another object or non-background pixel
                    
    return True # All adjacent cells outside the object are background

def contains_color(grid: np.ndarray, obj: Set[Tuple[int, int]], target_color: int) -> bool:
    """
    Checks if any pixel within the object has the target color.
    """
    for r, c in obj:
        if grid[r, c] == target_color:
            return True
    return False

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    Identifies objects containing white (0) and surrounded by orange (7),
    and replaces them entirely with orange (7).
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid = grid_np.copy()
    height, width = grid_np.shape
    
    background_color = 7
    target_indicator_color = 0

    # Find all distinct objects (connected components of non-background pixels)
    objects = find_objects(grid_np, background_color)

    # Iterate through each found object
    for obj in objects:
        # Check Condition 1: Does the object contain the target indicator color (white, 0)?
        has_target_color = contains_color(grid_np, obj, target_indicator_color)
        
        # Check Condition 2: Is the object completely surrounded by the background color (orange, 7)?
        is_obj_surrounded = is_surrounded(grid_np, obj, background_color)
        
        # If both conditions are met, replace the object's pixels with the background color
        if has_target_color and is_obj_surrounded:
            for r, c in obj:
                output_grid[r, c] = background_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()