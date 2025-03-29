import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all distinct connected components (objects) of non-white pixels in the input grid using 4-way adjacency.
2. Determine the component with the largest number of pixels; this is the 'frame'. Store its color ('frame_color') and coordinates ('frame_coords').
3. If no non-white components exist, return the input grid unchanged.
4. Create a set of 'barrier_coords' containing the coordinates of *all* non-white pixels found in step 1 (including the frame and any internal objects).
5. Perform a Breadth-First Search (BFS) starting from all white (0) pixels located on the grid borders.
6. The BFS can only traverse white pixels and cannot enter any coordinates present in the 'barrier_coords' set.
7. Keep track of all white pixels visited by the BFS ('reachable_white_coords'). These are the white pixels connected to the outside.
8. Create the output grid as a copy of the input grid.
9. Iterate through every pixel (r, c) of the grid:
    a. If the pixel in the *input* grid `input_grid[r, c]` is white (0) AND its coordinate `(r, c)` is *not* in the 'reachable_white_coords' set:
        i. Set the corresponding pixel in the *output* grid `output_grid[r, c]` to the 'frame_color'.
10. Return the modified output grid.
"""

def find_all_components(grid):
    """
    Finds all connected components of non-white pixels using 4-way adjacency.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of tuples [(color, coords_set), ...], where each tuple
        represents a connected non-white component. Returns an empty list
        if no non-white pixels are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    all_components = [] # List to store (color, coords_set)

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # If the cell is non-white and hasn't been visited as part of a component yet
            if grid[r, c] != 0 and not visited[r, c]:
                # Start a BFS to find the connected component
                component_color = grid[r, c]
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True # Mark starting cell visited

                while q:
                    row, col = q.popleft()
                    component_coords.add((row, col))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                           # Check if neighbor has the same color and hasn't been visited
                           if grid[nr, nc] == component_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Store the found component (color and its coordinates)
                if component_coords: # Should always be true here
                    all_components.append((component_color, component_coords))

    return all_components

def find_reachable_white(grid, barrier_coords):
    """
    Finds white pixels reachable from the grid borders via white pixels,
    avoiding the specified barrier coordinates. Uses BFS.

    Args:
        grid: A numpy array representing the input grid.
        barrier_coords: A set of (row, col) tuples representing all barrier pixels
                       (typically all non-white pixels).

    Returns:
        A set of (row, col) tuples for the white pixels reachable from the border.
    """
    rows, cols = grid.shape
    # Keep track of visited/reachable white cells to avoid cycles and redundant work
    reachable_white = set()
    q = deque()

    # Initialize queue with all border white cells that are NOT barriers
    # Check top/bottom borders
    for c in range(cols):
        for r in [0, rows - 1]:
            coord = (r, c)
            # If it's white, not a barrier, and not already found/queued
            if grid[r, c] == 0 and coord not in barrier_coords and coord not in reachable_white:
                reachable_white.add(coord)
                q.append(coord)
    # Check left/right borders (excluding corners already checked)
    for r in range(1, rows - 1):
        for c in [0, cols - 1]:
            coord = (r, c)
            # If it's white, not a barrier, and not already found/queued
            if grid[r, c] == 0 and coord not in barrier_coords and coord not in reachable_white:
                reachable_white.add(coord)
                q.append(coord)

    # Perform BFS starting from the border white cells
    while q:
        r, c = q.popleft()
        # Explore orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor_coord = (nr, nc)

            # Check if neighbor is within grid bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is white, not a barrier, and not already visited/reachable
                if grid[nr, nc] == 0 and \
                   neighbor_coord not in barrier_coords and \
                   neighbor_coord not in reachable_white:
                    # Mark as reachable and add to queue for further exploration
                    reachable_white.add(neighbor_coord)
                    q.append(neighbor_coord)

    # Return the set of all white coordinates reachable from the border
    return reachable_white


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Fills enclosed white areas with the color of the largest non-white object,
    treating all non-white objects as barriers for the fill.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find all non-white connected components
    all_components = find_all_components(input_grid)

    # 2. Handle edge case: If no non-white components exist, return the original grid
    if not all_components:
        return output_grid

    # 3. Identify the largest component (the 'frame') by pixel count
    # The key for max is the length of the coordinate set (item[1])
    largest_component = max(all_components, key=lambda item: len(item[1]))
    frame_color = largest_component[0]
    # frame_coords = largest_component[1] # Not strictly needed after barriers are built

    # 4. Create a single set of barrier coordinates from ALL non-white components
    barrier_coords = set()
    for _, coords in all_components:
        barrier_coords.update(coords) # Add coordinates from current component

    # 5. Find all white pixels reachable from the border, avoiding barriers
    reachable_white_coords = find_reachable_white(input_grid, barrier_coords)

    # 6. Fill the 'internal' white pixels (those not reachable from the border)
    # Iterate through every cell in the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is white in the original input grid
            if input_grid[r, c] == 0:
                # Check if this white pixel's coordinate was NOT found by the reachability BFS
                if (r, c) not in reachable_white_coords:
                    # This is an internal, unreachable white pixel. Fill it.
                    output_grid[r, c] = frame_color
            # Else (if it's non-white or reachable white), it keeps its original color
            # (already handled by copying input_grid initially)

    # 7. Return the modified grid
    return output_grid