import numpy as np
from collections import deque

"""
Transforms a 5x5 grid of 0s and 3s by keeping only the '3's that are isolated.
A '3' is considered isolated if it has no adjacent '3's horizontally, vertically, or diagonally (8-way connectivity).
This is achieved by finding all connected components of '3's and only retaining components of size 1.
"""

def get_neighbors(r, c, rows, cols):
    """ Helper function to get valid 8-way neighbors for a cell. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_connected_components(grid):
    """ Finds all connected components of '3's using BFS. """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # If we find an unvisited '3', start a BFS to find its component
            if grid[r, c] == 3 and not visited[r, c]:
                current_component = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))

                    # Explore neighbors
                    for nr, nc in get_neighbors(curr_r, curr_c, rows, cols):
                        if grid[nr, nc] == 3 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found component
                components.append(current_component)
                
    return components

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Keeps only '3's that form a connected component of size 1.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid)
    rows, cols = input_array.shape
    
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_array)

    # Find all connected components of '3's
    components = find_connected_components(input_array)

    # Filter components: keep only those with size 1
    for component in components:
        if len(component) == 1:
            # Get the coordinates of the isolated '3'
            r, c = component[0]
            # Set the corresponding cell in the output grid to '3'
            output_grid[r, c] = 3
            
    # Convert the output numpy array back to a list of lists
    return output_grid.tolist()
