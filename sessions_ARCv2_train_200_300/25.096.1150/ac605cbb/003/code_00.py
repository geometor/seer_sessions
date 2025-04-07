import collections

"""
Transforms a 2D grid based on marker values (1, 2, 3, 6) and specific drawing rules.

1. Find all non-zero markers in the input grid.
2. For each marker, determine the coordinates/values for its corresponding pattern:
    - Marker 1 at (r, c): Draws [1, 5, 5] at [(r, c), (r, c+1), (r, c+2)] AND places a 'shadow' 1 at (r-1, c+2).
    - Marker 2 at (r, c): Draws [2, 5, 5, 5, 2] at [(r, c-4), (r, c-3), (r, c-2), (r, c-1), (r, c)].
    - Marker 3 at (r, c): Draws [3, 5, 5, 3] at [(r, c), (r+1, c), (r+2, c), (r+3, c)].
    - Marker 6 at (r, c): Draws [6, 5, ..., 5, 6] (length 7) at [(r-6, c), (r-5, c), ..., (r, c)].
3. Store endpoint values (1, 2, 3, 6) and the shadow '1' from marker 1 in a priority placement map.
4. Store path values (5) in a separate structure, tracking which marker(s) painted each cell.
5. Apply priority placements directly to the output grid.
6. Identify intersection cells where more than one marker painted a path (5).
7. Apply path (5) and intersection (4) colors:
    - If a cell is an intersection, write 4 to the output grid (overwriting priority placements if necessary, although unlikely by design).
    - If a cell was painted by only one path (5) AND the cell is currently 0 in the output grid, write 5.
8. For each intersection cell (now containing 4), draw a diagonal line of 4s starting one cell down-left and continuing down-left until the grid boundary (overwriting any existing values).
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Initialize output grid with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Structure to track cells painted with '5' and by which marker(s)
    # {(r, c): [marker_id_1, marker_id_2, ...]}
    path_painters = collections.defaultdict(list)
    
    # Structure to store placements that take priority (endpoints, shadow '1')
    # {(r, c): value}
    priority_placements = {}

    # --- 1. Find markers ---
    markers = []
    for r in range(rows):
        for c in range(cols):
            if input_grid[r][c] != 0:
                markers.append(((r, c), input_grid[r][c]))

    # --- 2. Calculate placements for each marker ---
    for (r, c), marker_value in markers:
        placements_to_process = [] # List of ((row, col), value)

        if marker_value == 1: # Horizontal right + shadow point
            # Line segment [1, 5, 5]
            placements_to_process.extend([((r, c), 1), ((r, c + 1), 5), ((r, c + 2), 5)])
            # Shadow point '1' at (r-1, c+2)
            placements_to_process.append(((r - 1, c + 2), 1))
        elif marker_value == 2: # Horizontal left [2, 5, 5, 5, 2]
            placements_to_process.extend([((r, c - 4), 2), ((r, c - 3), 5), ((r, c - 2), 5), ((r, c - 1), 5), ((r, c), 2)])
        elif marker_value == 3: # Vertical down [3, 5, 5, 3]
            placements_to_process.extend([((r, c), 3), ((r + 1, c), 5), ((r + 2, c), 5), ((r + 3, c), 3)])
        elif marker_value == 6: # Vertical up [6, 5, ..., 5, 6] (length 7)
            placements_to_process.extend([((r - 6, c), 6)] + [((r - i, c), 5) for i in range(5, 0, -1)] + [((r, c), 6)])

        # Process the calculated placements for the current marker
        for (nr, nc), val in placements_to_process:
            # Check boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                if val == 5:
                    # Record path painter
                    path_painters[(nr, nc)].append(marker_value)
                else:
                    # Record priority placement (endpoints or shadow '1')
                    priority_placements[(nr, nc)] = val

    # --- 3. Apply priority placements to output grid ---
    for (pr, pc), p_val in priority_placements.items():
         output_grid[pr][pc] = p_val

    # --- 4. Identify intersections ---
    intersection_coords = set()
    for (r_path, c_path), painters in path_painters.items():
        if len(painters) > 1:
            intersection_coords.add((r_path, c_path))

    # --- 5. Apply path (5) and intersection (4) colors ---
    for (r_path, c_path), painters in path_painters.items():
        if (r_path, c_path) in intersection_coords:
            # Intersection: Overwrite whatever is there with 4
            output_grid[r_path][c_path] = 4
        elif len(painters) == 1:
             # Single path: Only place '5' if the cell is currently 0
             if output_grid[r_path][c_path] == 0:
                 output_grid[r_path][c_path] = 5

    # --- 6. Draw diagonal lines from intersections ---
    # Sort intersections to ensure consistent drawing order if needed (though overwriting makes it less critical)
    sorted_intersections = sorted(list(intersection_coords)) 
    for (ir, ic) in sorted_intersections:
        # Start diagonal one step down-left from the intersection point itself
        dr, dc = ir + 1, ic - 1
        while 0 <= dr < rows and 0 <= dc < cols:
            # Diagonal overwrites everything in its path with 4
            output_grid[dr][dc] = 4
            dr += 1
            dc -= 1

    return output_grid