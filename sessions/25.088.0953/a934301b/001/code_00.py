import numpy as np

"""
Identifies connected components (objects) of non-white pixels (1s and 8s) using 8-way adjacency (including diagonals).
Filters these objects based on the count of azure (8) and blue (1) pixels within each object.
An object is kept if:
1. It contains zero azure (8) pixels.
OR
2. It contains exactly one azure (8) pixel AND more than two blue (1) pixels.
All other objects are removed (replaced with white (0)).
The output grid contains only the pixels of the kept objects on a white (0) background.
"""

def find_objects(grid):
    """
    Finds all connected components (objects) of non-background pixels in the grid.
    Uses 8-way connectivity (including diagonals).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list where each element is a list of (row, col) tuples
              representing the coordinates of pixels belonging to one object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            # If the cell is non-background and not yet visited, start a search
            if grid[r, c] != 0 and not visited[r, c]:
                current_object_coords = []
                queue = [(r, c)]
                visited[r, c] = True
                
                while queue:
                    cr, cc = queue.pop(0)
                    current_object_coords.append((cr, cc))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                                
                            nr, nc = cr + dr, cc + dc
                            
                            # Check bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is part of an object and not visited
                                if grid[nr, nc] != 0 and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    queue.append((nr, nc))
                                    
                if current_object_coords:
                    objects.append(current_object_coords)
                    
    return objects

def transform(input_grid):
    """
    Filters objects in the input grid based on their composition of blue (1) and azure (8) pixels.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The output grid with filtered objects.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with background color (white = 0)
    output_grid = np.zeros_like(input_array)
    
    # Find all distinct objects (connected components of non-zero pixels)
    objects = find_objects(input_array)
    
    # Analyze each object and decide whether to keep it
    for obj_coords in objects:
        azure_count = 0
        blue_count = 0
        
        # Count azure and blue pixels in the current object
        for r, c in obj_coords:
            pixel_value = input_array[r, c]
            if pixel_value == 1: # Blue
                blue_count += 1
            elif pixel_value == 8: # Azure
                azure_count += 1
                
        # Apply the filtering rule
        keep_object = False
        if azure_count == 0:
            keep_object = True
        elif azure_count == 1 and blue_count > 2:
            keep_object = True
            
        # If the object should be kept, copy its pixels to the output grid
        if keep_object:
            for r, c in obj_coords:
                output_grid[r, c] = input_array[r, c]
                
    # Return the result as a list of lists
    return output_grid.tolist()
