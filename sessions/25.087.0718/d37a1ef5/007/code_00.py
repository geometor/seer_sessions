import numpy as np
from collections import deque

"""
Transformation Rule:
1. Find all separate connected groups (objects) of non-white pixels in the input grid, using 4-way (up, down, left, right) connections.
2. If no non-white objects exist, return the input grid unchanged.
3. Identify the object with the most pixels; this is the 'frame'. Note its color ('frame_color').
4. Identify all other non-white objects besides the frame; these are the 'internal objects'. Create a set of coordinates for all pixels belonging to internal objects ('internal_object_coords').
5. Create the output grid as a copy of the input grid.
6. Iterate through every pixel location (r, c) in the input grid.
7. If the pixel at (r, c) in the *input* grid is white (color 0):
    a. Perform a flood fill (BFS) starting from (r, c), visiting only adjacent white pixels (4-way).
    b. Determine if this flood fill reaches the border of the grid.
    c. If the flood fill *does not* reach the border (i.e., the white area is enclosed):
        i. Check if the original white pixel (r, c) is orthogonally adjacent to any pixel in `internal_object_coords`.
        ii. If the white pixel (r, c) is enclosed AND *not* adjacent to any internal object pixel, change the color of the pixel at (r, c) in the *output* grid to `frame_color`.
8. Return the output grid.
"""

def find_all_components(grid):
    """
    Finds all connected components of non-white pixels using 4-way adjacency.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of tuples [(color, coords_set), ...], where each tuple
        represents a connected non-white component. Returns an empty list
        if no non-white pixels are found. Components are sorted by size descending.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    all_components = [] # List to store (color, coords_set)
    non_white_coords = set() # Keep track of all non-white coords for faster lookup

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
                    non_white_coords.add((row, col)) # Add to overall non-white set

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                           # Check if neighbor has the same color and hasn't been visited
                           # Optimization: Check if it's non-white first
                           if grid[nr, nc] == component_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                # Store the found component (color and its coordinates)
                if component_coords: # Should always be true here
                    all_components.append((component_color, component_coords))

    # Sort components by size (number of coordinates) in descending order
    all_components.sort(key=lambda item: len(item[1]), reverse=True)

    return all_components, non_white_coords


def check_white_pixel_enclosure_and_adjacency(r, c, grid, non_white_coords, internal_object_coords):
    """
    Checks if a starting white pixel (r, c) belongs to an enclosed white area
    and if it's adjacent to any internal object.

    Args:
        r: Starting row of the white pixel.
        c: Starting column of the white pixel.
        grid: The input numpy grid.
        non_white_coords: A set of all non-white pixel coordinates.
        internal_object_coords: A set of coordinates for internal objects.

    Returns:
        A tuple (is_enclosed, is_adjacent_to_internal):
        - is_enclosed (bool): True if the white area containing (r,c) does not reach the border.
        - is_adjacent_to_internal (bool): True if the pixel (r,c) is orthogonally adjacent
          to any internal object pixel.
    """
    rows, cols = grid.shape
    q = deque([(r, c)])
    visited_white = set([(r, c)])
    reaches_border = False

    # Check initial adjacency to internal objects
    is_adjacent_to_internal = False
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if (nr, nc) in internal_object_coords:
            is_adjacent_to_internal = True
            break # Found one adjacent internal pixel, no need to check others

    # BFS to check if the white area reaches the border
    while q:
        curr_r, curr_c = q.popleft()

        # Check if current pixel is on the border
        if curr_r == 0 or curr_r == rows - 1 or curr_c == 0 or curr_c == cols - 1:
            reaches_border = True
            # We can stop the BFS early if border is reached, as we only need to know *if* it reaches
            break

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = curr_r + dr, curr_c + dc
            neighbor_coord = (nr, nc)

            # Check bounds, if it's white, and not visited in *this specific BFS*
            if 0 <= nr < rows and 0 <= nc < cols and \
               neighbor_coord not in non_white_coords and \
               neighbor_coord not in visited_white:
                visited_white.add(neighbor_coord)
                q.append(neighbor_coord)

    is_enclosed = not reaches_border
    return is_enclosed, is_adjacent_to_internal


def transform(input_grid):
    """Applies the transformation rule to the input grid."""
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Identify all non-white connected components and all non-white coords
    all_components, non_white_coords = find_all_components(input_grid)

    # 2. Handle edge case: If no non-white components exist, return original grid
    if not all_components:
        return output_grid

    # 3. Identify the largest component (the 'frame') and its color
    frame_component = all_components[0]
    frame_color = frame_component[0]
    # frame_coords = frame_component[1] # Not directly needed now

    # 4. Identify internal objects and collect their coordinates
    internal_object_coords = set()
    if len(all_components) > 1:
        for _, coords in all_components[1:]: # Skip the first (largest) component
            internal_object_coords.update(coords)

    # 5. Output grid is already initialized

    # 6. & 7. Iterate through each pixel
    for r in range(rows):
        for c in range(cols):
            coord = (r, c)
            # Check if the pixel is white in the original input grid
            if input_grid[r, c] == 0:
                # Check if this white pixel is enclosed and not adjacent to internal objects
                is_enclosed, is_adjacent = check_white_pixel_enclosure_and_adjacency(
                    r, c, input_grid, non_white_coords, internal_object_coords
                )

                # 7.c.ii: Fill if enclosed and NOT adjacent to internal
                if is_enclosed and not is_adjacent:
                    output_grid[r, c] = frame_color

    # 8. Return the modified grid
    return output_grid