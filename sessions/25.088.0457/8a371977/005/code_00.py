import numpy as np
from collections import deque

"""
Recolors connected components of white pixels (0) based on whether any pixel
within the component touches the absolute border of the grid.

1. Initialize the output grid as a copy of the input grid.
2. Create a 'visited' grid to track processed white pixels.
3. Iterate through each pixel (r, c) of the input grid.
4. If a pixel is white (0) and hasn't been visited:
    a. Start a search (e.g., Breadth-First Search) to find all connected
       white pixels forming a component. Use 8-way adjacency (including diagonals).
    b. Keep track of all coordinates belonging to this component.
    c. During the search, maintain a flag `is_border_component`. Set this
       flag to True if *any* pixel encountered during the search for this
       component lies on the grid's absolute border (row 0, row H-1, col 0,
       or col W-1).
    d. Mark all pixels found during the search as visited.
    e. After finding the complete component:
        i. If `is_border_component` is True, change the color of all pixels
           in this component in the output grid to red (2).
        ii. If `is_border_component` is False, change the color of all pixels
            in this component in the output grid to green (3).
5. Pixels that were not white initially remain unchanged.
6. Return the modified output grid.
"""

def _is_valid(r, c, height, width):
    """Checks if coordinates are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def _is_border_pixel(r, c, height, width):
    """Checks if a pixel coordinate is on the absolute border."""
    return r == 0 or r == height - 1 or c == 0 or c == width - 1

def transform(input_grid):
    """
    Transforms the input grid by recoloring connected components of white pixels.
    Components touching the border become red (2).
    Components not touching the border become green (3).
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
                is_component_border_adjacent = False
                q = deque([(r, c)])
                visited[r, c] = True # Mark the starting pixel visited

                while q:
                    curr_r, curr_c = q.popleft()
                    component_coords.append((curr_r, curr_c))

                    # Check if this *current* pixel is on the border
                    if not is_component_border_adjacent and _is_border_pixel(curr_r, curr_c, height, width):
                        is_component_border_adjacent = True
                        # No need to break, continue BFS to find all component pixels

                    # Explore neighbours for BFS continuation
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