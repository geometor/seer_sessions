import numpy as np
from collections import deque

"""
Transformation Rule:
1.  Identify the minimum bounding box enclosing all azure (8) pixels in the input grid.
2.  Find all contiguous objects within the input grid (using 4-way connectivity) whose color is neither white (0) nor azure (8).
3.  Filter these objects to retain only those that are located entirely inside or on the boundary of the calculated bounding box.
4.  Among the filtered, contained objects, determine the color ('fill_color') of the object with the largest size (pixel count). If there's a tie in size, choose the object with the numerically lowest color value.
5.  Create the output grid by copying the input grid.
6.  Iterate through all pixels within the bounding box (inclusive).
7.  If a pixel's corresponding location in the *input* grid was white (0), change its color in the *output* grid to the determined 'fill_color'.
8.  Pixels outside the bounding box, the azure (8) boundary pixels themselves, and any non-white pixels originally inside the bounding box remain unchanged.
9.  If no azure pixels are found, or if no non-white/non-azure objects are found fully contained within the bounding box, return the original grid unchanged.
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
              and contains 'color', 'coords' (list of (r, c) tuples), and 'size'.
    """
    if ignore_colors is None:
        ignore_colors = set()
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    if connectivity == 4:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up
    elif connectivity == 8:
        # 8-way connectivity (including diagonals)
        deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for r in range(rows):
        for c in range(cols):
            # If not visited and not an ignored color, start a Breadth-First Search (BFS)
            if not visited[r, c] and grid[r, c] not in ignore_colors:
                color = grid[r, c]
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                # Use a separate set for current BFS to handle visited status correctly within the object search
                # This prevents re-adding pixels belonging to the *same* object currently being explored.
                current_object_visited = set([(r, c)])

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_coords.append((curr_r, curr_c))

                    # Check neighbors based on specified connectivity
                    for dr, dc in deltas:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check bounds, color match, and if not visited in this specific BFS
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           (nr, nc) not in current_object_visited:

                            visited[nr, nc] = True # Mark globally visited to avoid starting new searches from here
                            current_object_visited.add((nr, nc)) # Mark visited for this object search
                            q.append((nr, nc))

                # Add the found object to the list if it has coordinates
                if obj_coords:
                     objects.append({
                         'color': color,
                         'coords': tuple(sorted(obj_coords)), # Use sorted tuple for consistency
                         'size': len(obj_coords)
                     })
    return objects


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to fill white space within an azure-defined
    bounding box with the color of the largest contained object.
    """
    # 1. Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Locate all azure (8) pixels
    azure_pixels = np.argwhere(input_grid == 8)

    # 3. If no azure pixels are found, return the original grid copy
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
        # Check if *all* pixels of the object are within the bounds (inclusive)
        for r, c in obj['coords']:
            if not (min_r <= r <= max_r and min_c <= c <= max_c):
                is_contained = False
                break
        if is_contained:
            contained_objects.append(obj)

    # 7. If no objects are fully contained within the box, return the original grid copy
    if not contained_objects:
        return output_grid

    # 8. Sort contained objects: primary key size (descending), secondary key color (ascending)
    contained_objects.sort(key=lambda obj: (-obj['size'], obj['color']))

    # 9. Determine the fill color from the largest (and lowest color value in case of tie) object
    fill_color = contained_objects[0]['color']

    # 10. Iterate through each pixel within the bounding box (inclusive)
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # 11. Check if the pixel in the *input* grid is white (0)
            if input_grid[r, c] == 0:
                # 12. If it is white, change its color in the *output* grid to the fill color
                output_grid[r, c] = fill_color

    # 13. Return the modified output grid
    return output_grid