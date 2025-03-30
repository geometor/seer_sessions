import numpy as np
from collections import deque

"""
Transforms the input grid by replacing each magenta pixel (color 6) with the 
color of its nearest non-magenta neighbor. Distance is measured using 
Manhattan distance (|row1 - row2| + |col1 - col2|).

If multiple non-magenta neighbors are equidistant, a tie-breaking rule is applied:
1. Priority based on the relative direction of the non-magenta neighbor (source) 
   to the magenta pixel (target): Up is preferred, then Left, then Down, then Right.
2. If still tied (e.g., equidistant sources in non-primary directions, or 
   multiple sources in the same highest-priority direction), the source with 
   the smallest row index is chosen.
3. If still tied, the source with the smallest column index is chosen.

Non-magenta pixels remain unchanged in the output grid.

This implementation uses an optimized multi-source Breadth-First Search (BFS) 
starting from all non-magenta pixels simultaneously. Instead of storing lists 
of potential sources for ties, it stores only the single "best" source found 
so far for each grid cell, applying the tie-breaking rules whenever an equally 
short path is discovered.
"""

def compare_sources(source1_pos, source2_pos, target_r, target_c):
    """
    Compares two source positions based on the tie-breaking rules relative 
    to a target position. Used to determine which source is 'better' when
    they are equidistant from the target.

    Args:
        source1_pos (tuple): (row, col) of the first source.
        source2_pos (tuple): (row, col) of the second source.
        target_r (int): Row index of the target pixel.
        target_c (int): Column index of the target pixel.

    Returns:
        int: -1 if source1 is better, 1 if source2 is better. 
             (Technically returns 0 if they are identical, but sources are
              distinct points).
    """
    sr1, sc1 = source1_pos
    sr2, sc2 = source2_pos

    # Helper to calculate priority based on relative direction
    def get_priority(sr, sc, tr, tc):
        dr = sr - tr
        dc = sc - tc
        if dr < 0 and dc == 0: return 0  # Up
        if dr == 0 and dc < 0: return 1  # Left
        if dr > 0 and dc == 0: return 2  # Down
        if dr == 0 and dc > 0: return 3  # Right
        return 4 # Other (diagonal or non-cardinal aligned)

    p1 = get_priority(sr1, sc1, target_r, target_c)
    p2 = get_priority(sr2, sc2, target_r, target_c)

    # Compare based on priority
    if p1 < p2: return -1
    if p1 > p2: return 1

    # Tie in priority: Compare based on row index
    if sr1 < sr2: return -1
    if sr1 > sr2: return 1

    # Tie in row index: Compare based on column index
    if sc1 < sc2: return -1
    if sc1 > sc2: return 1
    
    # This case should not be reached if source positions are distinct
    return 0 

def transform(input_grid):
    """
    Transforms the input grid using the optimized multi-source BFS approach.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    output_grid = np.copy(grid) # Initialize output grid

    # Find coordinates of source (non-magenta) and target (magenta) pixels
    source_pixels = [] # Stores tuples: ((r, c), color)
    target_coords = [] # Stores tuples: (r, c)
    has_magenta = False
    has_non_magenta = False
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color == 6:
                target_coords.append((r, c))
                has_magenta = True
            else:
                source_pixels.append(((r, c), color))
                has_non_magenta = True

    # Handle edge cases: no targets or no sources
    if not has_magenta or not has_non_magenta:
        return input_grid

    # Initialize distance grid: stores min distance from any source
    distance_grid = np.full((rows, cols), float('inf'), dtype=float)
    # Initialize source info grid: stores the (r, c, color) of the best source found so far
    # Use object dtype to store tuples, initialize with None
    source_info_grid = np.full((rows, cols), None, dtype=object) 

    # Initialize BFS queue with all source pixels
    queue = deque()
    for (sr, sc), color in source_pixels:
        distance_grid[sr, sc] = 0
        source_info_grid[sr, sc] = (sr, sc, color) # Store (source_r, source_c, source_color)
        queue.append((sr, sc))

    # --- Optimized Multi-Source BFS ---
    while queue:
        r, c = queue.popleft()
        current_dist = distance_grid[r, c]
        # The best source reaching (r, c) is stored in source_info_grid[r, c]
        current_best_source_info = source_info_grid[r, c] 
        
        # Explore neighbors (Up, Down, Left, Right) using Manhattan distance steps
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                new_dist = current_dist + 1

                # --- Comparison Logic ---
                # Case 1: Found a shorter path to the neighbor
                if new_dist < distance_grid[nr, nc]:
                    distance_grid[nr, nc] = new_dist
                    # The best source for (r,c) is now the best for (nr,nc) via this path
                    source_info_grid[nr, nc] = current_best_source_info 
                    queue.append((nr, nc)) # Add neighbor to queue for further exploration

                # Case 2: Found an equally short path to the neighbor
                elif new_dist == distance_grid[nr, nc]:
                    # Need to compare the source associated with the current path 
                    # (current_best_source_info) against the source already known 
                    # for the neighbor (source_info_grid[nr, nc]).
                    
                    existing_best_source_info = source_info_grid[nr, nc]
                    
                    # Extract source positions for comparison
                    candidate_source_pos = (current_best_source_info[0], current_best_source_info[1])
                    existing_source_pos = (existing_best_source_info[0], existing_best_source_info[1])

                    # Compare using the tie-breaking rules relative to the *neighbor* (nr, nc)
                    comparison_result = compare_sources(candidate_source_pos, existing_source_pos, nr, nc)

                    # If the new path's source is better (-1), update the neighbor's source info
                    if comparison_result == -1:
                        source_info_grid[nr, nc] = current_best_source_info
                        # No need to re-enqueue: (nr, nc) is already in the queue 
                        # or has been processed at this distance level. We just updated
                        # the source info that will be propagated *from* it later.

    # --- Post-BFS: Assign colors to target pixels ---
    for tr, tc in target_coords:
        best_source_info = source_info_grid[tr, tc]
        if best_source_info is not None:
            # The third element of the tuple is the color
            winning_color = best_source_info[2] 
            output_grid[tr, tc] = winning_color
        # If best_source_info is None, it means the target was unreachable, 
        # which shouldn't happen if has_non_magenta is true, but we keep its 
        # original color (which is magenta 6) just in case.

    # Convert the final NumPy array back to list of lists
    return output_grid.tolist()