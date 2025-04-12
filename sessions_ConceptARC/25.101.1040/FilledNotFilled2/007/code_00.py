import numpy as np
from collections import deque

"""
Determines the dimensions of an all-white output grid based on comparing properties
of objects in the input grid. It calculates two potential dimension sets:
1. Dims_A: Based on a 'special object' (where height equals color value), only
   applicable if the number of objects (N) equals the number of unique colors (C)
   and such an object exists. Dimensions are height x width of that object.
2. Dims_B: Based on the maximum height (MaxH) of any object and the number of
   unique colors (C). Dimensions are MaxH x max(0, C - 1).

The final output dimensions are chosen by selecting the dimension set (A or B)
that results in the larger grid area (Height * Width). If Set A is applicable
and the areas are equal, Set A is chosen. The resulting grid is filled with
white pixels (0).
"""

def find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous objects of non-white colors in the grid using
    Breadth-First Search (4-way adjacency).

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its color, pixels, bounding box coordinates, height, and width.
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
    Applies the transformation rule based on object properties and the 'max area'
    selection criterion between two dimension calculation methods.
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
    max_height = max(obj['height'] for obj in objects) # Guaranteed > 0

    # 3. Calculate Potential Dimensions B (Dims_B) and its area (Area_B).
    # Dims_B = MaxH x max(0, C - 1)
    h_B = max_height
    w_B = max(0, num_unique_colors - 1)
    dims_B = (h_B, w_B)
    area_B = h_B * w_B

    # 4. Initialize Potential Dimensions A (Dims_A) and Area_A as not applicable.
    dims_A = None
    area_A = -1 # Use -1 to indicate not applicable or area 0

    # 5. Check if N == C to determine if Dims_A can be calculated.
    if num_objects == num_unique_colors:
        # 5a. Search for a "special object" where height == color.
        for obj in objects:
            if obj['height'] == obj['color']:
                # 5b. If found, calculate Dims_A and Area_A.
                h_A = obj['height']
                w_A = obj['width']
                dims_A = (h_A, w_A)
                area_A = h_A * w_A
                break # Assume only one such object matters or take the first

    # 6. Select Final Dimensions based on the 'max area' rule.
    final_dims = None
    # Choose A if it's applicable (dims_A is not None) AND its area is >= Area B
    if dims_A is not None and area_A >= area_B:
        final_dims = dims_A
    else:
        # Otherwise, choose B (either A wasn't applicable or B had a larger area)
        final_dims = dims_B

    # 7. Ensure final dimensions are at least 1x1.
    final_height = max(1, final_dims[0])
    final_width = max(1, final_dims[1])

    # 8. Create the output grid with the final dimensions, filled with white (0).
    output_grid_np = np.zeros((final_height, final_width), dtype=int)

    # 9. Convert back to list of lists and return.
    return output_grid_np.tolist()