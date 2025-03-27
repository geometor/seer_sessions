import numpy as np
from collections import deque

"""
Identifies distinct connected objects composed of non-white (non-zero) pixels, considering diagonal adjacency.
If an object is composed of exactly two distinct non-white colors (Color A and Color B), 
it swaps these colors within the object: all pixels of Color A become Color B, and all pixels of Color B become Color A. 
Objects with only one non-white color or more than two non-white colors remain unchanged. 
White (zero) background pixels remain unchanged.
"""

def find_objects(grid, background_color=0):
    """
    Finds connected components of non-background pixels using BFS.
    Considers diagonal pixels as connected.

    Args:
        grid (np.array): Input grid.
        background_color (int): The color value representing the background. Default is 0.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples 
              of pixels belonging to a single connected object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Define 8 directions for neighbors (including diagonals)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    for r in range(height):
        for c in range(width):
            # Start BFS if we find a non-background pixel that hasn't been visited
            if grid[r, c] != background_color and not visited[r, c]:
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_coords.add((curr_r, curr_c))
                    
                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor is part of the object and not visited
                            if grid[nr, nc] != background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                # Add the found object's coordinates to the list
                if current_object_coords:
                    objects.append(current_object_coords)
                    
    return objects

def transform(input_grid):
    """
    Transforms the input grid by swapping the two constituent colors within each 
    distinct two-colored object.
    
    Args:
        input_grid (list of lists): The input grid representing colors.
        
    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to NumPy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Initialize the output grid as a copy of the input grid
    output_grid = grid.copy()
    
    # Find all distinct objects (connected components of non-white pixels)
    # Each object is represented by a set of its coordinates
    objects_coords_list = find_objects(grid, background_color=0)
    
    # Iterate through each identified object
    for object_coords in objects_coords_list:
        # Get the pixel values corresponding to the current object's coordinates
        object_pixels = [grid[r, c] for r, c in object_coords]
        
        # Find the unique non-white colors within this object
        unique_colors = np.unique(object_pixels)
        # Filter out the background color (0) - although find_objects ensures this shouldn't be needed
        non_white_colors = unique_colors[unique_colors != 0] 
        
        # Check if the object is composed of exactly two non-white colors
        if len(non_white_colors) == 2:
            color1, color2 = non_white_colors[0], non_white_colors[1]
            
            # Iterate through the coordinates of this object again to perform the swap
            for r, c in object_coords:
                if grid[r, c] == color1:
                    output_grid[r, c] = color2
                elif grid[r, c] == color2:
                    output_grid[r, c] = color1
            # Pixels that were background (0) within the bounding box but not part 
            # of the object remain unchanged (as they are not in object_coords).
            # Objects with 1 or >2 colors also remain unchanged as per the copy initialization.

    # Return the modified grid converted back to list of lists
    return output_grid.tolist()