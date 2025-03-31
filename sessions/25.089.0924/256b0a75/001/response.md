```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1.  Identify the minimum bounding box enclosing all azure (8) pixels in the input grid.
2.  Find all contiguous objects within the input grid whose color is neither white (0) nor azure (8).
3.  Filter these objects to retain only those that are located entirely inside the calculated bounding box.
4.  Determine the color of the largest object (by pixel count) among the filtered, contained objects. This is the "fill color".
5.  Create the output grid by copying the input grid.
6.  Iterate through all pixels within the bounding box in the output grid.
7.  If a pixel's corresponding location in the input grid was white (0), change its color in the output grid to the determined "fill color".
8.  Pixels outside the bounding box, the azure (8) boundary pixels themselves, and any non-white pixels originally inside the bounding box remain unchanged.
"""

def find_objects(grid, ignore_colors=None):
    """
    Finds all contiguous objects of the same color in a grid.

    Args:
        grid (np.array): The input grid.
        ignore_colors (set, optional): A set of color values to ignore. Defaults to None.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'coords' (list of (r, c) tuples), and 'size'.
    """
    if ignore_colors is None:
        ignore_colors = set()
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If not visited and not an ignored color, start a search (BFS)
            if not visited[r, c] and grid[r, c] not in ignore_colors:
                color = grid[r, c]
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_visited = set([(r,c)]) # Track visited for current BFS

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_coords.append((curr_r, curr_c))

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds, color match, and if not visited in *this specific BFS*
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           (nr, nc) not in current_object_visited:
                            
                            visited[nr, nc] = True # Mark globally visited
                            current_object_visited.add((nr, nc)) # Mark visited for this object search
                            q.append((nr, nc))
                            
                if obj_coords: # Add the found object to the list
                     objects.append({
                         'color': color,
                         'coords': obj_coords,
                         'size': len(obj_coords)
                     })
    return objects


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    """
    # 1. Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Locate all azure (8) pixels
    azure_pixels = np.argwhere(input_grid == 8)

    # If no azure pixels are found, return the original grid
    if azure_pixels.size == 0:
        return output_grid

    # 3. Determine the minimum bounding box for azure pixels
    min_r = np.min(azure_pixels[:, 0])
    max_r = np.max(azure_pixels[:, 0])
    min_c = np.min(azure_pixels[:, 1])
    max_c = np.max(azure_pixels[:, 1])

    # 4. Identify all distinct contiguous objects (not white=0, not azure=8)
    #    Uses a helper function `find_objects`.
    objects = find_objects(input_grid, ignore_colors={0, 8})

    # 5. Filter objects to find those fully contained within the bounding box
    contained_objects = []
    for obj in objects:
        is_contained = True
        # Check if *all* pixels of the object are within the bounds
        for r, c in obj['coords']:
            if not (min_r <= r <= max_r and min_c <= c <= max_c):
                is_contained = False
                break
        if is_contained:
            contained_objects.append(obj)

    # If no objects are fully contained within the box, return the grid as is
    # (no fill color can be determined)
    if not contained_objects:
        return output_grid

    # 6. Find the largest object among the contained ones
    largest_object = max(contained_objects, key=lambda obj: obj['size'])

    # 7. Determine the fill color from the largest object
    fill_color = largest_object['color']

    # 8. Iterate through each pixel within the bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            # 9. Check if the pixel in the *input* grid is white (0)
            if input_grid[r, c] == 0:
                # 10. If it is white, change its color in the *output* grid to the fill color
                output_grid[r, c] = fill_color

    # 11. Pixels outside the box, boundary pixels, and non-white pixels inside
    #     retain their original colors (already handled by copying initially and
    #     only modifying white pixels inside the box).
    return output_grid
```