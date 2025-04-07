import numpy as np
from collections import deque

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Scan the input grid to find the unique 'fill color' pixel (either yellow/4 or orange/7). Store this fill color.
3. Find all connected components (regions) of white (0) pixels in the input grid.
4. For each white component:
    a. Determine all pixels immediately adjacent (up, down, left, right) to the component that are *not* part of the component itself. These are the boundary neighbors.
    b. Check if the component touches the grid edge. If it does, it's not enclosed.
    c. Check if all boundary neighbors exist and have the *exact same* non-white color.
    d. If the component does not touch the edge AND all boundary neighbors share the same single non-white color, then this component is an "enclosed region".
5. Change the color of all pixels belonging to any identified "enclosed region" in the *output* grid to the stored 'fill color'.
6. Return the modified output grid.
"""

def find_fill_color(grid):
    """Scans the grid to find the unique yellow (4) or orange (7) pixel."""
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 4 or grid[r, c] == 7:
                return grid[r, c]
    # Should not happen based on problem description, but return default if needed
    return 0 

def get_neighbors(r, c, height, width):
    """Gets valid adjacent neighbor coordinates (up, down, left, right)."""
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < height - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def find_connected_components(grid, color_to_find):
    """Finds all connected components of a specific color using BFS."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color_to_find and not visited[r, c]:
                # Start BFS for a new component
                component = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component.add((r, c))

                while q:
                    row, col = q.popleft()
                    for nr, nc in get_neighbors(row, col, height, width):
                        if grid[nr, nc] == color_to_find and not visited[nr, nc]:
                            visited[nr, nc] = True
                            component.add((nr, nc))
                            q.append((nr, nc))
                
                components.append(component)
    return components

def check_enclosure(component, grid):
    """
    Checks if a component of white pixels is enclosed by a single non-white color
    and does not touch the grid edge.
    Returns True if enclosed, False otherwise.
    """
    height, width = grid.shape
    boundary_neighbors = set()
    boundary_colors = set()
    
    touches_edge = False

    for r, c in component:
        # Check if the component pixel is on the edge
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
            touches_edge = True
            # No need to check further if it touches the edge
            # break # Optimization: We could break early, but let's check all boundary neighbors first for completeness

        # Find neighbors of the current component pixel
        for nr, nc in get_neighbors(r, c, height, width):
            # If the neighbor is NOT part of the component, it's a boundary neighbor
            if (nr, nc) not in component:
                boundary_neighbors.add((nr, nc))
                boundary_colors.add(grid[nr, nc])

    # An enclosed region cannot touch the edge
    if touches_edge:
        return False
        
    # An enclosed region must have boundary neighbors
    if not boundary_neighbors:
        return False

    # All boundary neighbors must have the same color, and it must not be white (0)
    if len(boundary_colors) == 1 and 0 not in boundary_colors:
        return True
    else:
        return False

def transform(input_grid):
    """
    Applies the transformation rule: fills enclosed white regions with a specific color.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Step 1: Find the fill color
    fill_color = find_fill_color(grid)
    if fill_color == 0: # Handle case where fill color isn't found (though unlikely based on examples)
         return output_grid 

    # Step 2: Find all connected components of white (0) pixels
    white_components = find_connected_components(grid, 0)

    # Step 3 & 4: Check each white component for enclosure and fill if necessary
    for component in white_components:
        if check_enclosure(component, grid):
            # Step 5: Fill the enclosed region in the output grid
            for r, c in component:
                output_grid[r, c] = fill_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()