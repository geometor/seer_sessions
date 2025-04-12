import numpy as np
from collections import deque

"""
Determines the dimensions of an all-white output grid based on properties of objects in the input grid.
The core logic compares the number of distinct objects (N) to the number of unique non-white colors (C).

1. If N equals C, it searches for an object where its height matches its color value. The output grid dimensions become the height and width of that specific object. If no such object exists, it defaults to the N != C rule.
2. If N does not equal C, the output grid dimensions are set to the maximum height (MaxH) found among all objects by (C - 1).
3. The final output grid is filled entirely with white pixels (0).
"""


def find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous objects of non-white colors in the grid using Breadth-First Search.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its color, pixels (list of tuples), bounding box coordinates
        (min_r, max_r, min_c, max_c), height, and width.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if the cell is non-white and not yet visited
            if color != 0 and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Perform BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    # Update bounding box coordinates
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional adjacency)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Calculate height and width from bounding box
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'min_r': min_r, 'max_r': max_r,
                    'min_c': min_c, 'max_c': max_c,
                    'height': height,
                    'width': width
                })
    return objects

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid into an all-white grid whose dimensions
    are determined by the rules based on object counts, colors, and heights.
    """
    grid_np = np.array(input_grid, dtype=int)

    # 1. Identify all distinct non-white objects and their properties.
    objects = find_objects(grid_np)

    # Handle edge case: If there are no non-white objects, return a 1x1 white grid.
    if not objects:
        return [[0]]

    # 2. Calculate N (number of objects), C (number of unique colors), and MaxH (max height).
    num_objects = len(objects)
    unique_colors = set(obj['color'] for obj in objects)
    num_unique_colors = len(unique_colors)
    max_height = max(obj['height'] for obj in objects) # Guaranteed > 0 if objects exist

    output_height = 0
    output_width = 0

    # 3. Apply rules based on comparing N and C.
    if num_objects == num_unique_colors:
        # Rule 1: N == C
        found_special_object = False
        # 3a. Search for an object where height == color.
        for obj in objects:
            if obj['height'] == obj['color']:
                # 3b. If found, use its dimensions.
                output_height = obj['height']
                output_width = obj['width']
                found_special_object = True
                break
        # 3c. Fallback: If no such object is found, use the N != C rule.
        if not found_special_object:
            output_height = max_height
            output_width = max(0, num_unique_colors - 1) # Ensure width is not negative
    else:
        # Rule 2: N != C
        # 3d. Use MaxH for height and (C - 1) for width.
        output_height = max_height
        output_width = max(0, num_unique_colors - 1) # Ensure width is not negative

    # 4. Handle potential zero dimensions for the output grid. Default to 1x1 if needed.
    #    (Although current logic with max(0, C-1) should prevent negative widths,
    #     and height should be > 0 if objects exist. Width could be 0 if C=1).
    if output_height <= 0 or output_width <= 0:
         output_height = max(1, output_height)
         output_width = max(1, output_width)


    # 5. Create the output grid with the determined dimensions, filled with white (0).
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # 6. Convert back to list of lists and return.
    return output_grid_np.tolist()