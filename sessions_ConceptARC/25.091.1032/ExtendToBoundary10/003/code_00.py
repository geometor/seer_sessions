import numpy as np
from collections import deque

"""
Transformation Rule:
1. Create a copy of the input grid for the output.
2. Identify all yellow (4) pixels in the input grid. Determine the largest connected component (using 4-way adjacency) formed by these pixels - this constitutes the 'main boundary'. Store the coordinates of these boundary pixels.
3. If a main boundary exists, calculate its minimum and maximum row indices (`min_boundary_row`, `max_boundary_row`).
4. Identify all orange (7) 'seed' pixels in the input grid.
5. For each seed pixel at `(r, c)`:
    a. Set the pixel `(r, c)` in the output grid to orange (7).
    b. Determine the fill direction based on the seed's row `r` relative to the main boundary's row span:
        - If a boundary exists and `min_boundary_row <= r <= max_boundary_row`, the fill is horizontal.
        - Otherwise (boundary doesn't exist, or `r` is outside the span), the fill is vertical.
    c. Perform ray casting fill along the determined axis:
        - **Horizontal Fill:**
            - Cast left from `(r, c-1)`: Change white (0) pixels in the input to orange (7) in the output until a main boundary pixel or the left grid edge is hit.
            - Cast right from `(r, c+1)`: Change white (0) pixels in the input to orange (7) in the output until a main boundary pixel or the right grid edge is hit.
        - **Vertical Fill:**
            - If `r < min_boundary_row` (or no boundary): Cast *downwards* from `(r+1, c)`. Change white (0) pixels to orange (7) until a main boundary pixel or the bottom grid edge is hit.
            - If `r > max_boundary_row` (or no boundary): Cast *upwards* from `(r-1, c)`. Change white (0) pixels to orange (7) until a main boundary pixel or the top grid edge is hit.
            - *Note:* The examples suggest seeds outside the boundary only fill towards the boundary.
6. Return the modified output grid.
"""

def find_largest_connected_component(grid, target_color):
    """Finds the coordinates of the largest connected component (4-way adjacency) of a given color."""
    height, width = grid.shape
    visited = set()
    largest_component_coords = set()

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and (r, c) not in visited:
                current_component_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                current_component_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 4 neighbors (von Neumann)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == target_color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            current_component_coords.add((nr, nc))
                            q.append((nr, nc))

                if len(current_component_coords) > len(largest_component_coords):
                    largest_component_coords = current_component_coords

    return largest_component_coords

def get_row_span(component_coords):
    """Calculates the min and max row indices for a set of coordinates."""
    if not component_coords:
        return -1, -1 # Indicate no component found or empty component
    rows = [r for r, c in component_coords]
    return min(rows), max(rows)

def transform(input_grid):
    """Applies the directional ray-cast fill transformation."""
    
    # Convert to numpy array for easier manipulation
    input_arr = np.array(input_grid, dtype=int)
    # Create a copy to modify for the output
    output_arr = np.copy(input_arr)
    height, width = input_arr.shape

    # Define colors
    WHITE = 0
    YELLOW = 4
    ORANGE = 7

    # --- Step 2: Identify the largest yellow component (main boundary) ---
    main_boundary_coords = find_largest_connected_component(input_arr, YELLOW)

    # --- Step 3: Calculate the boundary's row span ---
    min_boundary_row, max_boundary_row = get_row_span(main_boundary_coords)
    boundary_exists = bool(main_boundary_coords) # True if the set is not empty

    # --- Step 4: Find all orange seed pixels ---
    seed_coords = []
    for r in range(height):
        for c in range(width):
            if input_arr[r, c] == ORANGE:
                seed_coords.append((r, c))

    # --- Step 5: Process each seed pixel ---
    for r_seed, c_seed in seed_coords:
        
        # --- Step 5a: Ensure seed pixel is orange in output ---
        output_arr[r_seed, c_seed] = ORANGE

        # --- Step 5b: Determine fill type (Horizontal or Vertical) ---
        is_horizontal_fill = False
        if boundary_exists and min_boundary_row <= r_seed <= max_boundary_row:
            is_horizontal_fill = True

        # --- Step 5c: Perform ray casting fill ---
        if is_horizontal_fill:
            # Fill Left
            for c in range(c_seed - 1, -1, -1):
                current_coord = (r_seed, c)
                if current_coord in main_boundary_coords:
                    break # Stop at boundary
                # Check the *input* array for white, modify the *output* array
                if input_arr[r_seed, c] == WHITE:
                    output_arr[r_seed, c] = ORANGE
                # Note: Based on analysis, fill continues through non-white, non-boundary pixels.
                # If it should stop at any non-white, add: elif input_arr[r_seed, c] != WHITE: break

            # Fill Right
            for c in range(c_seed + 1, width):
                current_coord = (r_seed, c)
                if current_coord in main_boundary_coords:
                    break # Stop at boundary
                if input_arr[r_seed, c] == WHITE:
                    output_arr[r_seed, c] = ORANGE
                # elif input_arr[r_seed, c] != WHITE: break

        else: # Vertical Fill (Directional)
            # Determine direction based on seed position relative to boundary
            fill_up = False
            fill_down = False

            if not boundary_exists:
                 # If no boundary, maybe fill both ways? Let's assume fill both based on lack of constraint.
                 # However, examples had boundaries. Let's stick to example-driven logic first.
                 # Refined logic: If outside boundary, fill *towards* boundary.
                 pass # No fill if no boundary and seed isn't inside hypothetical span? Seems unlikely.
                 # Let's assume the task implies a boundary exists if vertical fill happens.
                 # Revisit if a test case without boundary appears.
            elif r_seed < min_boundary_row:
                fill_down = True
            elif r_seed > max_boundary_row:
                fill_up = True
            # If r_seed is on the boundary row but outside the horizontal span logic
            # this 'else' branch wouldn't be reached due to the `is_horizontal_fill` check.

            # Fill Upwards (if applicable)
            if fill_up:
                for r in range(r_seed - 1, -1, -1):
                    current_coord = (r, c_seed)
                    if current_coord in main_boundary_coords:
                        break # Stop at boundary
                    if input_arr[r, c_seed] == WHITE:
                        output_arr[r, c_seed] = ORANGE
                    # elif input_arr[r, c_seed] != WHITE: break

            # Fill Downwards (if applicable)
            if fill_down:
                 for r in range(r_seed + 1, height):
                    current_coord = (r, c_seed)
                    if current_coord in main_boundary_coords:
                        break # Stop at boundary
                    if input_arr[r, c_seed] == WHITE:
                        output_arr[r, c_seed] = ORANGE
                    # elif input_arr[r, c_seed] != WHITE: break


    # --- Step 6: Return the final grid ---
    # Convert back to list of lists for the required output format
    return output_arr.tolist()