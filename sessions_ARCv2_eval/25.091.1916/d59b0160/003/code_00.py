import numpy as np
from typing import List, Tuple, Set

"""
Transformation Rule:

1. Identify all distinct objects in the input grid. An object is a connected 
   component of pixels (adjacent horizontally, vertically, or diagonally) that 
   are not the background color (orange, 7).
2. For each identified object:
   a. Check if it contains at least one white pixel (0).
   b. Check if it is entirely surrounded *within the grid boundaries* by the 
      background color (orange, 7). This means no pixel of the object can be 
      adjacent (horizontally, vertically, or diagonally) to the grid boundary 
      or to a non-background pixel that is not part of the same object.
3. If both conditions (contains white AND is surrounded by orange within the grid) 
   are true for an object, replace all pixels belonging to that object with the 
   background color (orange, 7) in the output grid.
4. Otherwise, the object remains unchanged.
5. Pixels that are initially the background color also remain unchanged.
"""

def find_objects(grid: np.ndarray, background_color: int) -> List[Set[Tuple[int, int]]]:
    """
    Finds all connected objects of non-background pixels in the grid.
    Connectivity includes diagonals (8-way).
    Args:
        grid: The input numpy array representing the grid.
        background_color: The integer value representing the background color.
    Returns:
        A list where each element is a set of (row, col) tuples representing
        the coordinates of the pixels belonging to a single object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If the pixel is not background and hasn't been visited yet, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                current_object = set()
                q = [(r, c)] # Queue for BFS
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

                            # Check if neighbor is within grid bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is part of the same object (not background)
                                # and hasn't been visited yet
                                if grid[nr, nc] != background_color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                
                # Add the found object to the list
                if current_object:
                    objects.append(current_object)
                    
    return objects

def is_surrounded(grid: np.ndarray, obj: Set[Tuple[int, int]], background_color: int) -> bool:
    """
    Checks if an object is completely surrounded by the background color 
    *within the grid boundaries*.
    Args:
        grid: The input numpy array representing the grid.
        obj: A set of (row, col) tuples representing the object's pixels.
        background_color: The integer value representing the background color.
    Returns:
        True if the object is surrounded, False otherwise.
    """
    height, width = grid.shape
    
    # Iterate through each pixel belonging to the object
    for r, c in obj:
        # Check all 8 neighbors of the current object pixel
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self
                
                nr, nc = r + dr, c + dc

                # Condition 1: Check if neighbor is outside the grid boundary
                if not (0 <= nr < height and 0 <= nc < width):
                    return False # Object touches the boundary, so it's not surrounded

                # Condition 2: Check if the neighbor is within bounds, 
                # *not* part of the current object, and *not* the background color.
                if (nr, nc) not in obj and grid[nr, nc] != background_color:
                    return False # Object touches another non-background pixel (could be another object)
                    
    # If we checked all neighbors of all pixels in the object and didn't return False,
    # it means all adjacent cells outside the object are background color.
    return True 

def contains_color(grid: np.ndarray, obj: Set[Tuple[int, int]], target_color: int) -> bool:
    """
    Checks if any pixel within the object has the target color.
    Args:
        grid: The input numpy array representing the grid.
        obj: A set of (row, col) tuples representing the object's pixels.
        target_color: The integer color value to search for.
    Returns:
        True if the target color is found in the object, False otherwise.
    """
    for r, c in obj:
        if grid[r, c] == target_color:
            return True
    return False

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    Identifies objects containing white (0) and surrounded by orange (7) 
    within the grid boundaries, and replaces them entirely with orange (7).
    """
    # Convert input list of lists to a numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, leaving the original input unchanged
    output_grid = grid_np.copy()
    
    # Define task-specific constants
    background_color = 7
    target_indicator_color = 0

    # Step 1: Find all distinct objects (connected components of non-background pixels)
    objects = find_objects(grid_np, background_color)

    # Step 2: Iterate through each found object
    for obj in objects:
        # Step 2a: Check if the object contains the target indicator color (white, 0)
        has_target_color = contains_color(grid_np, obj, target_indicator_color)
        
        # Step 2b: Check if the object is completely surrounded by the background color (orange, 7)
        #          within the grid boundaries.
        is_obj_surrounded = is_surrounded(grid_np, obj, background_color)
        
        # Step 3: If both conditions are met, replace the object's pixels 
        #         in the output grid with the background color.
        if has_target_color and is_obj_surrounded:
            for r, c in obj:
                output_grid[r, c] = background_color

    # Convert the final numpy array back to a list of lists for the required output format
    return output_grid.tolist()