import numpy as np
from collections import deque

"""
Identifies connected components of white pixels (color 0) using 8-way 
adjacency (including diagonals). 
Recolors each white component based on its proximity to the absolute grid 
border (first/last row or first/last column).

1. Find all connected components of white pixels (0).
2. For each white component:
   a. Check if *any* pixel belonging to the component is adjacent (8-way) to 
      a pixel located on the absolute border of the grid (row 0, row H-1, 
      col 0, or col W-1). Adjacency includes diagonal neighbors.
   b. If any pixel in the component is adjacent to the border, recolor all 
      pixels in that component to red (2).
   c. If no pixel in the component is adjacent to the border, recolor all 
      pixels in that component to green (3).
3. Pixels that were not originally white remain unchanged.
"""

def _is_valid(r, c, height, width):
    """Checks if coordinates are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def _is_border_pixel(r, c, height, width):
    """Checks if a pixel coordinate is on the absolute border."""
    # Note: This function assumes r, c might be out of bounds, 
    # but the way it's used ensures _is_valid is implicitly checked first,
    # or the check is simply whether the coordinates *match* border indices.
    # For clarity and safety if reused, explicitly add bounds check.
    if not _is_valid(r, c, height, width):
         return False # Cannot be a border pixel if out of bounds
    return r == 0 or r == height - 1 or c == 0 or c == width - 1

def transform(input_grid):
    """
    Transforms the input grid by recoloring connected components of white pixels.
    Components adjacent to the border become red (2).
    Components not adjacent to the border become green (3).
    Other pixels remain unchanged.
    """
    # Convert input to numpy array for efficient operations
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output_grid as a copy of the input
    output_array = np.copy(input_array)
    
    # Keep track of visited white pixels to avoid processing components multiple times
    visited = np.zeros_like(input_array, dtype=bool)

    # Define 8-directional neighbours (including diagonals)
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),           (0, 1),
                  (1, -1), (1, 0), (1, 1)]

    # Iterate through each pixel of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is white (0) and hasn't been processed yet
            if input_array[r, c] == 0 and not visited[r, c]:
                
                # Found the start of a new white component, perform BFS
                component_coords = []
                is_component_border_adjacent = False # Flag for the whole component
                q = deque([(r, c)])
                visited[r, c] = True # Mark the starting pixel visited

                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.append((curr_r, curr_c))

                    # Check neighbours of the CURRENT component pixel for border adjacency
                    # If we haven't already determined this component touches the border...
                    if not is_component_border_adjacent: 
                        for dr, dc in directions:
                            nr, nc = curr_r + dr, curr_c + dc
                            # Check if this neighbour coordinate (nr, nc) IS a border pixel
                            # We need _is_valid here because nr, nc could be out of bounds
                            if _is_valid(nr, nc, height, width) and _is_border_pixel(nr, nc, height, width):
                                is_component_border_adjacent = True
                                # Optimization: Found one border adjacent neighbour for this component, 
                                # no need to check others for border adjacency. 
                                # We still need to continue BFS to find all component pixels.
                                break # Break inner loop (checking neighbours for border)

                    # Explore neighbours to continue BFS (find other WHITE pixels in the component)
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check if the neighbour is valid, is white, and not visited
                        if _is_valid(nr, nc, height, width) and \
                           input_array[nr, nc] == 0 and \
                           not visited[nr, nc]:
                            
                            visited[nr, nc] = True # Mark neighbour as visited immediately
                            q.append((nr, nc)) # Add neighbour to the queue

                # After BFS, determine the color for the entire component
                target_color = 2 if is_component_border_adjacent else 3
                
                # Apply the color to all pixels in the found component
                for comp_r, comp_c in component_coords:
                    output_array[comp_r, comp_c] = target_color
            
            # If pixel is not white or already visited, do nothing

    # Convert the numpy array back to a list of lists for the expected output format
    return output_array.tolist()