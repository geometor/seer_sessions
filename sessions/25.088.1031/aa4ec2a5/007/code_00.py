import numpy as np
from collections import deque

# Define colors
BLUE = 1
RED = 2
GREEN = 3
YELLOW = 4
GRAY = 5
MAGENTA = 6
ORANGE = 7
AZURE = 8
MAROON = 9
WHITE = 0


def _get_neighbors(r, c, height, width, include_diagonal=True):
    """ Gets valid neighbor coordinates for a given cell. """
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            # Check for diagonal exclusion if specified
            if not include_diagonal and abs(dr) + abs(dc) > 1:
                continue
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def _find_connected_yellow(start_nodes, yellow_coords, height, width):
    """ Find all yellow coordinates connected to the start_nodes using BFS. """
    q = deque(list(start_nodes))
    visited = set(start_nodes)
    connected_region = set(start_nodes) # Include the starting frame pixels

    while q:
        r, c = q.popleft()

        # Explore neighbors
        for nr, nc in _get_neighbors(r, c, height, width, include_diagonal=True):
            coord = (nr, nc)
            # Check if neighbor is yellow and not visited yet
            if coord in yellow_coords and coord not in visited:
                visited.add(coord)
                connected_region.add(coord)
                q.append(coord)

    return connected_region


def transform(input_grid):
    """
    Transforms the input grid based on layered adjacency rules starting from Blue pixels
    and propagating through connected Yellow pixels.

    1. Initialize the output grid as a copy of the input grid.
    2. Identify coordinates of all Blue (1) and initial Yellow (4) pixels.
    3. Identify 'Frame' Yellow pixels: Those Yellow pixels adjacent (orthogonally or diagonally) to any Blue pixel.
    4. Change the color of 'Frame' pixels to Red (2) in the output grid.
    5. Identify the 'Region of Interest' (ROI): All Yellow pixels belonging to the same connected component(s) as the 'Frame' pixels. This uses BFS starting from the Frame pixels and exploring only through other Yellow pixels.
    6. Identify 'Outer Fill' pixels (Azure, 8): These are Yellow pixels within the ROI (but not Frame pixels) that are adjacent to at least one Red 'Frame' pixel.
    7. Identify 'Inner Fill' pixels (Magenta, 6): These are the remaining Yellow pixels within the ROI that were not turned Red or Azure.
    8. Update the output grid with Azure and Magenta colors.
    9. Original Blue pixels remain Blue. Yellow pixels outside the ROI remain Yellow. Other original colors (if any) remain unchanged.
    """
    # 1. Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 2. Identify coordinates of all blue and yellow pixels
    blue_coords = set(map(tuple, np.argwhere(input_grid == BLUE)))
    initial_yellow_coords = set(map(tuple, np.argwhere(input_grid == YELLOW)))

    # Handle edge cases with no blue or no yellow pixels
    if not blue_coords or not initial_yellow_coords:
        return output_grid # No transformation possible

    # 3. Find all yellow pixels adjacent to blue pixels ('frame_coords')
    frame_coords = set()
    for r_yellow, c_yellow in initial_yellow_coords:
        is_adjacent_to_blue = False
        # Check all 8 neighbors (including diagonals)
        neighbors = _get_neighbors(r_yellow, c_yellow, height, width, include_diagonal=True)
        for nr, nc in neighbors:
            if (nr, nc) in blue_coords:
                is_adjacent_to_blue = True
                break
        if is_adjacent_to_blue:
            frame_coords.add((r_yellow, c_yellow))

    # 4. Change 'frame' pixels to red in the output grid
    for r, c in frame_coords:
        output_grid[r, c] = RED

    # If no frame was created (e.g., blue and yellow not adjacent), return
    if not frame_coords:
         return output_grid

    # 5. Identify the 'Region of Interest' (ROI) using BFS
    # Start BFS from the frame_coords, exploring only within initial_yellow_coords
    yellow_roi = _find_connected_yellow(frame_coords, initial_yellow_coords, height, width)

    # 6. Classify remaining yellow pixels *within the ROI*
    outer_fill_coords = set()
    # Consider only yellows in the ROI that are not already frames
    potential_outer_fill = yellow_roi - frame_coords

    for r_rem, c_rem in potential_outer_fill:
        is_adjacent_to_red = False
        neighbors = _get_neighbors(r_rem, c_rem, height, width, include_diagonal=True)
        # Check adjacency against the *final* set of frame coordinates (now RED)
        for nr, nc in neighbors:
            if (nr, nc) in frame_coords: # Check if neighbor became red
                is_adjacent_to_red = True
                break
        if is_adjacent_to_red:
            outer_fill_coords.add((r_rem, c_rem))

    # 7. Determine inner fill coordinates accurately - must be within ROI
    # Inner fill are those in the ROI not part of frame or outer fill
    inner_fill_coords = yellow_roi - frame_coords - outer_fill_coords

    # 8. Update the output grid with azure and magenta colors
    for r, c in outer_fill_coords:
        output_grid[r, c] = AZURE
    for r, c in inner_fill_coords:
        output_grid[r, c] = MAGENTA

    # 9. Original blue, other colors, and yellows outside the ROI remain unchanged
    #    because we started with a copy and only modified specific yellow pixels within the ROI.
    #    (Blue pixel modification logic is omitted for now due to uncertainty).

    return output_grid