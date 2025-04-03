"""
Transforms an input grid by identifying 'frame' colors and 'inner' colors. 
An inner color cell is changed to the adjacent frame color if it's not reachable 
from the background (color 0) when the specific frame color is treated as a wall, 
and if it is directly adjacent to a cell of that frame color. This process is 
repeated for every unique non-zero color acting as a potential frame.
"""

import numpy as np
from collections import deque

def _get_neighbors(r, c, rows, cols):
    """ Helper to get valid 4-connectivity neighbors coordinates. """
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def _flood_fill(grid, start_coords, wall_colors_set):
    """
    Performs a flood fill (BFS) starting from start_coords.
    Returns a set of reachable coordinates, avoiding cells with colors in wall_colors_set.
    """
    rows, cols = grid.shape
    q = deque()
    reachable = set()
    visited = set() # Keep track of visited to avoid cycles and redundant checks

    # Initialize queue and visited set with valid starting points
    for r, c in start_coords:
        if grid[r, c] not in wall_colors_set:
            if (r,c) not in visited:
                q.append((r, c))
                visited.add((r,c))
                reachable.add((r,c)) # Start coords are reachable if not walls

    # Perform BFS
    while q:
        r, c = q.popleft()
        # Current cell (r,c) is already added to reachable when added to queue

        for nr, nc in _get_neighbors(r, c, rows, cols):
            neighbor_coord = (nr, nc)
            # Check if neighbor is reachable: not already visited and not a wall color
            if neighbor_coord not in visited and grid[nr, nc] not in wall_colors_set:
                visited.add(neighbor_coord)
                reachable.add(neighbor_coord) # Mark as reachable
                q.append(neighbor_coord)

    return reachable

def transform(input_grid):
    """
    Applies the frame-fill transformation to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape

    # 1. Create an output_grid as an identical copy of the input_grid.
    output_grid = np.copy(input_grid_np)

    # 2. Identify the set of all unique non-zero colors present in the input_grid.
    potential_frame_colors = np.unique(input_grid_np[input_grid_np != 0])
    if len(potential_frame_colors) == 0: # Handle empty or all-zero grids
        return input_grid # No transformation needed

    # 3. Identify the coordinates of all cells in the input_grid with color 0.
    background_coords = list(zip(*np.where(input_grid_np == 0)))

    # 4. For each potential_frame_color:
    for frame_color in potential_frame_colors:
        # a. Perform flood fill from background, treating frame_color as wall.
        wall_set = {frame_color}
        external_cells_relative_to_frame = _flood_fill(input_grid_np, background_coords, wall_set)

        # b. Iterate through every cell coordinate (r, c).
        for r in range(rows):
            for c in range(cols):
                coord = (r, c)
                current_color = input_grid_np[r, c]

                # c.i. Check if current_color is 0 or the frame_color itself. Skip if true.
                if current_color == 0 or current_color == frame_color:
                    continue

                # c.ii. Check if the cell is external relative to this frame_color. Skip if true.
                if coord in external_cells_relative_to_frame:
                    continue

                # c.iii. Check if any neighbor has the frame_color (in the *input* grid).
                has_frame_neighbor = False
                for nr, nc in _get_neighbors(r, c, rows, cols):
                    if input_grid_np[nr, nc] == frame_color:
                        has_frame_neighbor = True
                        break

                # c.iv. If all conditions pass (not 0, not frame_color, not external, has frame neighbor),
                #      update the output_grid cell to frame_color.
                #      Important: update the output_grid, not the input_grid_np being read.
                if has_frame_neighbor:
                    output_grid[r, c] = frame_color

    # 5. Return the final output_grid, converted back to list of lists.
    return output_grid.tolist()