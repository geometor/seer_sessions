```python
"""
Transforms the input grid based on the following rules:

1.  **Initialize:** Start with the input grid. Create a working copy.
2.  **Yellow Connection:**
    *   Identify all Yellow (4) pixels in the current working grid.
    *   For each row, find pairs of Yellow pixels.
    *   If the horizontal path strictly between a pair of Yellow pixels on the same row consists only of White (0) pixels, fill that path with Yellow (4) in the working grid.
    *   Repeat this connection process on the updated working grid until no more connections can be made in a full pass. Store this grid state (`grid_with_yellow_connections`).
3.  **Source Identification and Mapping:**
    *   Refer back to the *original* input grid. Identify all non-White (0) and non-Yellow (4) pixels. These are the "expansion sources".
    *   Determine if any of these identified expansion sources are Magenta (6) (`has_magenta_source`).
    *   Determine if the *original* input grid contains *any* Orange (7) pixels (not necessarily sources) (`has_orange_anywhere`).
    *   Create a mapping for how source colors will expand:
        *   If a source is Azure (8) AND `has_magenta_source` is true, it expands as Blue (1).
        *   If a source is Magenta (6) AND `has_orange_anywhere` is true, it expands as Orange (7).
        *   All other sources expand using their own original color.
4.  **Simultaneous Expansion (BFS):**
    *   Start a simultaneous Breadth-First Search (BFS) from all identified expansion sources on the `grid_with_yellow_connections`.
    *   The BFS expands one step (Manhattan distance) at a time into adjacent cells.
    *   **Expansion Condition:** A source can only expand into a cell `(nr, nc)` if that cell is White (0) in the `grid_with_yellow_connections` AND has not yet been reached or contested in the current BFS (`owner[nr, nc]` is `None`).
    *   **Obstacles:** Expansion is blocked by grid boundaries and any cell that is not White (0) in the `grid_with_yellow_connections` or cells that become contested.
    *   **Conflict Resolution:** If multiple *different* sources attempt to expand into the same valid White cell in the *same step* of the BFS, that cell becomes "CONTESTED", remains White (0) in the final output, and acts as an obstacle for subsequent steps.
    *   **Coloring:** When a source successfully expands into a cell, that cell's ownership is recorded. The final coloring happens after the BFS completes.
5.  **Output Construction:**
    *   Start with the `grid_with_yellow_connections`.
    *   Iterate through the grid. For each cell `(r, c)`:
        *   If the cell was successfully claimed by a source during the BFS (`owner[r, c]` is a source coordinate tuple), color the cell in the final output grid using the color determined by the source's original color and the color mapping (Step 3).
        *   Otherwise (if the cell was originally non-white, yellow-connected, contested, or never reached), it retains its color from `grid_with_yellow_connections`.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    # 1. Initialize: Create a working copy
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Yellow Connection Phase
    made_connection = True
    while made_connection:
        made_connection = False
        current_grid_state = np.copy(output_grid) # Check against state at start of pass
        for r in range(rows):
            # Find yellow pixel indices in the current row of the working grid
            yellow_indices = [c for c in range(cols) if current_grid_state[r, c] == 4]
            if len(yellow_indices) >= 2:
                for i in range(len(yellow_indices) - 1):
                    c1 = yellow_indices[i]
                    c2 = yellow_indices[i+1]
                    # Check if path between c1 and c2 (exclusive) is all white (0) in the current grid state
                    can_connect = True
                    if c2 > c1 + 1: # Only check if there are cells between them
                        for k in range(c1 + 1, c2):
                            # Check the state at the START of this pass
                            if current_grid_state[r, k] != 0:
                                can_connect = False
                                break
                        if can_connect:
                            # Fill the path with yellow (4) in the output_grid
                            for k in range(c1 + 1, c2):
                                # Ensure we only fill if it's currently white in the evolving output grid
                                # This prevents overwriting fills made earlier in the same pass in the same row
                                if output_grid[r, k] == 0:
                                     output_grid[r, k] = 4
                                     made_connection = True # Signal that a change occurred

    # Store the grid state after yellow connections
    grid_with_yellow_connections = np.copy(output_grid)

    # 3. Source Identification and Mapping
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
                if color != 4: # Non-white, non-yellow are potential sources
                    # Check if the source position still has its original color after yellow connection
                    # (it might have been paved over if it was white between two yellows, which shouldn't happen for non-white sources)
                    # We define sources based on the ORIGINAL grid, regardless of yellow connection overwrites.
                    sources.append(((r, c), color))
                    source_coords_colors[(r, c)] = color
                    if color == 6:
                        has_magenta_source = True # Check if any source is magenta

    # Create the expansion color map based on original source colors
    expansion_color_map = {}
    unique_source_colors = {color for _, color in sources}
    for color in unique_source_colors:
        if color == 8 and has_magenta_source:
            expansion_color_map[color] = 1 # Azure -> Blue
        elif color == 6 and has_orange_anywhere:
            expansion_color_map[color] = 7 # Magenta -> Orange
        else:
            expansion_color_map[color] = color # Other sources expand as themselves

    # 4. Simultaneous Expansion Phase (BFS)
    # distance: Stores the step count when a cell is reached. -1 means unreached.
    # owner: Stores the coordinate tuple (sr, sc) of the source that reached the cell.
    #        None means unreached/unowned. "CONTESTED" means multiple sources reached simultaneously.
    distance = np.full((rows, cols), -1, dtype=int)
    owner = np.full((rows, cols), None, dtype=object)
    queue = deque()

    # Initialize BFS queue and state grids with sources
    for (r, c), _ in sources:
         # Check if source position is still valid in grid_with_yellow_connections
         # A source is still a source even if its *cell* was paved over by yellow,
         # but it cannot expand *from* a yellow cell. It only starts expanding
         # if its original location wasn't changed by yellow connections.
         # If the source location *itself* became yellow, it cannot start expansion.
         # Check if the source cell in grid_with_yellow_connections still holds the original color
         if grid_with_yellow_connections[r,c] == input_grid[r,c]:
              # Check if the source location is not contested from the start (shouldn't be)
              if owner[r,c] is None:
                 distance[r, c] = 0
                 owner[r, c] = (r, c) # Owner is the coord tuple
                 queue.append(((r, c), 0)) # ((row, col), dist)
              # Handle potential source overlap (unlikely but possible if sources are adjacent)
              # If already owned, it means two sources are at the same spot (impossible by definition)
              # Or if adjacent sources try to claim each other in step 0 (also impossible)

    # Main BFS loop processing level by level
    current_dist = 0
    while queue:
        # Dictionary to track cells reached in this specific step for conflict detection
        # Format: {(nr, nc): [originating_owner_coord1, originating_owner_coord2, ...]}
        newly_reached_this_step = {}

        # Peek distance of the first element to confirm the current level
        if not queue: break
        peek_dist = queue[0][1]
        current_dist = peek_dist

        # Process all elements belonging to the current distance level
        processed_count_in_level = 0
        while queue and queue[0][1] == current_dist:
             (r, c), dist = queue.popleft()
             processed_count_in_level += 1

             # Get the owner coord tuple of the current cell expanding
             current_owner_coord = owner[r, c]

             # If the current cell became contested earlier, it cannot expand further
             if not isinstance(current_owner_coord, tuple):
                 continue

             # Explore neighbors (Manhattan distance)
             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 nr, nc = r + dr, c + dc

                 # Check bounds
                 if 0 <= nr < rows and 0 <= nc < cols:
                     # *** Expansion Condition ***
                     # 1. Must be white (0) in the grid *after* yellow connections.
                     # 2. Must be currently unreached (owner is None).
                     #    (Cells reached in *previous* steps or marked CONTESTED won't have owner == None)
                     if grid_with_yellow_connections[nr, nc] == 0 and owner[nr, nc] is None:
                        # Record this reach attempt for conflict resolution after the level is processed
                        if (nr, nc) not in newly_reached_this_step:
                            newly_reached_this_step[(nr, nc)] = []
                        # Only add unique owners reaching this cell in this step
                        if current_owner_coord not in newly_reached_this_step[(nr, nc)]:
                             newly_reached_this_step[(nr, nc)].append(current_owner_coord)


        # End of step processing: Update owner/distance grids and queue based on newly_reached_this_step
        next_level_dist = current_dist + 1
        for (nr, nc), owners_reaching in newly_reached_this_step.items():
            if len(owners_reaching) == 1:
                 # Successfully claimed by exactly one owner in this step
                 assigned_owner = owners_reaching[0]
                 distance[nr, nc] = next_level_dist
                 owner[nr, nc] = assigned_owner # Store the tuple coord of the owner source
                 queue.append(((nr, nc), next_level_dist)) # Add to queue for next level
            else:
                 # Contested: Reached by multiple different sources in this step
                 owner[nr, nc] = "CONTESTED"
                 # Do not update distance (or set to a special value if needed, but owner is enough)
                 # Crucially, do *not* add contested cells to the queue for further expansion.


    # 5. Final Output Construction
    # Start with the grid after yellow connections
    final_output_grid = grid_with_yellow_connections
    # Now fill in the expanded areas based on the BFS results
    for r in range(rows):
        for c in range(cols):
            cell_owner = owner[r, c]
            # Fill if owned by a non-contested source (owner is a tuple)
            # No need to check if originally white, as only originally white cells
            # could have been reached and assigned a tuple owner.
            if isinstance(cell_owner, tuple):
                sr, sc = cell_owner
                # Get the original color of the source that owns this cell
                original_source_color = source_coords_colors[(sr, sc)]
                # Determine the fill color using the expansion map
                fill_color = expansion_color_map.get(original_source_color, original_source_color) # Use map, fallback to original
                final_output_grid[r, c] = fill_color
            # If cell_owner is "CONTESTED" or None, the cell keeps its value
            # from grid_with_yellow_connections (which would be 0 if it was potentially expandable,
            # or its original/yellow color otherwise).

    return final_output_grid
```