import copy

"""
Transforms a 2D grid based on the location of a '5' and adjacent '2's.

1. Finds the location of the number 5 (anchor).
2. Identifies all numbers 2 directly adjacent (horizontally or vertically) to the 5.
3. Changes these adjacent 2s to 3s.
4. Determines a projection direction based on the relative position of the adjacent 2s to the 5:
    - 2s Left of 5 -> Project Up
    - 2s Right of 5 -> Project Down
    - 2s Above 5 -> Project Right
    - 2s Below 5 -> Project Left
5. Determines a projection anchor point based on the relative position:
    - Left: Rightmost adjacent 2.
    - Right: Leftmost adjacent 2.
    - Above: The 5 itself.
    - Below: Topmost adjacent 2.
6. Projects a line of 2s, with length equal to the number of original adjacent 2s,
   starting one step from the anchor point in the projection direction.
"""

def find_value(grid: list[list[int]], value: int) -> tuple[int | None, int | None]:
    """Finds the first occurrence of a value in the grid."""
    num_rows = len(grid)
    if num_rows == 0:
        return None, None
    num_cols = len(grid[0])
    for r in range(num_rows):
        for c in range(num_cols):
            if grid[r][c] == value:
                return r, c
    return None, None

def find_adjacent_target_coords(grid: list[list[int]], r: int, c: int, target_value: int) -> list[tuple[int, int]]:
    """Finds coordinates of adjacent cells with the target value."""
    num_rows = len(grid)
    num_cols = len(grid[0])
    adjacent_coords = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Right, Left, Down, Up
        nr, nc = r + dr, c + dc
        if 0 <= nr < num_rows and 0 <= nc < num_cols and grid[nr][nc] == target_value:
            adjacent_coords.append((nr, nc))
    return adjacent_coords


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    num_rows = len(output_grid)
    if num_rows == 0:
        return output_grid
    num_cols = len(output_grid[0])
    if num_cols == 0:
        return output_grid

    # 1. Locate the anchor (5)
    r5, c5 = find_value(input_grid, 5)
    if r5 is None:
        # No anchor found, return the original grid
        return output_grid

    # 2. Find adjacent targets (2s)
    adjacent_2s = find_adjacent_target_coords(input_grid, r5, c5, 2)

    # 3. If no adjacent 2s, return the grid unchanged
    if not adjacent_2s:
        return output_grid

    # 4. Change adjacent 2s to 3s in the output grid
    for r2, c2 in adjacent_2s:
        output_grid[r2][c2] = 3

    # 5. Determine relative direction and projection parameters
    proj_anchor_r, proj_anchor_c = -1, -1
    proj_dr, proj_dc = 0, 0
    
    # Check if adjacent 2s are horizontal or vertical relative to 5
    first_r2, first_c2 = adjacent_2s[0]

    if first_r2 == r5: # Horizontal adjacency
        if first_c2 < c5: # 2s are LEFT of 5
            proj_anchor_r, proj_anchor_c = r5, max(c for r, c in adjacent_2s) # Rightmost 2
            proj_dr, proj_dc = -1, 0 # Project UP
        else: # 2s are RIGHT of 5
            proj_anchor_r, proj_anchor_c = r5, min(c for r, c in adjacent_2s) # Leftmost 2
            proj_dr, proj_dc = 1, 0 # Project DOWN
            
    elif first_c2 == c5: # Vertical adjacency
        if first_r2 < r5: # 2s are ABOVE 5
            proj_anchor_r, proj_anchor_c = r5, c5 # Anchor is 5 itself
            proj_dr, proj_dc = 0, 1 # Project RIGHT
        else: # 2s are BELOW 5
            proj_anchor_r, proj_anchor_c = min(r for r, c in adjacent_2s), c5 # Topmost 2
            proj_dr, proj_dc = 0, -1 # Project LEFT

    # 6. Execute projection
    N = len(adjacent_2s)
    for i in range(1, N + 1):
        proj_r = proj_anchor_r + i * proj_dr
        proj_c = proj_anchor_c + i * proj_dc

        # Check boundaries before placing the 2
        if 0 <= proj_r < num_rows and 0 <= proj_c < num_cols:
            # Check if the target cell is currently 0 (based on examples, projection doesn't overwrite non-zero)
            # Although not explicitly stated, let's assume projection only happens onto 0s
            if output_grid[proj_r][proj_c] == 0:
                 output_grid[proj_r][proj_c] = 2
            # If we need to stop projection if it hits non-zero, uncomment below
            # else:
            #    break # Stop projection if the path is blocked by non-zero

    return output_grid