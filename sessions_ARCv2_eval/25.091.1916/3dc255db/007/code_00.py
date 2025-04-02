import numpy as np
from collections import deque, Counter

"""
Transformation Rule (Derived from Examples 2 & 3):

1.  Identify Unreachable Pixels: Find all non-white pixels in the input grid that cannot reach any boundary cell by moving only through adjacent white (0) pixels. This is achieved using a Breadth-First Search (BFS) starting from all white boundary cells.
2.  Group Unreachable Pixels: Partition the identified unreachable pixels into "Enclosed Groups". An Enclosed Group consists of pixels that:
    a.  All have the same color.
    b.  Form a single connected component using 4-way adjacency (considering only connections between the identified unreachable pixels of that same color).
3.  Process Each Group: For every Enclosed Group found:
    a.  Remove Group Pixels: Change the color of all pixels belonging to the group to white (0) in the output grid.
    b.  Determine Target Columns: Identify the set of all unique column indices occupied by the pixels within the group.
    c.  Determine Indicator Count (`N`): Count the number of unique row indices occupied by the pixels within the group.
    d.  Add Indicator Pixels: For *each* unique target column identified in step 3b, change the color of the top `N` pixels (rows 0 to N-1) in that column to the group's color. Overwriting may occur if multiple groups target the same top cells.
4.  Final Grid: The grid after processing all Enclosed Groups is the final output.
(Note: This procedure is specifically designed to match the pattern observed in training examples 2 and 3. Example 1 exhibits a different transformation pattern not captured by this rule, involving pixels *outside* the main shapes.)
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
    unreachable_pixels = set() # Store as ((row, col), color)

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

    # Identify non-white pixels that were not reached by the white-cell BFS
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not reachable[r, c]:
                unreachable_pixels.add(((r, c), grid[r,c]))

    return unreachable_pixels

def group_unreachable_pixels(unreachable_pixels_with_color, grid):
    """
    Groups unreachable pixels into connected components based on color and adjacency.
    Args:
        unreachable_pixels_with_color: A set of ((r, c), color) tuples.
        grid: The original input grid (needed for color checks).
    Returns:
        A dictionary {color: [group1_locations, group2_locations, ...]}
        where each group_locations is a list of (r, c) tuples.
    """
    rows, cols = grid.shape
    visited = set() # Keep track of visited pixel locations (r, c)
    groups = {}
    # Create a set of just locations for efficient checking
    unreachable_locations = {loc for loc, color in unreachable_pixels_with_color}

    for pixel_loc, color in unreachable_pixels_with_color:
        if pixel_loc not in visited:
            current_group = []
            q = deque([pixel_loc])
            visited.add(pixel_loc)

            # Start BFS to find connected component of the same color within unreachable pixels
            while q:
                r, c = q.popleft()
                current_group.append((r,c))

                # Explore neighbors
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    neighbor_loc = (nr, nc)

                    # Check if neighbor is within bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if neighbor is also unreachable, has the same color, and hasn't been visited yet
                        if neighbor_loc in unreachable_locations and \
                           grid[nr, nc] == color and \
                           neighbor_loc not in visited:
                            
                            # Verify it's in the original set (redundant if unreachable_locations is correct, but safe)
                            is_target_unreachable = False
                            for loc, clr in unreachable_pixels_with_color:
                                if loc == neighbor_loc and clr == color:
                                    is_target_unreachable = True
                                    break
                            
                            if is_target_unreachable:
                                visited.add(neighbor_loc)
                                q.append(neighbor_loc)

            # Store the found group associated with its color
            if color not in groups:
                groups[color] = []
            groups[color].append(current_group)

    return groups


def transform(input_grid):
    """
    Applies the enclosure transformation rule derived from examples 2 and 3.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find all non-white pixels unreachable via white cells
    unreachable_pixels_with_color = find_unreachable_non_white(input_grid)

    # 2. Group these pixels by color and connectivity
    enclosed_groups_by_color = group_unreachable_pixels(unreachable_pixels_with_color, input_grid)

    # 3. Process each group
    for color, groups in enclosed_groups_by_color.items():
        for group_locations in groups:
            if not group_locations: # Skip if group is empty
                continue

            # a. Remove group pixels from the output grid
            for r, c in group_locations:
                output_grid[r, c] = 0 # Set to white

            # b. Determine Target Columns (unique columns in the group)
            target_cols = sorted(list(set(c for r, c in group_locations)))

            # c. Determine Indicator Count (N - unique rows in the group)
            unique_rows = set(r for r, c in group_locations)
            N = len(unique_rows)

            # d. Add Indicator Pixels for each target column
            for target_col in target_cols:
                 # Ensure target_col is within grid bounds (should always be)
                 if 0 <= target_col < cols:
                    # Add pixels to the top N rows of this column
                    for i in range(min(N, rows)): # Ensure we don't write past grid boundary
                        output_grid[i, target_col] = color

    # Return the modified grid
    return output_grid