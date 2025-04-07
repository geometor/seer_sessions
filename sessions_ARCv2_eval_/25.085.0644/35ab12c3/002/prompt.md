
Previous Code:
```python
import numpy as np
from collections import deque

def solve(input_grid):
    """
    Transforms the input grid based on the following rules:

    1.  Yellow Connection: Horizontally connect pairs of Yellow (4) pixels if the
        path between them on the same row consists only of White (0) pixels. These
        newly filled Yellow pixels act as obstacles for the next phase. This process
        repeats until no more connections can be made.

    2.  Expansion Color Determination:
        - Identify all non-White, non-Yellow pixels in the original input grid as sources.
        - Check if the original input contains any Magenta (6) source pixels (`has_magenta_source`).
        - Check if the original input contains any Orange (7) pixels anywhere (`has_orange_anywhere`).
        - Create a mapping for expansion colors:
            - Azure (8) expands as Blue (1) if `has_magenta_source` is true.
            - Magenta (6) expands as Orange (7) if `has_orange_anywhere` is true.
            - All other source colors expand as themselves.

    3.  Simultaneous Expansion (BFS):
        - Start a simultaneous Breadth-First Search (BFS) from all source pixels identified in step 2.
        - Expansion occurs one step (Manhattan distance) at a time into adjacent cells that were originally White (0) in the input grid.
        - Expansion is blocked by grid boundaries, any non-White pixel in the original input, and any Yellow pixels filled during the connection phase.
        - Conflict Resolution: If a White cell is reached by multiple different sources in the same BFS step, the cell remains White (0) and acts as an obstacle for further expansion from any source.
        - The color used to fill an expanded cell is determined by the expansion color mapping from step 2 based on the color of the originating source pixel.

    4.  Output: The final grid contains the original non-White pixels, the Yellow connections, and the colored expansions.
    """

    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # --- 1. Yellow Connection Phase ---
    made_connection = True
    while made_connection:
        made_connection = False
        for r in range(rows):
            yellow_indices = [c for c in range(cols) if output_grid[r, c] == 4]
            if len(yellow_indices) >= 2:
                for i in range(len(yellow_indices) - 1):
                    c1 = yellow_indices[i]
                    c2 = yellow_indices[i+1]
                    # Check if path between c1 and c2 (exclusive) is all white (0)
                    can_connect = True
                    if c2 > c1 + 1: # Only check if there are cells between them
                        for k in range(c1 + 1, c2):
                            if output_grid[r, k] != 0:
                                can_connect = False
                                break
                        if can_connect:
                            # Fill the path with yellow (4)
                            for k in range(c1 + 1, c2):
                                if output_grid[r, k] == 0: # Double check, although logic implies it
                                     output_grid[r, k] = 4
                                     made_connection = True # Signal that a change occurred

    # --- 2. Expansion Phase Preparation ---
    sources = []
    has_magenta_source = False
    has_orange_anywhere = False

    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color != 0:
                if color == 7:
                    has_orange_anywhere = True
                if color != 4: # Non-white, non-yellow are potential sources
                    sources.append(((r, c), color))
                    if color == 6:
                        has_magenta_source = True

    expansion_color_map = {}
    for _, color in sources:
        if color not in expansion_color_map: # Avoid redundant mapping
            if color == 8 and has_magenta_source:
                expansion_color_map[color] = 1
            elif color == 6 and has_orange_anywhere:
                expansion_color_map[color] = 7
            else:
                expansion_color_map[color] = color

    # --- 3. Simultaneous Expansion Phase (BFS) ---
    # distance: Stores the step count when a cell is reached. -1 means unreached.
    # owner: Stores the coordinate tuple (sr, sc) of the source that reached the cell.
    #        None means unreached/unowned. "CONTESTED" means multiple sources reached simultaneously.
    distance = np.full((rows, cols), -1, dtype=int)
    owner = np.full((rows, cols), None, dtype=object)
    queue = deque()

    # Initialize BFS queue and grids with sources
    for (r, c), color in sources:
        if output_grid[r,c] != 0: # Check if source wasn't overwritten by yellow (unlikely but safe)
            distance[r, c] = 0
            owner[r, c] = (r, c)
            queue.append(((r, c), 0)) # ((row, col), dist)

    processed_in_step = {} # Store { (r,c): owner_coord } for conflict detection within a step

    current_dist = 0
    while queue:
        # Process all nodes at the current distance level first
        level_size = len(queue)
        if level_size == 0: break # Should not happen if queue is not empty, but safe check

        newly_reached_this_step = {} # Tracks cells reached in this specific step: {(r,c): owner_coord}

        # Peek distance of the first element to confirm level
        if queue:
             _, peek_dist = queue[0]
             current_dist = peek_dist

        processed_count = 0
        while queue and queue[0][1] == current_dist:
             (r, c), dist = queue.popleft()
             processed_count += 1
             current_owner_coord = owner[r, c]

             # If the current cell itself became contested earlier in this step, skip its expansion
             if current_owner_coord == "CONTESTED":
                 continue

             # Explore neighbors
             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                 nr, nc = r + dr, c + dc

                 # Check bounds
                 if 0 <= nr < rows and 0 <= nc < cols:
                     # Check if neighbor is originally white AND currently unoccupied/uncontested in the output/BFS state
                     # We only expand into originally white cells that haven't been filled yet by Yellow or previous expansion steps
                     # And crucially, haven't been reached in *this* step by another source yet.
                     if input_grid[nr, nc] == 0: # Must be originally white
                         
                         existing_owner = owner[nr, nc]
                         existing_dist = distance[nr, nc]

                         if existing_owner is None: # Unreached before this step
                             if (nr, nc) not in newly_reached_this_step:
                                 # First time reached in this step
                                 newly_reached_this_step[(nr, nc)] = current_owner_coord
                                 # Don't update distance/owner/queue yet, wait till end of step processing
                             elif newly_reached_this_step[(nr, nc)] != current_owner_coord:
                                 # Reached by a *different* source in the *same* step -> CONTESTED
                                 newly_reached_this_step[(nr, nc)] = "CONTESTED"

                         # This handles cases where a cell might be reached again in a later step,
                         # or by the same owner in the current step (which is fine).
                         # Conflicts (CONTESTED) are only triggered by different owners in the *same* step.


        # End of step processing: Update grids and queue based on newly_reached_this_step
        for (nr, nc), assigned_owner in newly_reached_this_step.items():
            if assigned_owner != "CONTESTED":
                 distance[nr, nc] = current_dist + 1
                 owner[nr, nc] = assigned_owner
                 queue.append(((nr, nc), current_dist + 1))
            else:
                 # Mark as contested permanently in the owner grid
                 # No need to update distance, as it won't expand further
                 owner[nr, nc] = "CONTESTED"
                 # Do not add contested cells to the queue


    # --- 4. Final Output Construction ---
    for r in range(rows):
        for c in range(cols):
            cell_owner = owner[r, c]
            # Fill if originally white and owned by a non-contested source
            if input_grid[r, c] == 0 and isinstance(cell_owner, tuple):
                sr, sc = cell_owner
                source_color = input_grid[sr, sc]
                fill_color = expansion_color_map.get(source_color, source_color) # Use map
                output_grid[r, c] = fill_color

    return output_grid

```
Results for code_00.py:
Train Set Error: transform function not found
