import numpy as np
from collections import deque

"""
Conditionally changes a single magenta pixel (6) to white (0) based on the
colors of its two innermost containing non-background objects.

The transformation rule is as follows:
1. Locate the unique magenta pixel (color 6). If not found or not unique, return the input grid.
2. Determine the color of the immediate object enclosing the magenta pixel and its surrounding white space (if any). Let this be C_inner. If no single enclosing object color is found, return the input grid.
3. Determine the color of the object immediately enclosing the C_inner object and its surrounding white space (if any). Let this be C_outer. If no single enclosing object color is found, return the input grid.
4. Check if the color pair (C_inner, C_outer) matches specific conditions:
   - (Yellow=4, Red=2) OR
   - (Blue=1, Green=3)
5. If a condition is met, change the magenta pixel to white (0). Otherwise, return the input grid unchanged.

Containment is determined using flood fill (BFS). A pixel/object is considered contained if a flood fill starting from it (traversing background color 0 and the object's own color) cannot reach the grid boundary.
"""

def find_pixel(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    # Use numpy's where function for efficiency
    coords_array = np.argwhere(grid == color)
    # Convert numpy array to list of tuples
    return [tuple(coord) for coord in coords_array]

def get_unique_colors(grid, coords):
    """Gets the set of unique non-zero colors at the given coordinates."""
    colors = set()
    rows, cols = grid.shape
    for r, c in coords:
        # Ensure coordinates are within bounds (though they should be from flood_fill)
        if 0 <= r < rows and 0 <= c < cols:
            color = grid[r, c]
            if color != 0: # Ignore background color
                colors.add(color)
    return colors

def flood_fill(grid, start_pos, traversable_colors):
    """
    Performs a flood fill (BFS) starting from start_pos.

    Args:
        grid: The numpy grid.
        start_pos: The (row, col) tuple to start from.
        traversable_colors: A set of colors allowed to traverse.

    Returns:
        A tuple: (filled_coords, adjacent_coords, boundary_reached)
        - filled_coords: set of (row, col) visited during the fill.
        - adjacent_coords: set of (row, col) neighboring the filled region but not part of it.
        - boundary_reached: boolean indicating if the fill touched the grid edge.
    """
    rows, cols = grid.shape
    
    # Ensure start pos is valid and traversable
    start_r, start_c = start_pos
    if not (0 <= start_r < rows and 0 <= start_c < cols):
         # Should not happen if called correctly
         return set(), set(), False 
    if grid[start_r, start_c] not in traversable_colors:
         # Start point itself isn't traversable (e.g., starting on the border color)
         # In this implementation, we expect start point to be traversable.
         # If we start on C_inner for the second fill, C_inner *must* be in traversable_colors.
         # Let's assume valid calls. If start not traversable, it fills nothing.
         return set(), {start_pos}, False # Adjacent is just the start pos itself

    q = deque([start_pos])
    visited = {start_pos}
    filled_coords = {start_pos}
    adjacent_coords = set()
    boundary_reached = False

    # Check if start position itself is on the boundary
    if start_r == 0 or start_r == rows - 1 or start_c == 0 or start_c == cols - 1:
        # Starting on the boundary means boundary is trivially reached *if* fill can move.
        boundary_reached = True

    while q:
        r, c = q.popleft()

        # Check neighbors (4-connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is out of bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                boundary_reached = True
                continue # Don't process out-of-bounds coordinates further

            # Process in-bounds neighbor
            neighbor_pos = (nr, nc)
            if neighbor_pos not in visited:
                visited.add(neighbor_pos)
                neighbor_color = grid[nr, nc]

                # If neighbor is traversable, add to queue and filled set
                if neighbor_color in traversable_colors:
                    q.append(neighbor_pos)
                    filled_coords.add(neighbor_pos)
                    # Check if this newly added traversable cell is on boundary
                    if nr == 0 or nr == rows - 1 or nc == 0 or nc == cols - 1:
                        boundary_reached = True
                # If neighbor is not traversable, add to adjacent set
                else:
                    adjacent_coords.add(neighbor_pos)

    return filled_coords, adjacent_coords, boundary_reached


def transform(input_grid_list):
    """
    Main transformation function. Applies the conditional color change based on nested object colors.

    Args:
        input_grid_list: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    # Start with a copy that will be modified if conditions are met
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # --- Step 1: Locate Target ---
    magenta_pixels = find_pixel(output_grid, 6)
    if len(magenta_pixels) != 1:
        # If not exactly one magenta pixel, return the original input
        return input_grid_list
    target_pos = magenta_pixels[0]

    # --- Step 2: Check Innermost Containment ---
    # Flood fill from target, allowed to move through background (0) and target color (6).
    # This identifies the space immediately around the target pixel(s) inside the first barrier.
    fill1_coords, adjacent1_coords, boundary1_reached = flood_fill(
        output_grid, target_pos, {0, 6}
    )

    # If the first fill reaches the boundary, the target pixel is not enclosed.
    if boundary1_reached:
        return input_grid_list

    # Determine the color of the immediate enclosing object (must be unique non-zero).
    neighbor1_colors = get_unique_colors(output_grid, adjacent1_coords)
    if len(neighbor1_colors) != 1:
        # Needs exactly one enclosing color. If 0 or >1, no clear inner object found.
        return input_grid_list
    C_inner = list(neighbor1_colors)[0]

    # --- Step 3: Check Next Outer Containment ---
    # Find a starting point for the second fill. This point should be on the border
    # identified previously, and have the color C_inner.
    start_pos2 = None
    for r_adj, c_adj in adjacent1_coords:
        if output_grid[r_adj, c_adj] == C_inner:
            start_pos2 = (r_adj, c_adj)
            break

    # If no suitable starting point found (should be impossible if C_inner was valid).
    if start_pos2 is None:
        # This indicates a potential logic error or unexpected grid structure
        # Safest is to return original grid.
        return input_grid_list

    # Perform the second fill, starting from the inner object's border.
    # Allow traversal through background (0) and the inner object's color (C_inner).
    # This identifies the space between the inner and outer objects.
    fill2_coords, adjacent2_coords, boundary2_reached = flood_fill(
        output_grid, start_pos2, {0, C_inner}
    )

    # If the second fill reaches the boundary, the C_inner object is not enclosed.
    if boundary2_reached:
        return input_grid_list

    # Determine the color of the next enclosing object (must be unique non-zero).
    neighbor2_colors = get_unique_colors(output_grid, adjacent2_coords)
    if len(neighbor2_colors) != 1:
         # Needs exactly one outer enclosing color.
        return input_grid_list
    C_outer = list(neighbor2_colors)[0]

    # --- Step 4: Evaluate Condition ---
    condition_met = False
    # Check for Yellow (4) inside Red (2)
    if C_inner == 4 and C_outer == 2:
        condition_met = True
    # Check for Blue (1) inside Green (3)
    elif C_inner == 1 and C_outer == 3:
        condition_met = True

    # --- Step 5: Apply Transformation ---
    if condition_met:
        # Modify the output grid by changing the target pixel's color to white (0)
        r_target, c_target = target_pos
        output_grid[r_target, c_target] = 0
        # Return the modified grid
        return output_grid.tolist()
    else:
        # If condition not met, return the original unchanged input grid
        return input_grid_list