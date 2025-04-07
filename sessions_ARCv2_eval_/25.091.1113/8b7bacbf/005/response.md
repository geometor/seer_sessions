```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Scan the input grid to find the unique 'fill color' pixel (either yellow/4 or orange/7). Store this fill color.
3. Find all connected components (regions) of white (0) pixels in the input grid.
4. For each white component:
    a. Check if any pixel in the component touches the grid edge. If it does, this component is invalid; ignore it.
    b. Determine all pixels immediately adjacent (up, down, left, right) to any pixel in the component, but which are *not* part of the component itself. These are the boundary neighbors.
    c. Check if all boundary neighbors exist (i.e., the component is not empty and has neighbors outside itself) and if they all have the *exact same* single non-white color. Store this boundary color. If neighbors don't exist, or are not uniform, or are white, this component is invalid; ignore it.
    d. Apply a filter based on the fill color and the boundary color:
        i. If the fill color is orange (7), the component is only valid if its boundary color is red (2) or gray (5).
        ii. If the fill color is yellow (4), the component is only valid if its boundary color is red (2).
    e. If the component is valid (passes edge check, uniform non-white boundary check, and the color filter check), then mark it for filling.
5. Change the color of all pixels belonging to any valid marked component in the *output* grid to the stored 'fill color'.
6. Return the modified output grid.
"""

def find_fill_color(grid):
    """Scans the grid to find the unique yellow (4) or orange (7) pixel."""
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            pixel_color = grid[r, c]
            # Check if the color is yellow (4) or orange (7)
            if pixel_color == 4 or pixel_color == 7:
                return pixel_color
    # Fallback, though examples suggest a fill color always exists.
    # Return -1 to indicate not found, distinct from valid colors 0-9.
    return -1 

def get_neighbors(r, c, height, width):
    """Gets valid adjacent neighbor coordinates (up, down, left, right)."""
    neighbors = []
    # Check neighbor above
    if r > 0: neighbors.append((r - 1, c))
    # Check neighbor below
    if r < height - 1: neighbors.append((r + 1, c))
    # Check neighbor left
    if c > 0: neighbors.append((r, c - 1))
    # Check neighbor right
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def find_connected_components(grid, color_to_find):
    """Finds all connected components of a specific color using Breadth-First Search (BFS)."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    # Iterate through each cell in the grid
    for r in range(height):
        for c in range(width):
            # If the cell has the target color and hasn't been visited yet
            if grid[r, c] == color_to_find and not visited[r, c]:
                # Start BFS for a new component
                component = set() # Store coordinates of pixels in the component
                q = deque([(r, c)]) # Queue for BFS
                visited[r, c] = True
                component.add((r, c))

                # Process the queue
                while q:
                    row, col = q.popleft()
                    # Explore neighbors
                    for nr, nc in get_neighbors(row, col, height, width):
                        # If neighbor has the target color and hasn't been visited
                        if grid[nr, nc] == color_to_find and not visited[nr, nc]:
                            visited[nr, nc] = True
                            component.add((nr, nc))
                            q.append((nr, nc))
                
                # Add the found component to the list
                components.append(component)
    return components

def check_enclosure_and_filter(component, grid, fill_color):
    """
    Checks if a component of white pixels satisfies all enclosure and filter conditions:
    1. Does not touch the grid edge.
    2. Is enclosed by a single, uniform, non-white color.
    3. Meets the specific color filter based on fill_color and boundary_color.
    Returns True if all conditions are met, False otherwise.
    """
    height, width = grid.shape
    boundary_colors = set()
    first_boundary_color = -1 # Initialize boundary color tracker
    touches_edge = False
    has_boundary_neighbors = False

    # Iterate through each pixel in the component
    for r, c in component:
        # 1. Check if the component pixel is on the grid edge
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
            touches_edge = True
            # If it touches the edge, it cannot be enclosed per the rule.
            return False 

        # Find neighbors of the current component pixel
        for nr, nc in get_neighbors(r, c, height, width):
            # Check if the neighbor is *outside* the current white component
            if (nr, nc) not in component:
                has_boundary_neighbors = True
                neighbor_color = grid[nr, nc]
                boundary_colors.add(neighbor_color)
                # Store the first boundary color encountered
                if first_boundary_color == -1:
                    first_boundary_color = neighbor_color

    # 2a. Check if the component actually has any boundary neighbors
    if not has_boundary_neighbors:
        # Isolated component with no neighbors outside itself (e.g., whole grid is white)
        return False

    # 2b. Check if all boundary neighbors have the same, single, non-white color
    is_uniform_non_white = len(boundary_colors) == 1 and 0 not in boundary_colors
    if not is_uniform_non_white:
        # Boundary is non-uniform, or contains white pixels
        return False
        
    # If edge check and uniformity check passed, proceed to the color filter
    boundary_color = first_boundary_color # Since it's uniform, the first one represents all

    # 3. Apply color filter based on fill_color and boundary_color
    if fill_color == 7: # Fill color is Orange
        # Valid only if boundary is Red (2) or Gray (5)
        if boundary_color == 2 or boundary_color == 5: 
            return True
    elif fill_color == 4: # Fill color is Yellow
        # Valid only if boundary is Red (2)
        if boundary_color == 2: 
            return True

    # If the filter conditions are not met for the specific fill/boundary combination
    return False


def transform(input_grid):
    """
    Applies the transformation rule: finds the fill color (orange/7 or yellow/4),
    identifies white regions that are fully enclosed by specific boundary colors 
    (red/2 or gray/5 for orange fill; red/2 only for yellow fill) without touching the edge,
    and fills those valid regions with the fill color.
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = grid.copy()
    height, width = grid.shape

    # Step 1: Find the fill color (4 or 7)
    fill_color = find_fill_color(grid)
    # If no fill color is found, return the original grid (as per fallback in helper)
    if fill_color == -1: 
         #print("Warning: Fill color (4 or 7) not found in input grid.")
         return output_grid.tolist() 

    # Step 2: Find all connected components of white (0) pixels
    white_components = find_connected_components(grid, 0)

    # Step 3 & 4: Check each white component for validity and filter
    for component in white_components:
        # Check enclosure conditions (edge, uniform non-white boundary) and color filter
        if check_enclosure_and_filter(component, grid, fill_color):
            # Step 5: If valid, fill the region in the output grid
            for r, c in component:
                output_grid[r, c] = fill_color

    # Return the final modified grid as a list of lists
    return output_grid.tolist()
```