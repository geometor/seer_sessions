import numpy as np
from collections import deque

"""
Identifies connected blue (1) objects in the input grid.
For each object:
1. Finds all adjacent (including diagonal) yellow (4) pixels, marking them as the border.
2. Determines if the area enclosed by the border (including the original blue pixels and potentially some yellow pixels) contained only blue pixels or both blue and yellow pixels in the input.
   - "Enclosed" yellow pixels are those yellow pixels in the input that are not part of the border and are not reachable from the grid edges without crossing the border or the blue object. This is determined using a flood fill from the edges.
3. If the enclosed area was originally only blue (no enclosed yellow pixels found):
   - Change the border pixels to red (2).
   - The original blue pixels remain blue (1).
4. If the enclosed area was originally blue and yellow (enclosed yellow pixels were found):
   - Change the border pixels to red (2).
   - Change the original blue pixels to azure (8).
   - Change the enclosed yellow pixels:
     - to azure (8) if they are adjacent (including diagonal) to any red border pixel (belonging to the current object's border).
     - to magenta (6) otherwise.
Pixels not part of any object transformation remain their original color.
"""

# Define color constants for better readability
BLUE = 1
RED = 2
YELLOW = 4
MAGENTA = 6
AZURE = 8


def find_objects(grid, color):
    """
    Finds all connected components (objects) of a specific color in the grid.
    Connectivity includes diagonals (8-way).
    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.
    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of one object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If it's the target color and not yet visited, start a new object search (BFS)
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds and if neighbor is the same color and unvisited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects


def get_neighbors(r, c, height, width, diagonal=True):
    """
    Gets valid neighbor coordinates for a given cell (r, c).
    Args:
        r (int): Row index.
        c (int): Column index.
        height (int): Grid height.
        width (int): Grid width.
        diagonal (bool): Include diagonal neighbors if True.
    Returns:
        list[tuple]: List of valid (row, col) neighbor coordinates.
    """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            # Skip diagonals if diagonal is False (though not used in this problem)
            if not diagonal and (dr != 0 and dc != 0):
                 continue
            nr, nc = r + dr, c + dc
            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors


def transform(input_grid):
    # Convert input list of lists to a NumPy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    height, width = input_grid_np.shape

    # Find all connected blue objects
    blue_objects = find_objects(input_grid_np, BLUE)

    # Process each blue object independently
    for blue_coords in blue_objects:
        border_coords = set()

        # Step 1: Find border pixels for the current blue object.
        # Border pixels are yellow pixels adjacent (8-way) to any blue pixel of this object.
        for r, c in blue_coords:
            for nr, nc in get_neighbors(r, c, height, width, diagonal=True):
                # Check if the neighbor is yellow
                if input_grid_np[nr, nc] == YELLOW:
                    border_coords.add((nr, nc))

        # Step 2: Determine internal yellow pixels using a flood fill approach.
        # Create a barrier map where 1 indicates a barrier (blue object pixel or border pixel)
        # and 0 indicates a traversable space.
        barrier_map = np.zeros_like(input_grid_np, dtype=int)
        for r, c in blue_coords:
            barrier_map[r, c] = 1
        for r, c in border_coords:
            barrier_map[r, c] = 1 # Mark border pixels as barriers as well

        # Initialize flood fill map: 0 = unknown, 1 = barrier, 2 = external/reachable from edge
        flood_fill_map = np.copy(barrier_map)
        q = deque()

        # Seed the flood fill queue with all non-barrier pixels along the grid edges.
        for r in range(height):
            for c in [0, width - 1]: # Left and right edges
                if flood_fill_map[r, c] == 0: # If not a barrier
                    q.append((r, c))
                    flood_fill_map[r, c] = 2 # Mark as external
        for c in range(1, width - 1): # Top and bottom edges (avoiding corners)
            for r in [0, height - 1]:
                if flood_fill_map[r, c] == 0: # If not a barrier
                    q.append((r, c))
                    flood_fill_map[r, c] = 2 # Mark as external

        # Perform the flood fill (8-way connectivity) to mark all reachable non-barrier pixels.
        while q:
            r, c = q.popleft()
            for nr, nc in get_neighbors(r, c, height, width, diagonal=True):
                # If the neighbor is not a barrier (0) and hasn't been visited/marked external yet
                if flood_fill_map[nr, nc] == 0:
                    flood_fill_map[nr, nc] = 2 # Mark as external
                    q.append((nr, nc))

        # Identify internal yellow pixels:
        # These are pixels that were originally yellow, are not part of the border set,
        # and were not reached by the flood fill (i.e., flood_fill_map value is not 2).
        internal_yellow_coords = set()
        for r in range(height):
            for c in range(width):
                is_original_yellow = (input_grid_np[r, c] == YELLOW)
                is_not_border = ((r, c) not in border_coords)
                is_not_external = (flood_fill_map[r, c] != 2)

                if is_original_yellow and is_not_border and is_not_external:
                    internal_yellow_coords.add((r, c))

        # Step 3 & 4: Apply coloring rules based on the presence of internal yellow pixels.

        # Always change the border pixels to red in the output grid.
        for r, c in border_coords:
            output_grid[r, c] = RED

        # Check if any internal yellow pixels were found for this object.
        if not internal_yellow_coords:
            # Case 3: Only blue inside. Blue pixels remain blue (1).
            # No change needed as output_grid is initialized from input.
            pass
        else:
            # Case 4: Blue and yellow inside.
            # Change original blue pixels to azure (8).
            for r, c in blue_coords:
                output_grid[r, c] = AZURE

            # Change internal yellow pixels based on adjacency to the red border.
            # Use the 'border_coords' set calculated specifically for this object.
            for r, c in internal_yellow_coords:
                is_adj_to_border = False
                # Check 8 neighbors of the internal yellow pixel
                for nr, nc in get_neighbors(r, c, height, width, diagonal=True):
                    # If any neighbor is a border pixel for this object
                    if (nr, nc) in border_coords:
                        is_adj_to_border = True
                        break # Found an adjacent border pixel, no need to check further

                # Apply coloring based on adjacency result
                if is_adj_to_border:
                    output_grid[r, c] = AZURE    # Change to azure
                else:
                    output_grid[r, c] = MAGENTA  # Change to magenta

    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()