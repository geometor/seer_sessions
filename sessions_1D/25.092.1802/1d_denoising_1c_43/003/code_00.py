"""
Transforms the input grid by keeping only the largest contiguous object
of the dominant non-background color. The input grid is assumed to be 2D.

1.  Accept the input as a 2D grid (e.g., NumPy array).
2.  Identify the single non-white color present in the grid. If only white (0) is present, return an all-white grid of the same dimensions.
3.  Find all separate groups of connected pixels (objects) of this non-white color using cardinal adjacency (up, down, left, right).
4.  Count the number of pixels in each object found.
5.  Identify the object that has the largest count of pixels. If no non-white objects were found, return an all-white grid.
6.  Create a new output grid of the same dimensions as the input, initially filled entirely with the white color (0).
7.  For each pixel coordinate that belongs to the largest object identified, set the corresponding pixel in the output grid to the non-white color.
8.  Return the resulting 2D output grid.
"""

import numpy as np
from collections import deque

def _find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in a grid using BFS.

    Args:
        grid (np.array): The 2D input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of pixels belonging to a single object. Returns an empty list
              if no objects of target_color are found.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # If the cell has the target color and hasn't been visited yet, start a BFS
            if grid[r, c] == target_color and (r, c) not in visited:
                current_object = set() # Store pixels of the current object
                q = deque([(r, c)])    # Queue for BFS
                visited.add((r, c))    # Mark starting cell as visited
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object.add((curr_r, curr_c))
                    
                    # Check cardinal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == target_color and (nr, nc) not in visited:
                                visited.add((nr, nc)) # Mark neighbor as visited
                                q.append((nr, nc))   # Add neighbor to the queue
                                
                # Add the completed object (set of pixel coordinates) to the list
                objects.append(current_object)
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid by keeping only the largest object.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)
        
    # Initialize output grid with the background color (0)
    output_grid = np.zeros_like(input_grid)
    
    # --- Identify Dominant Color ---
    # Find unique colors in the input grid
    unique_colors = np.unique(input_grid)
    dominant_color = 0 # Default to background color
    
    # Find the first non-zero color (assuming only one non-background color per task example)
    for color in unique_colors:
        if color != 0:
            dominant_color = color
            break
            
    # If no non-background color found, return the all-zero grid
    if dominant_color == 0:
        return output_grid

    # --- Find Objects of the Dominant Color ---
    objects = _find_objects(input_grid, dominant_color)
    
    # If no objects of the dominant color are found, return the all-zero grid
    if not objects:
        return output_grid

    # --- Find the Largest Object ---
    # Use the 'key=len' argument to find the object (set) with the maximum number of elements (pixels)
    largest_object = max(objects, key=len)

    # --- Populate Output Grid ---
    # Iterate through the pixel coordinates of the largest object
    for r, c in largest_object:
        # Set the corresponding pixel in the output grid to the dominant color
        output_grid[r, c] = dominant_color
        
    # Return the final 2D output grid
    return output_grid