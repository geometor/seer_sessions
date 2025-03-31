import numpy as np
from collections import deque

"""
Transforms the input grid based on partitioning relative to blue(1) walls, 
following a hybrid approach combining reachability and adjacency.

1.  Partition the grid into 'reachable' (from border, avoiding blue walls) and 
    'enclosed' (not reachable) areas using BFS. Blue pixels are 'walls'.
2.  Categorize non-white(0), non-blue(1) 'active pixels':
    - 'Internal Influencers': Active pixels that are either NOT reachable OR 
      are 4-directionally adjacent to any blue pixel.
    - 'External Seeds': Active pixels that ARE reachable AND are NOT 
      4-directionally adjacent to any blue pixel.
3.  Categorize white(0) pixels:
    - 'Reachable White': White(0) reachable by BFS.
    - 'Enclosed White': White(0) not reachable by BFS.
4.  Determine Wall Color: Walls (blue pixels) become Red(2) if any 
    'Internal Influencer' is Red(2); otherwise, they become Azure(8).
5.  Determine Fill Color: 'Enclosed White' pixels are filled based on the colors 
    of 'Internal Influencers' (priority: Green(3) > Magenta(6) > Azure(8)). 
    Defaults to Azure(8).
6.  Fill Reachable Area: 'Reachable White' pixels are filled using Voronoi 
    tessellation based on 'External Seeds' (Manhattan distance, tie-break by 
    row then column).
7.  Active pixels (seeds, influencers) retain their original color unless 
    overwritten by Wall/Fill transformations applied to the initial copy.
"""

def _find_reachable_pixels(grid):
    """
    Finds pixels reachable from the border without crossing blue (1) pixels.
    Uses Breadth-First Search (BFS) on non-blue cells starting from the border.
    Blue pixels themselves are marked as not reachable.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: A boolean mask where True indicates a reachable pixel.
    """
    rows, cols = grid.shape
    reachable_mask = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Add border cells that are not blue (1) to the queue and mark reachable
    for r in range(rows):
        if grid[r, 0] != 1 and not reachable_mask[r, 0]:
            queue.append((r, 0))
            reachable_mask[r, 0] = True
        if grid[r, cols - 1] != 1 and not reachable_mask[r, cols - 1]:
            queue.append((r, cols - 1))
            reachable_mask[r, cols - 1] = True
    for c in range(1, cols - 1): # Avoid double-adding corners
        if grid[0, c] != 1 and not reachable_mask[0, c]:
            queue.append((0, c))
            reachable_mask[0, c] = True
        if grid[rows - 1, c] != 1 and not reachable_mask[rows - 1, c]:
            queue.append((rows - 1, c))
            reachable_mask[rows - 1, c] = True

    # Perform BFS, only moving through non-blue cells
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Check bounds, if NOT blue, and if NOT already visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] != 1 and not reachable_mask[nr, nc]:
                   reachable_mask[nr, nc] = True
                   queue.append((nr, nc))
                   
    # Ensure blue pixels are explicitly marked as not reachable by this mask
    reachable_mask[grid == 1] = False
    return reachable_mask

def _get_neighbors(pos, rows, cols):
    """Gets 4-directional neighbors within grid bounds."""
    r, c = pos
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def _manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid):
    """
    Applies the transformation rules described in the module docstring.
    """
    # Initialization
    grid = np.array(input_grid)
    output_grid = np.copy(grid) # Start with a copy
    rows, cols = grid.shape

    # 1. Identify Reachable Area
    reachable_mask = _find_reachable_pixels(grid)

    # 2. Categorize Pixels & Identify Influencers/Seeds
    internal_influencers = []
    external_seeds = []
    has_red_influencer = False

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            pos = (r, c)

            # Skip walls and white pixels for influencer/seed categorization
            if color == 1 or color == 0:
                continue

            # It's an active pixel (non-0, non-1)
            is_reachable = reachable_mask[r, c]
            
            # Check adjacency to blue walls
            is_adjacent_to_blue = False
            for nr, nc in _get_neighbors(pos, rows, cols):
                if grid[nr, nc] == 1:
                    is_adjacent_to_blue = True
                    break
            
            pixel_info = {'pos': pos, 'color': color}

            # Apply categorization logic (Strategy 3.0)
            if not is_reachable or is_adjacent_to_blue:
                internal_influencers.append(pixel_info)
                if color == 2: # Check for Red(2) influencer
                    has_red_influencer = True
            else: # Reachable AND not adjacent to blue
                external_seeds.append(pixel_info)

    # 4. Determine Wall Transformation Color
    wall_color = 2 if has_red_influencer else 8

    # 5. Determine Enclosed Fill Color
    internal_colors_set = set(p['color'] for p in internal_influencers)
    fill_color = 8 # Default Azure
    if 3 in internal_colors_set: # Green priority
        fill_color = 3
    elif 6 in internal_colors_set: # Magenta priority
        fill_color = 6
    elif 8 in internal_colors_set: # Azure priority
        fill_color = 8
    # If none of the priority colors are present, it stays Azure(8)

    # 6. Apply Transformations to Output Grid
    for r in range(rows):
        for c in range(cols):
            input_color = grid[r, c]
            
            if input_color == 1: # Original blue wall pixel
                output_grid[r, c] = wall_color
            elif input_color == 0: # Original white pixel
                is_reachable = reachable_mask[r, c]
                if not is_reachable: # Enclosed White
                    output_grid[r, c] = fill_color
                else: # Reachable White - Apply Voronoi Fill
                    if not external_seeds:
                        # If there are reachable white pixels but no seeds,
                        # behavior is undefined by examples. Keep original (0)
                        # or default? Let's default to black/background for now.
                        # Based on examples, this case likely won't happen if
                        # reachable white exists.
                        # Let's assume seeds exist if reachable_white exists.
                        # If somehow seeds list is empty, this code will error.
                        # We could add a check: if not external_seeds: output_grid[r,c]=0; continue
                         pass # If no seeds, keep white (or maybe fill_color? default to 0 seems safest)

                    else:
                        min_dist = float('inf')
                        nearest_seeds = []
                        for seed in external_seeds:
                            dist = _manhattan_distance((r, c), seed['pos'])
                            if dist < min_dist:
                                min_dist = dist
                                nearest_seeds = [seed]
                            elif dist == min_dist:
                                nearest_seeds.append(seed)

                        # Tie-breaking: lowest row, then lowest column
                        best_seed = min(nearest_seeds, key=lambda s: (s['pos'][0], s['pos'][1]))
                        output_grid[r, c] = best_seed['color']
            # Else: Active pixel (non-0, non-1) - already copied correctly initially

    # Return result as list of lists
    return output_grid.tolist()