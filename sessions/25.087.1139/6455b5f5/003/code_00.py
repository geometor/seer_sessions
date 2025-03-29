import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid based on the following rules:
    1. Red (2) pixels remain unchanged.
    2. Identify connected regions (components) of white (0) pixels.
    3. Determine which white pixels are 'border-reachable' by performing a flood fill (BFS)
       starting from all white pixels on the grid's border, treating red pixels as barriers.
    4. For each white component:
       a. Check if it's adjacent (4-directionally) to any red pixel.
       b. If not adjacent to red, it remains white (0).
       c. If adjacent to red:
          i. Check if any pixel within the component is 'border-reachable'.
          ii. If any part of the component is border-reachable, fill the entire component with blue (1).
          iii. If no part of the component is border-reachable (enclosed), fill the entire component with azure (8).
    """

    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # --- Step 3: Determine border reachability for all white pixels ---
    is_border_reachable = np.zeros_like(input_grid_np, dtype=bool)
    visited_reachability = np.zeros_like(input_grid_np, dtype=bool) # Track visited for reachability BFS
    q_reachability = deque()

    # Add all white border pixels to the queue and mark them as visited
    for r in range(height):
        for c in [0, width - 1]: # Left and Right borders
            if input_grid_np[r, c] == 0 and not visited_reachability[r, c]:
                q_reachability.append((r, c))
                visited_reachability[r, c] = True
    for c in range(width):
        for r in [0, height - 1]: # Top and Bottom borders
             if input_grid_np[r, c] == 0 and not visited_reachability[r, c]:
                q_reachability.append((r, c))
                visited_reachability[r, c] = True

    # Perform BFS to find all border-reachable white pixels
    while q_reachability:
        r, c = q_reachability.popleft()
        is_border_reachable[r, c] = True # Mark the current pixel as reachable

        # Check 4-directional neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds, if white, and not visited for reachability
            if 0 <= nr < height and 0 <= nc < width and \
               input_grid_np[nr, nc] == 0 and not visited_reachability[nr, nc]:
                visited_reachability[nr, nc] = True
                q_reachability.append((nr, nc))

    # --- Step 4: Identify white components, check adjacency & reachability, and fill ---
    visited_component = np.zeros_like(input_grid_np, dtype=bool) # Track visited for component BFS

    for r in range(height):
        for c in range(width):
            # If it's a white pixel and hasn't been visited as part of a component yet
            if input_grid_np[r, c] == 0 and not visited_component[r, c]:

                component_pixels = []
                is_adjacent_to_red = False
                component_is_reachable = False # Tracks if *any* pixel in the component is border reachable

                comp_q = deque([(r, c)])
                visited_component[r, c] = True

                # BFS to find the current white component and its properties
                while comp_q:
                    cr, cc = comp_q.popleft()
                    component_pixels.append((cr, cc))

                    # Check if this specific pixel is border-reachable
                    if is_border_reachable[cr, cc]:
                        component_is_reachable = True # Mark the whole component reachable if any part is

                    # Check neighbors for adjacency to red and other white pixels for expansion
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = cr + dr, cc + dc

                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_color = input_grid_np[nr, nc]
                            # Check for adjacent red pixel
                            if neighbor_color == 2:
                                is_adjacent_to_red = True

                            # Check for adjacent white pixel for component expansion
                            elif neighbor_color == 0 and not visited_component[nr, nc]:
                                visited_component[nr, nc] = True
                                comp_q.append((nr, nc))

                # --- Determine fill color and apply ---
                fill_color = 0 # Default is white (no change needed as output is a copy)

                if is_adjacent_to_red:
                    if component_is_reachable:
                        fill_color = 1 # Blue
                    else:
                        fill_color = 8 # Azure

                # Apply the fill color if it's not white
                if fill_color != 0:
                    for pr, pc in component_pixels:
                        output_grid[pr, pc] = fill_color
                # Else: component remains white (already correct in the output_grid copy)

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()