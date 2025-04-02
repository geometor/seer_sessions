import numpy as np
from collections import deque

"""
Transforms an input grid by identifying connected non-white objects (including diagonals).
If an object consists of exactly one pixel, it is expanded into a 1x3 horizontal line 
centered at the original pixel's location, using the original pixel's color. 
The expansion respects grid boundaries. Objects consisting of more than one pixel 
are left unchanged. The background remains white unless overwritten by the expansion.
"""

def find_objects(grid):
    """
    Finds all connected objects of non-white pixels in the grid.
    Connectivity includes diagonals.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'pixels' (a set of (row, col) tuples) and 'color'.
    """
    height, width = grid.shape
    visited = set()
    objects = []
    
    for r in range(height):
        for c in range(width):
            # Check if pixel is non-white and not visited
            if grid[r, c] != 0 and (r, c) not in visited:
                object_color = grid[r, c]
                current_object_pixels = set()
                queue = deque([(r, c)])
                visited.add((r, c))
                
                # Start Breadth-First Search (BFS) to find connected pixels of the same color
                while queue:
                    curr_r, curr_c = queue.popleft()
                    current_object_pixels.add((curr_r, curr_c))
                    
                    # Check all 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                                
                            nr, nc = curr_r + dr, curr_c + dc
                            
                            # Check bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # Check if neighbor is part of the same object (same color) and not visited
                                if grid[nr, nc] == object_color and (nr, nc) not in visited:
                                    visited.add((nr, nc))
                                    queue.append((nr, nc))
                                    
                objects.append({'pixels': current_object_pixels, 'color': object_color})
                
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input_grid.
    # This preserves background and larger objects initially.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find all distinct non-white objects in the input grid.
    objects = find_objects(input_grid)

    # Iterate through each identified object.
    for obj in objects:
        # Count the number of pixels in the object.
        num_pixels = len(obj['pixels'])
        
        # If the object consists of exactly one pixel:
        if num_pixels == 1:
            # Get the coordinates and color of the single pixel.
            r, c = next(iter(obj['pixels'])) 
            color = obj['color']
            
            # Color the center pixel (the original pixel's location).
            # This is technically already done by the copy, but good practice.
            output_grid[r, c] = color 
            
            # Color the pixel to the left, if within bounds.
            if c - 1 >= 0:
                output_grid[r, c - 1] = color
                
            # Color the pixel to the right, if within bounds.
            if c + 1 < width:
                output_grid[r, c + 1] = color
                
        # If the object consists of more than one pixel, do nothing.
        # The pixels are already correctly placed in the output_grid 
        # due to the initial copy.
        # else: # num_pixels > 1
        #     pass # No change needed for larger objects

    # Return the modified grid.
    return output_grid