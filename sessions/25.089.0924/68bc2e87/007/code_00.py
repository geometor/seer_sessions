import numpy as np
from collections import deque

"""
Identifies nested layers of colors in a grid, starting from the outermost layer adjacent to the initial 
azure (8) or white (0) background pixels, and proceeds inwards. The colors of these layers are collected 
in order and returned as a single-column grid.

The transformation uses a Breadth-First Search (BFS) approach to iteratively expand an 'outside' region:
1. Initialize an 'outside' region comprising all azure (8) and white (0) pixels. Mark these as visited 
   and add them to a queue for the first BFS expansion.
2. Iteratively perform BFS rounds:
   a. Start a BFS using the pixels queued from the previous round (or the initial background).
   b. During the BFS, explore neighbors of pixels from the queue.
   c. If an unvisited neighbor is background (8/0), mark it visited and queue it for the *next* BFS round.
   d. If an unvisited neighbor is colored (not 8/0), and no colored neighbor has been identified *in this round yet*, 
      record its color and position as the 'next layer candidate'. Mark it visited. Do not queue colored pixels 
      during the BFS expansion itself.
   e. Continue the BFS until the current queue is empty, ensuring all reachable background pixels for the next round are queued.
3. After a BFS round completes:
   a. If a 'next layer candidate' was found:
      i. Record the layer's color.
      ii. Perform a flood fill (using a helper function) starting from the candidate pixel to find all connected pixels 
         of the same color (the complete layer object).
      iii. Ensure all pixels of this object are marked as visited.
      iv. Add all pixels of the found layer object to the queue for the *next* BFS round.
   b. If no 'next layer candidate' was found and the queue for the next round is empty, the process terminates.
4. Format the collected layer colors into a single-column NumPy array.
"""

def find_connected_object(grid, start_r, start_c, target_color, visited_global):
    """
    Finds all connected pixels of a target_color starting from (start_r, start_c) using BFS,
    considering 8-way adjacency. It only explores pixels of the target_color and avoids
    pixels already in visited_global.

    Args:
        grid (np.ndarray): The grid to search within.
        start_r (int): Starting row.
        start_c (int): Starting column.
        target_color (int): The color of the object to find.
        visited_global (set): The set of globally visited pixels to avoid re-exploring.

    Returns:
        set: A set of (row, col) tuples representing the pixels of the connected object.
    """
    height, width = grid.shape
    object_pixels = set()
    
    # Check if start pixel is valid and not already visited by the main BFS
    if not (0 <= start_r < height and 0 <= start_c < width) or grid[start_r, start_c] != target_color:
         return object_pixels # Invalid start

    queue = deque([(start_r, start_c)])
    # Keep track of visited pixels *during this flood fill* to avoid cycles within the object
    visited_local = set([(start_r, start_c)]) 

    while queue:
        r, c = queue.popleft()
        object_pixels.add((r, c))

        # Explore 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                pixel = (nr, nc)

                # Check bounds, color match, and if not visited *locally in this flood fill*
                if 0 <= nr < height and 0 <= nc < width and \
                   grid[nr, nc] == target_color and \
                   pixel not in visited_local:
                    
                    visited_local.add(pixel)
                    queue.append(pixel)

    return object_pixels


def transform(input_grid):
    """
    Transforms the input grid by finding nested colored layers and outputting their colors in order.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        numpy.ndarray: A 2D NumPy array representing the output grid (single column).
    """
    working_grid = np.array(input_grid, dtype=int)
    height, width = working_grid.shape
    nested_colors = []
    
    # visited tracks all pixels globally (initial background + processed layers)
    visited = set() 
    
    # current_q stores pixels for the *current* BFS expansion boundary
    current_q = deque()

    # 1. Initialize visited set and queue with all initial azure (8) and white (0) pixels
    for r in range(height):
        for c in range(width):
            if working_grid[r, c] == 8 or working_grid[r, c] == 0:
                if (r, c) not in visited:
                    visited.add((r, c))
                    current_q.append((r, c))

    # 2. Main loop: process one layer per iteration
    while current_q: # Loop as long as there are boundary pixels to expand from
        next_q = deque() # Queue for the *next* iteration's boundary
        next_layer_candidate = None # Stores (color, (r, c))
        
        # Use a temporary queue for the BFS expansion to not consume current_q prematurely
        bfs_q = current_q 
        
        # Track pixels added to next_q *during this iteration* (BFS + flood fill) 
        # to prevent duplicates in next_q. Add initial boundary to avoid re-adding later.
        processed_this_iteration = set(current_q) 

        # --- BFS Expansion Phase ---
        while bfs_q:
            r, c = bfs_q.popleft()

            # Explore 8 neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    pixel = (nr, nc)

                    # Check bounds and if neighbor has *not* been globally visited yet
                    if 0 <= nr < height and 0 <= nc < width and pixel not in visited:
                        # Mark as globally visited immediately
                        visited.add(pixel) 
                        
                        neighbor_color = working_grid[nr, nc]

                        if neighbor_color == 8 or neighbor_color == 0:
                            # Background pixel: Add to next round's queue if not already processed this iteration
                            if pixel not in processed_this_iteration:
                                next_q.append(pixel)
                                processed_this_iteration.add(pixel)
                        else:
                            # Colored pixel: Potential layer candidate
                            if next_layer_candidate is None:
                                next_layer_candidate = (neighbor_color, pixel)
                            # Do not add colored pixels to next_q here.
                            # Ensure it's marked processed for this iteration even if not the candidate
                            processed_this_iteration.add(pixel)

        # --- Layer Processing Phase ---
        if next_layer_candidate is not None:
            layer_color, start_pixel = next_layer_candidate
            nested_colors.append(layer_color)

            # Find all pixels of this layer object using flood fill
            # Pass the global visited set to the helper? No, flood fill should only care about target color.
            # The global visited set prevents the BFS from *finding* the start_pixel again.
            object_pixels = find_connected_object(working_grid, start_pixel[0], start_pixel[1], layer_color, visited)

            # Absorb the object into the 'outside' region for the next iteration
            for r_obj, c_obj in object_pixels:
                # Ensure globally visited (might be redundant if BFS marked start_pixel, but safe)
                visited.add((r_obj, c_obj)) 
                # Add all object pixels to the queue for the *next* BFS expansion
                # if not already processed this iteration (e.g., by the BFS itself)
                if (r_obj, c_obj) not in processed_this_iteration:
                     next_q.append((r_obj, c_obj))
                     processed_this_iteration.add((r_obj, c_obj))
        
        # Update queue for the next iteration
        current_q = next_q

        # Termination check: If no candidate was found AND the next queue is empty, 
        # it means the BFS expanded fully into background without hitting a new color boundary.
        if next_layer_candidate is None and not current_q:
             break


    # 3. Format the output
    if not nested_colors:
        output_grid = np.empty((0, 1), dtype=int)
    else:
        output_grid = np.array(nested_colors, dtype=int).reshape(-1, 1)

    return output_grid