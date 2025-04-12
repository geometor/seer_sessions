import copy

"""
Transforms a grid based on the location of horizontal '7 7 7' patterns, applying rules in a specific order of precedence.

1.  Identifies all horizontal sequences of '7 7 7' in the input grid.
2.  Applies transformation rules in the following priority order:
    a.  Core Rule (Priority 1): The outer '7's of the pattern are changed to '8', and the center '7' is changed to '6'. Cells modified by this rule are finalized.
    b.  Vertical Neighbor Rule (Priority 2): If an *input* cell value is '8' AND it is vertically adjacent to the *center* '7' of a pattern (identified in step 1) AND the cell was not modified by the Core Rule, it is changed to '6'. Cells modified by this rule are finalized.
    c.  Adjacent Neighbor Rule (Priority 3): If an *input* cell value is *not* 0, *not* 3, *not* 7, and *not* 8 AND the cell is orthogonally or diagonally adjacent to any *outer* '7' of a pattern (identified in step 1) AND the cell was not modified by previous rules, it is changed to '3'. Cells modified by this rule are finalized. (Note: This rule is likely incomplete and fails to capture cases where input 3 or 8 should become 3).
    d.  Copy Rule (Priority 4): Any cell not modified by the above rules retains its original input value.
"""

def find_777_patterns(grid: list[list[int]]) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    """
    Finds the locations of the center and outer cells of all '7 7 7' patterns.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing two sets:
        - center_locations: Set of (row, col) tuples for the middle '7'.
        - outer_locations: Set of (row, col) tuples for the left and right '7's.
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    center_locations = set()
    outer_locations = set()

    for r in range(height):
        for c in range(1, width - 1):
            # Check for the '7 7 7' pattern horizontally
            if grid[r][c-1] == 7 and grid[r][c] == 7 and grid[r][c+1] == 7:
                center_locations.add((r, c))
                outer_locations.add((r, c - 1))
                outer_locations.add((r, c + 1))
    return center_locations, outer_locations

def get_neighbors(r: int, c: int, height: int, width: int, diagonal: bool = True) -> list[tuple[int, int]]:
    """
    Gets valid neighbor coordinates for a given cell.

    Args:
        r: Row index of the cell.
        c: Column index of the cell.
        height: Grid height.
        width: Grid width.
        diagonal: Whether to include diagonal neighbors (default True).

    Returns:
        A list of valid (row, col) neighbor coordinates.
    """
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            # Skip the cell itself
            if dr == 0 and dc == 0:
                continue
            # Skip diagonals if diagonal is False
            if not diagonal and abs(dr) + abs(dc) > 1:
                continue

            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    height = len(input_grid)
    width = len(input_grid[0])

    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)

    # Identify patterns based on the input grid
    center_7_locations, outer_7_locations = find_777_patterns(input_grid)

    # Keep track of cells modified by higher priority rules
    modified_cells = set()

    # --- Priority 1: Apply Core Rule ---
    # Change center 7s to 6
    for r, c in center_7_locations:
        output_grid[r][c] = 6
        modified_cells.add((r, c))
    # Change outer 7s to 8
    for r, c in outer_7_locations:
        output_grid[r][c] = 8
        modified_cells.add((r, c))

    # --- Priority 2: Apply Vertical Neighbor Rule ---
    # Iterate through all grid cells
    for r in range(height):
        for c in range(width):
            # Skip if already modified
            if (r, c) in modified_cells:
                continue

            # Check condition: Input value is 8
            if input_grid[r][c] == 8:
                is_vert_neighbor_to_center = False
                # Check cell above (if exists)
                if r > 0 and (r - 1, c) in center_7_locations:
                    is_vert_neighbor_to_center = True
                # Check cell below (if exists)
                if not is_vert_neighbor_to_center and r < height - 1 and (r + 1, c) in center_7_locations:
                    is_vert_neighbor_to_center = True

                # Apply rule if condition met
                if is_vert_neighbor_to_center:
                    output_grid[r][c] = 6
                    modified_cells.add((r, c))

    # --- Priority 3: Apply Adjacent Neighbor Rule (Refined but likely incomplete) ---
    # Iterate through all grid cells
    for r in range(height):
        for c in range(width):
            # Skip if already modified
            if (r, c) in modified_cells:
                continue

            # Check condition 1: Input value is NOT 0, 3, 7, or 8
            input_val = input_grid[r][c]
            if input_val not in {0, 3, 7, 8}:
                # Check condition 2: Is adjacent to any outer 7 location
                is_adjacent_to_outer_7 = False
                neighbors = get_neighbors(r, c, height, width, diagonal=True)
                for nr, nc in neighbors:
                    if (nr, nc) in outer_7_locations:
                        is_adjacent_to_outer_7 = True
                        break # Found one, no need to check others

                # Apply rule if both conditions met
                if is_adjacent_to_outer_7:
                    output_grid[r][c] = 3
                    modified_cells.add((r, c))

    # --- Priority 4: Copy Rule (Implicit) ---
    # Cells not added to modified_cells retain their initial value from the deep copy.

    return output_grid