import numpy as np
from collections import deque
import collections

"""
Transforms the input grid by propagating colors from the middle of each border 
inwards into a background region, respecting obstacle pixels.

The transformation logic is as follows:
1. Identify the colors present at the midpoint of the top, right, bottom, and left borders.
2. Analyze the inner area of the grid (excluding the 1-pixel border) to determine:
   - The background color: The single most frequent color in the inner area. If there's a tie 
     for the most frequent color, or if the inner area is empty or uniform, the transformation
     cannot proceed, and the original grid is returned.
   - Obstacle colors: All other colors present in the inner area besides the background color.
3. Perform a simultaneous Breadth-First Search (BFS) starting from all background-colored pixels 
   that are adjacent to the border.
4. Each border source (Top, Right, Bottom, Left) attempts to expand into adjacent, 
   connected background pixels.
5. Propagation Rules:
   - Expansion only occurs into pixels that originally had the background color.
   - Obstacle pixels block the expansion.
   - The 1-pixel border remains unchanged.
   - When expansions from different sources reach the same background pixel during the same 
     BFS layer (i.e., at the same distance from their respective borders), a conflict occurs.
   - Conflicts are resolved based on a fixed priority: Top > Right > Bottom > Left. The 
     expansion from the higher-priority source colors the pixel.
   - Pixels (background or obstacles) that are not reached by any expansion wave retain 
     their original color.
"""

def find_inner_elements(grid):
    """
    Analyzes the inner area (excluding the 1-pixel border) of the grid 
    to find the background color (most frequent) and the obstacle colors 
    (all other colors present in the inner area).

    Args:
        grid (np.array): The input grid.

    Returns:
        tuple: (background_color, obstacle_colors_set)
               Returns (None, set()) if the inner area is empty, cannot be analyzed,
               contains only one color (no obstacles), or contains multiple colors 
               with a tie for the most frequent (ambiguous background).
    """
    h, w = grid.shape
    # Ensure there's an inner area to analyze
    if h <= 2 or w <= 2:
        return None, set() 
        
    inner_grid = grid[1:h-1, 1:w-1]
    
    # Check if inner grid is actually empty after slicing
    if inner_grid.size == 0:
        return None, set()

    colors, counts = np.unique(inner_grid, return_counts=True)
    
    if len(colors) <= 1: 
         # Need at least one background and one obstacle color for the process
         # Or, if only one color, it's background, but no obstacles to define regions.
         # The problem seems to imply distinct background and obstacle regions.
         return None, set() 
         
    # Multiple colors found, assume background is the most frequent
    count_map = collections.OrderedDict(sorted(zip(colors, counts), key=lambda item: item[1], reverse=True)) # Sort by count descending
    
    # Check for ties in the highest count
    sorted_counts = sorted(counts, reverse=True)
    if len(sorted_counts) > 1 and sorted_counts[0] == sorted_counts[1]:
         # Ambiguous background color due to tie
         return None, set() 

    # Background is the color with the unique highest count
    background_color = list(count_map.keys())[0]
                 
    # Obstacles are all colors that are not the background color
    obstacle_colors = set(c for c in colors if c != background_color)
                 
    return background_color, obstacle_colors

def transform(input_grid_list):
    """
    Applies the border color propagation transformation to the input grid.

    Args:
        input_grid_list (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = input_grid.copy()
    h, w = input_grid.shape

    # --- Handle edge case: grid too small for an inner area ---
    if h <= 2 or w <= 2:
        return output_grid.tolist() # No inner area to propagate into

    # --- 1. Identify Border Colors ---
    # Use the middle pixel of each edge as the source color for that side.
    # Integer division // handles both even and odd dimensions correctly for midpoint.
    c_mid = w // 2
    r_mid = h // 2
    # Store border colors in the processing order for collision resolution (T, R, B, L)
    border_colors = [
        input_grid[0, c_mid],       # 0: Top
        input_grid[r_mid, w - 1],   # 1: Right
        input_grid[h - 1, c_mid],   # 2: Bottom
        input_grid[r_mid, 0]        # 3: Left
    ]

    # --- 2. Identify Inner Background and Obstacles ---
    background_color, obstacle_colors = find_inner_elements(input_grid)
    
    # If no clear background color or no obstacles found, return original grid
    if background_color is None: 
         return output_grid.tolist() 

    # --- 3. Initialize Propagation Structures ---
    queues = [deque() for _ in range(4)] # T, R, B, L queues
    # visited array also stores the source index + 1 (1=T, 2=R, 3=B, 4=L)
    # 0 means not visited, > 0 means visited by source (value - 1)
    visited = np.zeros(input_grid.shape, dtype=int) 
    
    # Mark border as visited (cannot be overwritten, cannot propagate from/to)
    # Use a value unlikely to be a source index + 1, e.g., 99
    visited[0, :] = 99
    visited[-1, :] = 99
    visited[:, 0] = 99
    visited[:, -1] = 99
    
    # Mark initial obstacles as visited (block propagation)
    for r in range(1, h - 1):
        for c in range(1, w - 1):
            if input_grid[r, c] in obstacle_colors:
                visited[r, c] = 99 # Mark obstacles

    # --- 4. Seed Propagation ---
    # Add initial background pixels adjacent to borders to queues and mark as visited by source.
    # Process in T, R, B, L order for deterministic seeding at corners/edges.
    
    # Top seed (row 1)
    source_index = 0 # Top
    r_seed = 1
    for c in range(1, w - 1):
        if visited[r_seed, c] == 0 and input_grid[r_seed, c] == background_color:
            visited[r_seed, c] = source_index + 1
            queues[source_index].append((r_seed, c))

    # Right seed (column w-2)
    source_index = 1 # Right
    c_seed = w - 2
    for r in range(1, h - 1):
         if visited[r, c_seed] == 0 and input_grid[r, c_seed] == background_color:
            # Only seed if not already seeded by Top (higher priority)
            visited[r, c_seed] = source_index + 1 
            queues[source_index].append((r, c_seed))
            
    # Bottom seed (row h-2)
    source_index = 2 # Bottom
    r_seed = h - 2
    for c in range(1, w - 1):
         if visited[r_seed, c] == 0 and input_grid[r_seed, c] == background_color:
             # Check higher priorities (T, R)
            visited[r_seed, c] = source_index + 1
            queues[source_index].append((r_seed, c))

    # Left seed (column 1)
    source_index = 3 # Left
    c_seed = 1
    for r in range(1, h - 1):
         if visited[r, c_seed] == 0 and input_grid[r, c_seed] == background_color:
             # Check higher priorities (T, R, B)
            visited[r, c_seed] = source_index + 1
            queues[source_index].append((r, c_seed))

    # --- 5. Iterative Propagation (Simultaneous BFS Layer by Layer) ---
    active_queues = True
    while active_queues:
        active_queues = False # Assume no propagation happens in this layer
        coords_to_process_next = [[] for _ in range(4)] # Collect coords for next layer

        # Process queues layer by layer, respecting priority T > R > B > L
        for i in range(4): # 0:T, 1:R, 2:B, 3:L
            q = queues[i]
            source_color = border_colors[i]
            
            processed_in_this_source = len(q) > 0 # Flag if this source had nodes
            if processed_in_this_source:
                 active_queues = True # Mark that work was done in this layer

            while q:
                r, c = q.popleft()
                # Color the pixel in the output grid
                output_grid[r, c] = source_color

                # Explore orthogonal neighbors
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc

                    # Check bounds (already implicitly handles border check due to visited init)
                    # Check if neighbor is unvisited (value 0) background pixel
                    if visited[nr, nc] == 0 and input_grid[nr, nc] == background_color:
                        visited[nr, nc] = i + 1 # Mark visited by this source
                        coords_to_process_next[i].append((nr, nc)) # Add to next layer list

        # Update queues for the next layer
        for i in range(4):
            queues[i].clear()
            queues[i].extend(coords_to_process_next[i])

    # --- 6. Return the final grid ---
    # output_grid contains original border, obstacles, unreached background, and filled areas.
    return output_grid.tolist()