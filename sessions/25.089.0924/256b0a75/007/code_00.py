import numpy as np
from collections import deque

"""
Transformation Rule:
1.  Identify the minimum bounding box enclosing all azure (8) pixels in the input grid.
2.  Find all contiguous objects (using 4-way connectivity) within the input grid whose color is neither white (0) nor azure (8).
3.  Filter these objects to retain only those located entirely inside the calculated bounding box.
4.  Among the filtered, contained objects, determine the color ('fill_color') of the object with the largest size (pixel count). If there's a tie in size, choose the object with the numerically lowest color value.
5.  Initialize the output grid as a copy of the input grid.
6.  Identify all 'seed' pixels: pixels within the bounding box (inclusive) whose color in the *input* grid is white (0).
7.  Perform a flood fill operation starting from these seed pixels:
    a. Use the determined 'fill_color'.
    b. The fill propagates in 4 directions (up, down, left, right).
    c. Propagation only occurs into pixels whose color in the *input* grid is white (0).
    d. The fill is not constrained by the bounding box itself, only by non-white pixels in the input grid or grid boundaries.
8.  Pixels that were not white (0) in the input grid retain their original colors.
9.  If no azure (8) pixels are found, or if no non-white/non-azure objects are fully contained within the bounding box, or if no white 'seed' pixels are found within the bounding box, return the original grid unchanged.
"""

def find_objects(grid, ignore_colors=None, connectivity=4):
    """
    Finds all contiguous objects of the same color in a grid using BFS.

    Args:
        grid (np.array): The input grid.
        ignore_colors (set, optional): A set of color values to ignore. Defaults to None.
        connectivity (int): 4 or 8 for neighbor connectivity. Defaults to 4.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'coords' (tuple of sorted (r, c) tuples), and 'size'.
    """
    if ignore_colors is None:
        ignore_colors = set()
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    if connectivity == 4:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up
    elif connectivity == 8:
        deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] not in ignore_colors:
                color = grid[r, c]
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_visited = set([(r, c)])

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_coords.append((curr_r, curr_c))

                    for dr, dc in deltas:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           (nr, nc) not in current_object_visited:
                            visited[nr, nc] = True
                            current_object_visited.add((nr, nc))
                            q.append((nr, nc))

                if obj_coords:
                     objects.append({
                         'color': color,
                         'coords': tuple(sorted(obj_coords)),
                         'size': len(obj_coords)
                     })
    return objects

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the flood fill transformation based on the azure boundary and largest internal object.
    """
    # 1. Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Locate all azure (8) pixels
    azure_pixels = np.argwhere(input_grid == 8)

    # 3. Handle edge case: no azure pixels found
    if azure_pixels.size == 0:
        return output_grid

    # 4. Determine the minimum bounding box for azure pixels
    min_r = np.min(azure_pixels[:, 0])
    max_r = np.max(azure_pixels[:, 0])
    min_c = np.min(azure_pixels[:, 1])
    max_c = np.max(azure_pixels[:, 1])

    # 5. Find all distinct contiguous objects (not white=0, not azure=8) using 4-connectivity
    all_objects = find_objects(input_grid, ignore_colors={0, 8}, connectivity=4)

    # 6. Filter objects to find those fully contained within the bounding box
    contained_objects = []
    for obj in all_objects:
        is_contained = True
        for r, c in obj['coords']:
            # Check if *all* pixels of the object are within the bounds (inclusive)
            if not (min_r <= r <= max_r and min_c <= c <= max_c):
                is_contained = False
                break
        if is_contained:
            contained_objects.append(obj)

    # 7. Handle edge case: no objects are fully contained within the box
    if not contained_objects:
        return output_grid

    # 8. Sort contained objects: primary key size (descending), secondary key color (ascending)
    contained_objects.sort(key=lambda obj: (-obj['size'], obj['color']))

    # 9. Determine the fill color from the largest (and lowest color value in case of tie) object
    fill_color = contained_objects[0]['color']

    # 10. Identify seed pixels for flood fill (white pixels inside the bounding box)
    seed_pixels = []
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if input_grid[r, c] == 0:
                seed_pixels.append((r, c))

    # 11. Handle edge case: no white pixels inside the box to start the fill
    if not seed_pixels:
        return output_grid

    # 12. Perform flood fill
    q = deque(seed_pixels)
    # visited_flood tracks pixels already processed *by this flood fill*
    # Initialize with seeds because we start filling from these locations
    visited_flood = set(seed_pixels)
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)] # 4-connectivity for fill

    while q:
        r, c = q.popleft()

        # Fill the current pixel in the output grid
        output_grid[r, c] = fill_color

        # Check neighbors for potential filling
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc

            # Check conditions for filling the neighbor:
            # a) Within grid bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            # b) Original color was white (0) in the *input* grid
            if input_grid[nr, nc] != 0:
                continue
            # c) Not already visited/processed by *this* flood fill
            if (nr, nc) in visited_flood:
                continue

            # If all conditions met, add neighbor to queue and mark as visited
            visited_flood.add((nr, nc))
            q.append((nr, nc))

    # 13. Return the modified output grid
    return output_grid