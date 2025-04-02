import numpy as np
from collections import deque, Counter
import math

"""
Transformation Rule:

1.  Identify Unreachable Pixels: Find all non-white pixels in the input grid that cannot reach any boundary cell by moving only through adjacent white (0) pixels. This is done via a Breadth-First Search (BFS) starting from boundary white cells.
2.  Group Unreachable Pixels: Partition the identified unreachable pixels into "Enclosed Groups". An Enclosed Group consists of pixels that:
    a.  All have the same color.
    b.  Form a single connected component using 4-way adjacency (considering only connections between the identified unreachable pixels of that same color).
3.  Process Each Group: For every Enclosed Group found:
    a.  Remove Group Pixels: Change the color of all pixels belonging to the group to white (0) in the output grid.
    b.  Determine Target Column:
        i.  Calculate the frequency of each column index among the group's pixel locations.
        ii. Find the maximum frequency (`max_freq`).
        iii. Identify all column indices (`candidate_cols`) that achieve `max_freq`.
        iv. Apply Tie-breaker:
            - If only one candidate column, select it.
            - If multiple candidates: Calculate the average column index (centroid) of the group's locations. Select the candidate column closest (minimum absolute difference) to the centroid. If still tied (equidistant), select the leftmost (minimum index) tied column.
    c.  Determine Indicator Count (`N`): Count the number of unique row indices among the group's pixel locations.
    d.  Add Indicator Pixels: In the selected target column, change the color of the top `N` pixels (rows 0 to N-1) to the group's color.
4.  Final Grid: The grid after processing all Enclosed Groups is the final output.
(Note: This procedure describes the logic derived primarily from examples 2 and 3; example 1 appears to follow a different pattern not captured by this rule.)
"""

def find_unreachable_non_white(grid):
    """
    Finds all non-white pixels that cannot reach the grid boundary via white cells.
    Uses BFS starting from the boundary, propagating only through white cells (0).
    Returns a set of ((r, c), color) tuples for unreachable non-white pixels.
    """
    rows, cols = grid.shape
    reachable = np.zeros_like(grid, dtype=bool)
    q = deque()
    unreachable_pixels = set() # Using a set for efficient lookup later

    # Initialize BFS queue with boundary white cells
    for r in range(rows):
        for c in [0, cols - 1]:
            if not reachable[r, c] and grid[r, c] == 0:
                q.append((r, c))
                reachable[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
             if not reachable[r, c] and grid[r, c] == 0:
                q.append((r, c))
                reachable[r, c] = True

    # Perform BFS through white cells
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               not reachable[nr, nc] and grid[nr, nc] == 0:
                reachable[nr, nc] = True
                q.append((nr, nc))

    # Identify non-white pixels that were not reached
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not reachable[r, c]:
                unreachable_pixels.add(((r, c), grid[r,c]))

    return unreachable_pixels

def group_pixels(unreachable_pixels, grid_shape):
    """
    Groups unreachable pixels into connected components based on color and adjacency.
    Returns a dictionary {color: [group1_locations, group2_locations, ...]}
    where each group_locations is a list of (r, c) tuples.
    """
    rows, cols = grid_shape
    visited = set()
    groups = {}
    unreachable_locations = {loc for loc, color in unreachable_pixels} # For quick spatial check

    for pixel_loc, color in unreachable_pixels:
        if pixel_loc not in visited:
            current_group = []
            q = deque([pixel_loc])
            visited.add(pixel_loc)

            # BFS within unreachable pixels of the same color
            while q:
                r, c = q.popleft()
                current_group.append((r,c))

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    neighbor_loc = (nr, nc)

                    # Check bounds, if neighbor is unreachable, same color, and not visited
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       neighbor_loc in unreachable_locations and \
                       grid[nr, nc] == color and \
                       neighbor_loc not in visited:

                        # Check if this neighbor is part of the original unreachable set
                        # (This check might be redundant if unreachable_locations is derived correctly)
                        is_unreachable = False
                        for loc, clr in unreachable_pixels:
                           if loc == neighbor_loc and clr == color:
                               is_unreachable = True
                               break
                        
                        if is_unreachable:
                            visited.add(neighbor_loc)
                            q.append(neighbor_loc)


            # Store the found group
            if color not in groups:
                groups[color] = []
            groups[color].append(current_group)

    return groups


def transform(input_grid):
    """
    Applies the enclosure transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    global grid # Make input_grid accessible to group_pixels for color check
    grid = input_grid

    # 1. Find all non-white pixels unreachable via white cells
    unreachable_pixels_with_color = find_unreachable_non_white(input_grid)

    # 2. Group these pixels by color and connectivity
    enclosed_groups_by_color = group_pixels(unreachable_pixels_with_color, (rows, cols))

    # 3. Process each group
    for color, groups in enclosed_groups_by_color.items():
        for group_locations in groups:
            if not group_locations:
                continue

            # a. Remove group pixels
            for r, c in group_locations:
                output_grid[r, c] = 0

            # b. Determine Target Column
            columns = [c for r, c in group_locations]
            if not columns: continue
            col_counts = Counter(columns)
            max_freq = max(col_counts.values())
            candidate_cols = sorted([col for col, count in col_counts.items() if count == max_freq]) # Sort for leftmost tie-break later

            target_col = -1
            if len(candidate_cols) == 1:
                target_col = candidate_cols[0]
            else:
                # Calculate centroid column
                avg_col = sum(columns) / len(columns)
                min_dist = float('inf')
                best_cols = []
                for col in candidate_cols:
                    dist = abs(col - avg_col)
                    if dist < min_dist:
                        min_dist = dist
                        best_cols = [col]
                    elif dist == min_dist:
                        best_cols.append(col)
                target_col = min(best_cols) # Leftmost if equidistant

            # c. Determine Indicator Count (N)
            unique_rows = set(r for r, c in group_locations)
            N = len(unique_rows)

            # d. Add Indicator Pixels
            for i in range(min(N, rows)): # Ensure we don't write past grid boundary
                output_grid[i, target_col] = color

    return output_grid