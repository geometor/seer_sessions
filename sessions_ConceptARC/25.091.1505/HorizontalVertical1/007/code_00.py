import numpy as np
from collections import deque

"""
Transforms the input grid by filling specific internal white regions (holes) 
based on boundary color, where the fill rule depends on the set of boundary 
colors present globally across all filled holes.

A white region is considered a 'fillable hole' if:
1. It is a connected component (8-way) of white pixels.
2. It is not connected to the grid border via 4-way adjacent white pixels 
   (i.e., it's not part of the outer background).
3. All non-white pixels adjacent (8-way) to any pixel within the hole have 
   the same single color (the boundary color C).
4. No pixel within the hole is adjacent (8-way) to any background white pixel. 
   (This is implicitly covered by checking neighbors during hole identification).

The color used to fill these holes depends on the set S of unique boundary 
colors found across *all* fillable holes in the grid:
- If S = {Red(2), Yellow(4)}, the mapping is Red(2)->Green(3), Yellow(4)->Orange(7).
- If S = {Red(2), Yellow(4), Orange(7)}, the mapping is Red(2)->Orange(7), 
  Yellow(4)->Green(3), Orange(7)->Green(3).
The original boundary shapes remain unchanged.
"""

def get_neighbors(r, c, height, width, connectivity=8):
    """ Gets 8-way (default) or 4-way neighbors within grid bounds. """
    neighbors = []
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)] # 4-way
    if connectivity == 8:
        steps.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)]) # Add diagonals

    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    # Initialize NumPy arrays
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # --- Step 2: Identify background white pixels (connected to border, 4-way) ---
    is_background = np.zeros_like(input_grid_np, dtype=bool)
    q_background = deque()

    # Seed queue with border white pixels
    for r in range(height):
        for c in [0, width - 1]:
            if input_grid_np[r, c] == 0 and not is_background[r, c]:
                is_background[r, c] = True
                q_background.append((r, c))
    for c in range(1, width - 1): # Avoid corners checked twice
         for r in [0, height - 1]:
            if input_grid_np[r, c] == 0 and not is_background[r, c]:
                is_background[r, c] = True
                q_background.append((r, c))

    # Perform BFS for background
    while q_background:
        r, c = q_background.popleft()
        for nr, nc in get_neighbors(r, c, height, width, connectivity=4):
            if input_grid_np[nr, nc] == 0 and not is_background[nr, nc]:
                is_background[nr, nc] = True
                q_background.append((nr, nc))

    # --- Steps 3-6: Identify and filter fillable holes, collect boundary colors ---
    visited = is_background.copy() # Start visited mask including background
    fillable_holes = [] # List to store (list_of_pixels, boundary_color)
    global_boundary_colors = set() # Set of unique boundary colors found

    for r in range(height):
        for c in range(width):
            # Start BFS for potential hole if white, not background, and not visited
            if input_grid_np[r, c] == 0 and not visited[r, c]:
                q_hole = deque([(r, c)])
                visited[r, c] = True
                current_hole_pixels = []
                boundary_colors_found = set() # Colors bordering this specific hole
                hole_visited_local = set([(r,c)]) # Track pixels in this specific hole BFS
                is_valid_hole = True # Assume valid initially

                while q_hole:
                    hr, hc = q_hole.popleft()
                    current_hole_pixels.append((hr, hc))
                    visited[hr, hc] = True # Mark as globally visited

                    # Check 8-way neighbors for boundary conditions
                    for nr, nc in get_neighbors(hr, hc, height, width, connectivity=8):
                        neighbor_coord = (nr, nc)
                        neighbor_color = input_grid_np[nr, nc]

                        if neighbor_color == 0: # White neighbor
                            if neighbor_coord not in hole_visited_local:
                                # Check if it touches background white
                                if is_background[nr, nc]:
                                    is_valid_hole = False # Touches background -> invalid hole
                                    # No need to break here, let BFS finish finding all pixels
                                else:
                                    # Add to queue if it's part of the same hole component
                                    hole_visited_local.add(neighbor_coord)
                                    q_hole.append(neighbor_coord)
                        else: # Non-white neighbor (part of the boundary)
                            boundary_colors_found.add(neighbor_color)

                # Validate the hole after exploring the whole component
                # Condition 3: Single boundary color
                is_single_boundary = len(boundary_colors_found) == 1
                # Condition 4 implicitly checked by is_valid_hole flag (touching background)

                if is_valid_hole and is_single_boundary:
                    # This component is a fillable hole
                    boundary_color = boundary_colors_found.pop() # Get the single boundary color
                    fillable_holes.append((current_hole_pixels, boundary_color))
                    global_boundary_colors.add(boundary_color) # Add to global set

    # --- Step 7: Determine the fill color mapping ---
    fill_map = {}
    global_boundary_colors_set = frozenset(global_boundary_colors)

    # Define known mappings based on training examples
    mapping_rules = {
        frozenset({2, 4}): {2: 3, 4: 7}, # Red(2), Yellow(4) -> Red:Green(3), Yellow:Orange(7)
        frozenset({2, 4, 7}): {2: 7, 4: 3, 7: 3} # Red(2), Yellow(4), Orange(7) -> Red:Orange(7), Yellow:Green(3), Orange:Green(3)
    }

    # Select the appropriate map
    if global_boundary_colors_set in mapping_rules:
        fill_map = mapping_rules[global_boundary_colors_set]

    # --- Step 8: Fill the identified holes in the output grid ---
    if fill_map: # Proceed only if a valid mapping was found
        for hole_pixels, boundary_color in fillable_holes:
            # Check if this specific hole's boundary color has a mapping
            if boundary_color in fill_map:
                fill_color = fill_map[boundary_color]
                # Color the pixels belonging to this hole
                for r_fill, c_fill in hole_pixels:
                    output_grid[r_fill, c_fill] = fill_color

    # --- Step 9: Return the modified grid ---
    return output_grid.tolist()