import numpy as np
from collections import deque

"""
Transformation Rule:

1. Identify the area of white pixels (0) enclosed by a gray frame (5).
2. Fill this enclosed area with concentric layers of colors, starting from the layer adjacent to the gray frame and moving inwards.
3. The fill colors follow a repeating sequence: Red (2), Gray (5), White (0), Gray (5).
4. The original gray frame and any pixels outside the enclosed area remain unchanged.

Process:
1. Copy the input grid to create the output grid.
2. Find all white pixels (0) in the input grid.
3. Perform a flood fill starting from all white pixels located on the border of the grid. Mark all reachable white pixels as 'exterior'.
4. The set of white pixels not marked as 'exterior' constitutes the 'enclosed white pixels'. If this set is empty, return the copied grid.
5. Identify the coordinates of all gray pixels (5) in the input grid; these form the initial boundary for the filling process.
6. Initialize a set `pixels_to_fill` with the coordinates of the enclosed white pixels.
7. Initialize `current_boundary` with the coordinates of the gray frame pixels.
8. Define the fill color sequence: `fill_colors = [2, 5, 0, 5]`.
9. Initialize a layer index `layer_index = 0`.
10. While `pixels_to_fill` is not empty:
    a. Get the color for the current layer: `current_color = fill_colors[layer_index % len(fill_colors)]`.
    b. Find all pixels in `pixels_to_fill` that are adjacent (up, down, left, right) to any pixel in `current_boundary`. Store these in `pixels_for_this_layer`.
    c. If `pixels_for_this_layer` is empty, break the loop (filling is complete or no more reachable pixels).
    d. For each pixel coordinate `(r, c)` in `pixels_for_this_layer`:
        i. Set `output_grid[r, c] = current_color`.
    e. Remove the coordinates in `pixels_for_this_layer` from `pixels_to_fill`.
    f. Update `current_boundary` to be `pixels_for_this_layer`.
    g. Increment `layer_index`.
11. Return the modified `output_grid`.
"""

def find_enclosed_white_pixels(grid):
    """
    Identifies white pixels (0) enclosed within boundaries (non-zero pixels).

    Performs a flood fill starting from border white pixels to find all
    white pixels connected to the outside. The remaining white pixels
    are considered enclosed.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A set of (row, col) tuples representing the coordinates of enclosed
        white pixels. Returns an empty set if none are found.
    """
    rows, cols = grid.shape
    all_white_pixels = set(tuple(p) for p in np.argwhere(grid == 0))
    if not all_white_pixels:
        return set()

    exterior_white = set()
    q = deque()
    visited = set() # Track visited white pixels during flood fill

    # Add border white pixels to queue and mark as visited & exterior
    for r in range(rows):
        if grid[r, 0] == 0 and (r, 0) not in visited:
            q.append((r, 0))
            visited.add((r, 0))
            exterior_white.add((r, 0))
        if grid[r, cols-1] == 0 and (r, cols-1) not in visited:
            q.append((r, cols-1))
            visited.add((r, cols-1))
            exterior_white.add((r, cols-1))
    # Check top/bottom edges (excluding corners already checked)
    for c in range(1, cols - 1):
        if grid[0, c] == 0 and (0, c) not in visited:
            q.append((0, c))
            visited.add((0, c))
            exterior_white.add((0, c))
        if grid[rows-1, c] == 0 and (rows-1, c) not in visited:
            q.append((rows-1, c))
            visited.add((rows-1, c))
            exterior_white.add((rows-1, c))

    # Perform BFS flood fill from border white pixels
    while q:
        r, c = q.popleft()

        # Check 4-directional neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds and if it's a white pixel not yet visited
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                exterior_white.add((nr, nc))
                q.append((nr, nc))

    # Enclosed white pixels are those not reached by the flood fill
    enclosed_white = all_white_pixels - exterior_white
    return enclosed_white


def transform(input_grid):
    """
    Fills an area enclosed by a gray frame with nested layers of colors.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify enclosed white pixels
    enclosed_white_coords = find_enclosed_white_pixels(input_grid)
    if not enclosed_white_coords:
        # No enclosed area found, return the original grid copy
        return output_grid

    # 2. Identify the initial boundary (assuming it's the gray '5' pixels)
    #    We need the gray pixels adjacent to the enclosed area to start.
    #    Alternatively, start the boundary with *all* non-zero pixels surrounding the enclosed area.
    #    Let's stick to the gray pixels as per observation.
    initial_boundary_coords = set(tuple(p) for p in np.argwhere(input_grid == 5))
    
    # If no gray pixels, perhaps another color forms the frame? Check adjacent non-white pixels.
    if not initial_boundary_coords:
         initial_boundary_coords = set()
         for r_w, c_w in enclosed_white_coords:
             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 nr, nc = r_w + dr, c_w + dc
                 if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr, nc] != 0:
                     initial_boundary_coords.add((nr, nc))
         if not initial_boundary_coords:
              # Cannot determine boundary
              return output_grid


    # 3. Initialize sets for the filling process
    pixels_to_fill = set(enclosed_white_coords) # Coordinates of white pixels yet to be colored
    current_boundary = initial_boundary_coords # Start with frame pixels as the outer boundary

    # 4. Define fill colors and layer index
    fill_colors = [2, 5, 0, 5] # Red, Gray, White, Gray
    layer_index = 0

    # 5. Iteratively fill layers
    max_layers = rows * cols # Safety break
    while pixels_to_fill and layer_index < max_layers:
        current_color = fill_colors[layer_index % len(fill_colors)]
        pixels_for_this_layer = set()

        # Find white pixels in 'pixels_to_fill' adjacent to the 'current_boundary'
        # Iterate over a copy because we might modify pixels_to_fill indirectly
        candidates_to_check = list(pixels_to_fill)
        for r, c in candidates_to_check:
            is_adjacent_to_boundary = False
            # Check 4 neighbors
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                # Check bounds and if neighbor is in the current boundary set
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in current_boundary:
                    is_adjacent_to_boundary = True
                    break # Found an adjacent boundary pixel
            
            if is_adjacent_to_boundary:
                # This white pixel is part of the current layer to be colored
                pixels_for_this_layer.add((r, c))

        # If no pixels found for this layer, stop
        if not pixels_for_this_layer:
            break

        # Color the identified pixels in the output grid
        for r, c in pixels_for_this_layer:
            output_grid[r, c] = current_color

        # Update for the next iteration:
        # Remove colored pixels from the set of pixels still needing filling
        pixels_to_fill -= pixels_for_this_layer
        # The newly colored pixels form the boundary for the *next* layer
        current_boundary = pixels_for_this_layer
        # Move to the next layer/color
        layer_index += 1

    # Return the modified grid
    return output_grid