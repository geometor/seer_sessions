```python
"""
Transforms the input grid based on the following rules:

1.  **Initialize:** Start with the input grid. Create a working copy.
2.  **Iterative Connection:**
    *   Repeatedly scan the current working grid:
        *   For each row, identify all pairs of pixels `(r, c1)` and `(r, c2)` (where `c1 < c2`) that have the *same* non-White (0) color `C`.
        *   Check if all pixels in the range `(r, c1+1)` to `(r, c2-1)` are White (0) in the grid's state *at the beginning of the current pass*.
        *   If the path is clear (all White), fill the pixels from `(r, c1+1)` to `(r, c2-1)` with color `C` in the working grid. Mark that a change was made in this pass.
    *   Continue these passes until a full pass completes with no new connections made.
    *   Store the resulting grid as `grid_with_connections`.
3.  **Source Identification and Mapping:**
    *   Refer back to the *original* input grid.
    *   Identify all non-White (0) pixels. These are the "expansion sources". Record their locations `(sr, sc)` and original colors.
    *   Determine global conditions from the *original* input grid:
        *   `has_magenta_source`: True if any identified source has original color Magenta (6).
        *   `has_orange_anywhere`: True if *any* pixel (source or not) in the original grid has color Orange (7).
    *   Create a mapping for how each source's original color determines its expansion color:
        *   If a source's original color is Azure (8) AND `has_magenta_source` is true, its expansion color is Blue (1).
        *   If a source's original color is Magenta (6) AND `has_orange_anywhere` is true, its expansion color is Orange (7).
        *   Otherwise, a source's expansion color is its own original color.
4.  **Simultaneous Expansion (BFS):**
    *   Initialize data structures to track distance from the nearest source and the owner (source coordinate tuple) for each cell, initially marking all as unreached/unowned.
    *   Create a queue for the BFS, initially populated with all source locations `(sr, sc)` found in Step 3, marked with distance 0. Set the owner of each source location to its own coordinate tuple `(sr, sc)`. Sources start expansion regardless of whether their cell was filled by connection.
    *   Process the BFS level by level (incrementing distance):
        *   In each step, determine all potential next cells `(nr, nc)` reachable from the cells processed in the *previous* step.
        *   A cell `(nr, nc)` is a potential target if it is within grid bounds, is White (0) in `grid_with_connections`, and has not yet been reached or contested (`owner[nr, nc]` is `None`).
        *   Keep track of which source(s) (identified by their origin coordinates) attempt to reach each potential target `(nr, nc)` *in this specific step*.
        *   After checking all cells at the current level:
            *   For each potential target `(nr, nc)`:
                *   If exactly one unique source reached it in this step, assign ownership `owner[nr, nc]` to that source's coordinate tuple, record the new distance `distance[nr, nc]`, and add `(nr, nc)` to the queue for the next level.
                *   If multiple *different* sources reached it in this step, mark `owner[nr, nc]` as "CONTESTED". It remains White (0) and does not get added to the queue (acts as an obstacle).
    *   Continue the BFS until the queue is empty.
5.  **Output Construction:**
    *   Start with a copy of `grid_with_connections`.
    *   Iterate through the grid cells `(r, c)`.
    *   If cell `(r, c)` was successfully claimed by a source `(sr, sc)` during the BFS (i.e., `owner[r, c]` is a coordinate tuple), find the corresponding expansion color determined in Step 3 for the source `(sr, sc)` and update the cell `(r, c)` in the final grid to this expansion color.
    *   If the cell `(r, c)` was marked as "CONTESTED", ensure it is White (0) in the final grid (though it should be already if it was eligible for expansion).
    *   Otherwise (if the cell was part of `grid_with_connections` and was never reached or contested), it retains its color from `grid_with_connections`.
    *   Return the final grid.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies the transformation rules involving iterative horizontal connection
    of same-colored pixels and subsequent simultaneous expansion (BFS) with
    color mapping and conflict resolution.
    """
    rows, cols = input_grid.shape
    
    # --- Step 1: Initialize ---
    working_grid = np.copy(input_grid)

    # --- Step 2: Iterative Connection ---
    while True:
        made_connection_in_pass = False
        # Check paths against the state at the beginning of the pass
        grid_at_pass_start = np.copy(working_grid) 

        for r in range(rows):
            # Find indices and colors of non-white pixels in the row (using state at pass start)
            non_white_pixels = {}
            for c in range(cols):
                color = grid_at_pass_start[r, c]
                if color != 0:
                    non_white_pixels[c] = color

            sorted_indices = sorted(non_white_pixels.keys())

            # Iterate through pairs of non-white pixels in the row
            for i in range(len(sorted_indices)):
                for j in range(i + 1, len(sorted_indices)):
                    c1 = sorted_indices[i]
                    c2 = sorted_indices[j]
                    color1 = non_white_pixels[c1]
                    color2 = non_white_pixels[c2]

                    # Check if colors match
                    if color1 == color2:
                        # Check if path between c1 and c2 (exclusive) is all white (0) in grid_at_pass_start
                        can_connect = True
                        if c2 > c1 + 1: # Only check if there are cells between them
                            for k in range(c1 + 1, c2):
                                if grid_at_pass_start[r, k] != 0:
                                    can_connect = False
                                    break
                        else: # Adjacent, no path to check/fill
                            can_connect = False 

                        if can_connect:
                            # Fill the path with color1 in the working_grid
                            # Check if we are actually changing anything (target cell is white)
                            path_changed = False
                            for k in range(c1 + 1, c2):
                                # Modify working_grid if the target is currently white
                                if working_grid[r, k] == 0:
                                    working_grid[r, k] = color1
                                    path_changed = True
                            if path_changed:
                                made_connection_in_pass = True # Signal change

        # If no connections were made in the entire pass, break the loop
        if not made_connection_in_pass:
            break

    grid_with_connections = working_grid # Final state after connections

    # --- Step 3: Source Identification and Mapping ---
    sources = []
    has_magenta_source = False
    has_orange_anywhere = False
    source_coords_colors = {} # Store original color at source coord: {(r, c): color}

    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c] # Check ORIGINAL grid
            if color != 0:
                if color == 7:
                    has_orange_anywhere = True # Check if orange exists anywhere in original
                # All non-white pixels are potential sources
                sources.append(((r, c), color))
                source_coords_colors[(r, c)] = color
                if color == 6:
                    has_magenta_source = True # Check if any source is magenta

    # Create the expansion color map based on original source colors
    expansion_color_map = {}
    # Iterate through unique original source colors to build the map
    unique_source_colors = {color for _, color in sources}
    for color in unique_source_colors:
        if color == 8 and has_magenta_source:
            expansion_color_map[color] = 1 # Azure -> Blue
        elif color == 6 and has_orange_anywhere:
            expansion_color_map[color] = 7 # Magenta -> Orange
        else:
            expansion_color_map[color] = color # Other sources expand as themselves


    # --- Step 4: Simultaneous Expansion (BFS) ---
    # distance: Stores the step count when a cell is reached. -1 means unreached.
    # owner: Stores the coordinate tuple (sr, sc) of the source that reached the cell.
    #        None means unreached/unowned. "CONTESTED" means multiple sources reached simultaneously.
    distance = np.full((rows, cols), -1, dtype=int)
    owner = np.full((rows, cols), None, dtype=object)
    queue = deque()

    # Initialize BFS queue and state grids with sources
    for (r, c), _ in sources:
         # Sources always start, regardless of connection phase results at their location.
         # If the source location is already owned (e.g., two sources at same spot, impossible), handle gracefully.
         if owner[r,c] is None:
             distance[r, c] = 0
             owner[r, c] = (r, c) # Owner is the coord tuple of the source itself
             queue.append(((r, c), 0)) # ((row, col), dist)
         # Note: If multiple sources start at the same location (input error?), the first one processed wins initialization.

    # Main BFS loop processing level by level
    while queue:
        # Dictionary to track cells reached in this specific step for conflict detection
        # Format: {(nr, nc): {originating_owner_coord1, originating_owner_coord2, ...}}
        newly_reached_this_step = {}

        # Determine current distance level
        if not queue: break
        current_dist = queue[0][1]

        # Process all elements belonging to the current distance level
        processed_in_level = 0
        while queue and queue[0][1] == current_dist:
             (r, c), dist = queue.popleft()
             processed_in_level += 1

             # Get the owner coord tuple of the current cell expanding
             current_owner_coord = owner[r, c]

             # If the current cell became contested earlier, it cannot expand further
             # Also check if it's a valid tuple (source origin)
             if not isinstance(current_owner_coord, tuple):
                 continue

             # Explore neighbors (Manhattan distance)
             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 nr, nc = r + dr, c + dc

                 # Check bounds
                 if 0 <= nr < rows and 0 <= nc < cols:
                     # *** Expansion Condition ***
                     # 1. Must be white (0) in the grid *after* connections.
                     # 2. Must be currently unreached/unowned (owner is None).
                     if grid_with_connections[nr, nc] == 0 and owner[nr, nc] is None:
                        # Record this reach attempt for conflict resolution after the level is processed
                        if (nr, nc) not in newly_reached_this_step:
                            newly_reached_this_step[(nr, nc)] = set()
                        # Add the *originating source* coord
                        newly_reached_this_step[(nr, nc)].add(current_owner_coord)

        # End of step processing: Update owner/distance grids and queue based on newly_reached_this_step
        next_level_dist = current_dist + 1
        for (nr, nc), owners_reaching in newly_reached_this_step.items():
            if len(owners_reaching) == 1:
                 # Successfully claimed by exactly one owner source in this step
                 assigned_owner_coord = owners_reaching.pop() # Get the single owner coord
                 distance[nr, nc] = next_level_dist
                 owner[nr, nc] = assigned_owner_coord # Store the tuple coord of the owner source
                 queue.append(((nr, nc), next_level_dist)) # Add to queue for next level
            elif len(owners_reaching) > 1:
                 # Contested: Reached by multiple different sources in this step
                 owner[nr, nc] = "CONTESTED"
                 # Do not update distance
                 # Crucially, do *not* add contested cells to the queue for further expansion.

    # --- Step 5: Final Output Construction ---
    # Start with the grid after connections
    final_output_grid = np.copy(grid_with_connections)
    # Now fill in the expanded areas based on the BFS results
    for r in range(rows):
        for c in range(cols):
            cell_owner = owner[r, c]
            # Fill if owned by a non-contested source (owner is a tuple)
            if isinstance(cell_owner, tuple):
                sr, sc = cell_owner
                # Get the original color of the source that owns this cell
                original_source_color = source_coords_colors[(sr, sc)]
                # Determine the fill color using the expansion map
                fill_color = expansion_color_map.get(original_source_color, original_source_color) # Use map, fallback to original
                final_output_grid[r, c] = fill_color
            elif cell_owner == "CONTESTED":
                # Ensure contested cells remain white (they should be white in grid_with_connections anyway)
                final_output_grid[r, c] = 0
            # Else: cell keeps its color from grid_with_connections (original non-white, connected line, or unreached white)


    return final_output_grid
```