import numpy as np
from collections import deque

"""
Transformation Rule:
1. Initialize the output grid as a copy of the input grid.
2. Scan the input grid to find the unique 'fill color' pixel (either yellow/4 or orange/7). Store this fill color. If none is found, return the original grid.
3. Find all connected components (regions) of white (0) pixels in the input grid.
4. For each white component:
    a. Check if any pixel in the component touches the grid edge. If it does, this component is invalid; ignore it.
    b. Determine all pixels immediately adjacent (up, down, left, right) to any pixel in the component, but which are *not* part of the component itself. These are the boundary neighbors.
    c. Check if all boundary neighbors exist and if they all have the *exact same* single non-white color. Store this boundary color. If neighbors don't exist, or are not uniform, or are white, this component is invalid; ignore it.
    d. **Size Exclusion:** Check if the component is exactly a 2x2 square. If it is, and the boundary color found in step 4c is red (2), then this component is invalid; ignore it.
    e. **Color Filter:** Apply a filter based on the fill color and the boundary color:
        i. If the fill color is orange (7), the component is only valid if its boundary color is red (2) or gray (5).
        ii. If the fill color is yellow (4), the component is only valid if its boundary color is red (2).
    f. If the component is valid (passes edge check, uniform non-white boundary check, size exclusion check, and the color filter check), then mark it for filling.
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
    # Fallback: Return -1 if no fill color found
    return -1 

def get_neighbors(r, c, height, width):
    """Gets valid adjacent neighbor coordinates (up, down, left, right)."""
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < height - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def find_connected_components(grid, color_to_find):
    """Finds all connected components of a specific color using Breadth-First Search (BFS)."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color_to_find and not visited[r, c]:
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

def check_validity_and_filter(component, grid, fill_color):
    """
    Checks if a component of white pixels satisfies all enclosure, size, and filter conditions.
    Returns True if valid, False otherwise.
    """
    height, width = grid.shape
    boundary_colors = set()
    first_boundary_color = -1 
    touches_edge = False
    has_boundary_neighbors = False

    # Check for edge contact first
    for r, c in component:
        if r == 0 or r == height - 1 or c == 0 or c == width - 1:
            touches_edge = True
            return False # Invalid if touches edge

    # If not touching edge, find boundary neighbors and colors
    for r, c in component:
        for nr, nc in get_neighbors(r, c, height, width):
            if (nr, nc) not in component:
                has_boundary_neighbors = True
                neighbor_color = grid[nr, nc]
                boundary_colors.add(neighbor_color)
                if first_boundary_color == -1:
                    first_boundary_color = neighbor_color

    # Check boundary validity
    if not has_boundary_neighbors:
        return False # Must have neighbors outside itself

    is_uniform_non_white = len(boundary_colors) == 1 and 0 not in boundary_colors
    if not is_uniform_non_white:
        return False # Boundary must be single, non-white color
        
    boundary_color = first_boundary_color # The uniform boundary color

    # Check Size Exclusion: Is it a 2x2 square bounded by red?
    if len(component) == 4 and boundary_color == 2:
        # Further check if it's actually a 2x2 square shape
        min_r = min(r for r, c in component)
        max_r = max(r for r, c in component)
        min_c = min(c for r, c in component)
        max_c = max(c for r, c in component)
        if max_r - min_r == 1 and max_c - min_c == 1:
             return False # Exclude 2x2 white squares bounded by red

    # Apply Color Filter
    if fill_color == 7: # Orange fill
        if boundary_color == 2 or boundary_color == 5: # Red or Gray boundary
            return True
    elif fill_color == 4: # Yellow fill
        if boundary_color == 2: # Red boundary only
            return True

    # If filter conditions are not met
    return False

def transform(input_grid):
    """
    Applies the transformation rule: finds the fill color (orange/7 or yellow/4),
    identifies white regions that are fully enclosed by specific boundary colors 
    (red/2 or gray/5 for orange fill; red/2 only for yellow fill) without touching the edge,
    excluding 2x2 red-bounded squares, and fills those valid regions with the fill color.
    """
    # Convert input to numpy array for efficient operations
    grid = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_grid = grid.copy()
    height, width = grid.shape

    # Step 1: Find the fill color (4 or 7)
    fill_color = find_fill_color(grid)
    if fill_color == -1: 
         # No fill color found, return the original grid
         return output_grid.tolist() 

    # Step 2: Find all connected components of white (0) pixels
    white_components = find_connected_components(grid, 0)

    # Step 3 & 4: Check each white component for validity and filter
    for component in white_components:
        # Check all conditions: edge, boundary uniformity, size exclusion, color filter
        if check_validity_and_filter(component, grid, fill_color):
            # Step 5: If valid, fill the region in the output grid
            for r, c in component:
                output_grid[r, c] = fill_color

    # Return the final modified grid as a list of lists
    return output_grid.tolist()