```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1.  Identify the minimum bounding box enclosing all azure (8) pixels.
2.  Find all contiguous objects within the input grid whose color is neither white (0) nor azure (8).
3.  Filter these objects to retain only those located entirely inside the calculated bounding box.
4.  Determine the color ('fill_color') of the largest object (by pixel count) among the filtered, contained objects.
5.  Identify all 'seed pixels': pixels within the bounding box (inclusive) that are neither white (0) nor azure (8).
6.  Create the output grid by copying the input grid.
7.  Perform a flood fill starting from the 'seed pixels'. The fill uses the 'fill_color', propagates only into white (0) pixels, and stays within the bounds of the bounding box.
8.  Pixels outside the bounding box, the azure (8) boundary pixels, and original non-white/non-azure pixels inside the box remain unchanged (except white pixels filled during the flood fill).
"""

def find_objects(grid, ignore_colors=None, connectivity=4):
    """
    Finds all contiguous objects of the same color in a grid.

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
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for r in range(rows):
        for c in range(cols):
            # If not visited and not an ignored color, start a search (BFS)
            if not visited[r, c] and grid[r, c] not in ignore_colors:
                color = grid[r, c]
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                # Use a separate set for current BFS to handle visited status correctly within the object search
                current_object_visited = set([(r, c)]) 

                while q:
                    curr_r, curr_c = q.popleft()
                    obj_coords.append((curr_r, curr_c))

                    # Check neighbors
                    for dr, dc in deltas:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds, color match, and if not visited in this specific BFS
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           (nr, nc) not in current_object_visited:
                            
                            visited[nr, nc] = True # Mark globally visited
                            current_object_visited.add((nr, nc)) # Mark visited for this object search
                            q.append((nr, nc))
                            
                if obj_coords: # Add the found object to the list
                     objects.append({
                         'color': color,
                         'coords': tuple(sorted(obj_coords)), # Use tuple for potential hashing/set operations later
                         'size': len(obj_coords)
                     })
    return objects


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the flood fill transformation based on the azure boundary and largest internal object.
    """
    # 1. Create a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Find azure (8) pixels
    azure_pixels = np.argwhere(input_grid == 8)

    # If no azure pixels, return the original grid copy
    if azure_pixels.size == 0:
        return output_grid

    # 3. Calculate the bounding box
    min_r = np.min(azure_pixels[:, 0])
    max_r = np.max(azure_pixels[:, 0])
    min_c = np.min(azure_pixels[:, 1])
    max_c = np.max(azure_pixels[:, 1])

    # 4. Find all non-white/non-azure objects
    all_objects = find_objects(input_grid, ignore_colors={0, 8})

    # 5. Filter for objects fully contained within the bounding box
    contained_objects = []
    for obj in all_objects:
        is_contained = True
        for r, c in obj['coords']:
            if not (min_r <= r <= max_r and min_c <= c <= max_c):
                is_contained = False
                break
        if is_contained:
            contained_objects.append(obj)

    # 6. Determine the fill color from the largest contained object
    if not contained_objects:
        # No object fully inside determines the color, so no fill happens
        return output_grid 
        
    # Sort by size (descending), then color (ascending) as a tie-breaker if needed
    contained_objects.sort(key=lambda x: (-x['size'], x['color']))
    fill_color = contained_objects[0]['color']

    # 7. Identify seed pixels (non-white/non-azure pixels within the box)
    seed_pixels = []
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if input_grid[r, c] != 0 and input_grid[r, c] != 8:
                seed_pixels.append((r, c))

    # 8. If no seed pixels, return the grid (no starting point for fill)
    if not seed_pixels:
        return output_grid

    # 9. Perform flood fill
    q = deque(seed_pixels)
    # visited_flood tracks pixels already processed *by the flood fill*
    # Initialize with seeds because we don't want to fill seed locations
    visited_flood = set(seed_pixels) 
    
    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)] # 4-connectivity for fill

    while q:
        r, c = q.popleft()

        # Check neighbors for potential filling
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc

            # Check conditions for filling the neighbor:
            # a) Within grid bounds
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            # b) Within the bounding box
            if not (min_r <= nr <= max_r and min_c <= nc <= max_c):
                continue
            # c) Original color was white (0) in the input grid
            if input_grid[nr, nc] != 0:
                continue
            # d) Not already visited/processed by this flood fill
            if (nr, nc) in visited_flood:
                continue

            # If all conditions met, fill the neighbor
            output_grid[nr, nc] = fill_color
            visited_flood.add((nr, nc))
            q.append((nr, nc))

    # 10. Return the modified grid
    return output_grid
```