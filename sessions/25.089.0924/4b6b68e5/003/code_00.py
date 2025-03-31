import numpy as np
from collections import Counter, deque

"""
Identifies regions completely enclosed by a single connected boundary component of a uniform color.
For each such enclosed region:
1. Finds all "seed" pixels within the region. Seeds are pixels whose color is not white (0) and not the color of the enclosing boundary.
2. Counts the number of seed pixels (N_seeds).
3. If N_seeds > 1:
    a. Determines the most frequent color among the seeds (C_fill). Ties in frequency are broken by choosing the color with the smallest numerical index.
    b. Flood-fills the entire interior region (including original seeds and white pixels) in the output grid with C_fill.
4. If N_seeds is 0 or 1:
    a. The region remains unchanged in the output grid.
Boundary pixels themselves remain unchanged in all cases.
Pixels not part of any identified enclosed region (e.g., exterior pixels, pixels between boundaries) also remain unchanged.
"""

def get_neighbors(r, c, height, width):
    """Gets 4-directionally adjacent valid neighbor coordinates."""
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < height - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def transform(input_grid):
    """
    Applies the region-based flood fill transformation.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # --- Step 1: Identify all boundary pixels and their connected components ---
    component_map = np.full((height, width), -1, dtype=int) # Maps pixel to component ID
    components = [] # List of sets, each set contains coords of a component
    component_colors = [] # List of colors corresponding to components list
    all_boundary_pixels = set() # Set of all non-white pixel coordinates
    component_id_counter = 0

    for r in range(height):
        for c in range(width):
            color = input_grid_np[r, c]
            if color != 0:
                all_boundary_pixels.add((r, c))
                if component_map[r, c] == -1: # Found start of a new component
                    comp_id = component_id_counter
                    current_component_pixels = set()
                    q = deque([(r, c)])
                    component_map[r, c] = comp_id
                    current_component_pixels.add((r, c))

                    while q:
                        row, col = q.popleft()
                        for nr, nc in get_neighbors(row, col, height, width):
                            if input_grid_np[nr, nc] == color and component_map[nr, nc] == -1:
                                component_map[nr, nc] = comp_id
                                current_component_pixels.add((nr, nc))
                                q.append((nr, nc))
                    
                    components.append(current_component_pixels)
                    component_colors.append(color)
                    component_id_counter += 1

    # --- Step 2: Identify Exterior Pixels ---
    # Pixels reachable from the edge without crossing any boundary pixel
    is_exterior = np.zeros((height, width), dtype=bool)
    q_exterior = deque()

    # Add edge pixels to queue if they are not boundaries
    for r in range(height):
        if (r, 0) not in all_boundary_pixels and not is_exterior[r, 0]:
            is_exterior[r, 0] = True
            q_exterior.append((r, 0))
        if (r, width - 1) not in all_boundary_pixels and not is_exterior[r, width - 1]:
            is_exterior[r, width - 1] = True
            q_exterior.append((r, width - 1))
    for c in range(1, width - 1): # Avoid double-adding corners
        if (0, c) not in all_boundary_pixels and not is_exterior[0, c]:
            is_exterior[0, c] = True
            q_exterior.append((0, c))
        if (height - 1, c) not in all_boundary_pixels and not is_exterior[height - 1, c]:
            is_exterior[height - 1, c] = True
            q_exterior.append((height - 1, c))

    # Flood fill to find all exterior pixels
    while q_exterior:
        r, c = q_exterior.popleft()
        for nr, nc in get_neighbors(r, c, height, width):
            if (nr, nc) not in all_boundary_pixels and not is_exterior[nr, nc]:
                is_exterior[nr, nc] = True
                q_exterior.append((nr, nc))

    # --- Step 3: Find and Process Enclosed Regions ---
    visited_for_regions = np.zeros((height, width), dtype=bool)

    for r in range(height):
        for c in range(width):
            # Potential start of an enclosed region: not boundary, not exterior, not yet processed
            if (r, c) not in all_boundary_pixels and not is_exterior[r, c] and not visited_for_regions[r, c]:
                
                current_region_pixels = set()
                adjacent_boundary_component_ids = set()
                q_region = deque()
                possible_region = True # Flag to check if region touches exterior during BFS

                # Start BFS for the potential region
                q_region.append((r, c))
                visited_for_regions[r, c] = True
                current_region_pixels.add((r, c))

                processed_in_this_bfs = set([(r,c)]) # Track pixels added to queue in this BFS run

                while q_region:
                    rr, cc = q_region.popleft()

                    # Check neighbors
                    for nr, nc in get_neighbors(rr, cc, height, width):
                        neighbor_pos = (nr, nc)
                        
                        if neighbor_pos in all_boundary_pixels:
                            # Found adjacent boundary pixel, record its component ID
                            adjacent_boundary_component_ids.add(component_map[nr, nc])
                        elif not is_exterior[nr, nc]:
                             # If it's an interior/unclassified pixel not yet visited in *this specific* BFS run
                             if neighbor_pos not in processed_in_this_bfs: 
                                visited_for_regions[nr, nc] = True # Mark globally visited
                                current_region_pixels.add(neighbor_pos)
                                q_region.append(neighbor_pos)
                                processed_in_this_bfs.add(neighbor_pos) # Mark visited for this run
                        # else: neighbor is exterior, means this region is not fully enclosed

                # --- Step 4: Analyze the found region ---
                # Check if it was enclosed by exactly one boundary component
                if len(adjacent_boundary_component_ids) == 1:
                    enclosing_comp_id = list(adjacent_boundary_component_ids)[0] # Get the single ID
                    boundary_color = component_colors[enclosing_comp_id]

                    # Identify seed pixels within this confirmed enclosed region
                    seed_pixels = []
                    for pr, pc in current_region_pixels:
                        pixel_color = input_grid_np[pr, pc]
                        if pixel_color != 0 and pixel_color != boundary_color:
                            seed_pixels.append(pixel_color)

                    num_seeds = len(seed_pixels)

                    # Apply transformation rule based on seed count
                    if num_seeds > 1:
                        # Find the most frequent seed color
                        if seed_pixels: # Ensure list is not empty
                             color_counts = Counter(seed_pixels)
                             max_freq = max(color_counts.values())
                             most_frequent_colors = sorted([color for color, count in color_counts.items() if count == max_freq])
                             fill_color = most_frequent_colors[0] # Smallest index tie-breaker

                             # Flood fill the region in the output grid
                             for fr, fc in current_region_pixels:
                                 output_grid[fr, fc] = fill_color
                    # If num_seeds is 0 or 1, do nothing (region remains as copied initially)

    # --- Step 5: Return result ---
    return output_grid.tolist()