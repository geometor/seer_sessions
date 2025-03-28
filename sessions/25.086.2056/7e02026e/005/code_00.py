"""
Identifies all distinct contiguous regions composed entirely of 'white' (0) pixels in the input grid.
For each identified 'white' region, determines two properties:
a. Boundary Contact: Checks if any pixel belonging to this region lies on the outermost border (top, bottom, left, or right edge) of the grid.
b. Adjacent Colors: Finds all non-'white' pixels that are directly adjacent (up, down, left, or right) to any pixel within this 'white' region. Collects the set of unique colors of these adjacent non-'white' pixels.

Examines the properties for each 'white' region:
a. If a 'white' region does not have Boundary Contact (i.e., it is fully enclosed within the grid) AND its set of Adjacent Colors contains only 'azure' (8), then this region qualifies for transformation.
b. If a 'white' region touches the boundary, or if its adjacent non-'white' neighbors include colors other than 'azure', or if it has no non-'white' neighbors, it does not qualify.

Creates the output grid:
a. For every 'white' region that qualifies for transformation (met conditions above), changes the color of all pixels within that region to 'green' (3).
b. All other pixels (those in non-qualifying 'white' regions, and all non-'white' pixels) retain their original color from the input grid.
"""

import collections

# Define colors (using names for clarity in the code)
WHITE = 0
GREEN = 3
AZURE = 8

def _find_and_analyze_white_region(input_grid, visited, start_r, start_c):
    """
    Performs BFS starting from (start_r, start_c) to find a connected white region.
    Analyzes if the region touches the boundary and collects adjacent non-white colors.

    Args:
        input_grid: The input grid (list of lists).
        visited: A grid (list of lists) tracking visited white cells.
        start_r: The starting row for the BFS.
        start_c: The starting column for the BFS.

    Returns:
        A tuple: (region_coords, touches_boundary, neighbor_colors)
        - region_coords: A list of (r, c) tuples for all pixels in the region.
        - touches_boundary: Boolean, True if the region touches the grid edge.
        - neighbor_colors: A set of colors adjacent to the region (excluding white).
    """
    height = len(input_grid)
    width = len(input_grid[0])

    region_coords = []
    touches_boundary = False
    neighbor_colors = set()
    queue = collections.deque([(start_r, start_c)])
    visited[start_r][start_c] = True

    while queue:
        curr_r, curr_c = queue.popleft()
        region_coords.append((curr_r, curr_c))

        # Check boundary contact
        if curr_r == 0 or curr_r == height - 1 or curr_c == 0 or curr_c == width - 1:
            touches_boundary = True

        # Explore neighbors (4 directions)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_color = input_grid[nr][nc]
                # If neighbor is white and not visited, add to queue
                if neighbor_color == WHITE and not visited[nr][nc]:
                    visited[nr][nc] = True
                    queue.append((nr, nc))
                # If neighbor is not white, record its color
                elif neighbor_color != WHITE:
                    neighbor_colors.add(neighbor_color)
            # Neighbor outside bounds implicitly handled by boundary check within the loop

    return region_coords, touches_boundary, neighbor_colors


def transform(input_grid):
    """
    Transforms the input grid based on enclosed white regions bordered only by azure.

    Args:
        input_grid: A list of lists representing the input grid (integers 0-9).

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a copy of the input
    output_grid = [row[:] for row in input_grid]

    # Visited grid to keep track of processed white pixels during BFS
    visited = [[False for _ in range(width)] for _ in range(height)]

    # Iterate through each cell (pixel) of the grid
    for r in range(height):
        for c in range(width):
            # If a white cell is found that hasn't been processed yet
            if input_grid[r][c] == WHITE and not visited[r][c]:
                # Find the connected white region and analyze its properties
                region_coords, touches_boundary, neighbor_colors = \
                    _find_and_analyze_white_region(input_grid, visited, r, c)

                # Check if the conditions for transformation are met:
                # 1. The region does NOT touch the boundary.
                # 2. The set of non-white neighbors contains ONLY Azure (8).
                if not touches_boundary and neighbor_colors == {AZURE}:
                    # If conditions met, change the color of all pixels in this region to green
                    for pr, pc in region_coords:
                        output_grid[pr][pc] = GREEN

    # Return the modified grid
    return output_grid