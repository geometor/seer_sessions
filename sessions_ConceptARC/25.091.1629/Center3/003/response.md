Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
from collections import deque, defaultdict, Counter
import statistics

"""
Transformation Rule:
1. Find all distinct, contiguous, non-background (non-zero color) objects in the input grid.
2. For each object found:
    a. Determine its color (C).
    b. Calculate its bounding box (B).
    c. Extract the subgrid (S) defined by the bounding box B from the input grid.
    d. Check if this subgrid S contains ONLY the object's color C and the background color 0.
    e. If the check in (d) passes, this object is considered a "candidate". Store its color (C), bounding box (B), bounding box area (A), and the extracted subgrid (S).
3. If no candidates are found, return a default small grid (e.g., [[0]]).
4. Determine the "border color" (BC): Find the color of the largest object (by pixel count) that touches any of the outer edges of the input grid.
5. Collect the areas (A) of all candidate objects. Find the median area (median_A) among these candidates. If there's an even number of candidates, use the lower of the two middle area values after sorting.
6. Filter the candidates, keeping only those whose area A equals the median_A.
7. If only one candidate remains after filtering by median area, select its subgrid (S) as the output.
8. If multiple candidates remain (tied by having the median area):
    a. Check if any of the tied candidates' colors (C) match the border color (BC).
    b. If exactly one tied candidate's color matches BC, select its subgrid (S) as the output.
    c. If zero or more than one tied candidate's color matches BC, find the median color among these tied candidates. Sort their colors (C) numerically. If there's an odd number, the median is the middle value. If there's an even number, the median color is the lower of the two middle values. Select the subgrid (S) belonging to the candidate with this median color.
9. Return the selected subgrid S.
"""

def find_objects(grid, colors_to_find=None, connectivity=4):
    """
    Finds all connected components (objects) of specified colors in the grid.

    Args:
        grid (np.array): The input grid.
        colors_to_find (set, optional): A set of color values to search for.
                                         If None, searches for all non-background (0) colors.
        connectivity (int): 4 for cardinal directions, 8 for cardinal and diagonal.

    Returns:
        dict: A dictionary where keys are colors and values are lists of objects.
              Each object is represented as a set of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = defaultdict(list)

    if colors_to_find is None:
        # Find all unique non-zero colors present in the grid
        unique_colors = np.unique(grid)
        colors_to_find = set(unique_colors[unique_colors != 0])


    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color in colors_to_find and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Define neighbors based on connectivity
                    if connectivity == 4:
                        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
                    else: # connectivity == 8
                         neighbors = [
                            (row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1),
                            (row - 1, col - 1), (row - 1, col + 1), (row + 1, col - 1), (row + 1, col + 1)
                         ]

                    for nr, nc in neighbors:
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            obj_coords.add((nr, nc))

                if obj_coords:
                    objects[color].append(obj_coords)
    return objects

def get_bounding_box(obj_coords):
    """Calculates the bounding box of an object."""
    if not obj_coords:
        return None
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return (min_r, min_c, max_r, max_c)

def get_border_color(grid):
    """Finds the color of the largest object (by pixel count) touching the grid borders."""
    rows, cols = grid.shape

    # Find all non-background objects first
    all_objects = find_objects(grid)
    largest_border_object_size = -1
    determined_border_color = 0 # Default to background

    for color, objects_list in all_objects.items():
        for obj_coords in objects_list:
            touches_border = False
            for r, c in obj_coords:
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    touches_border = True
                    break
            if touches_border:
                obj_size = len(obj_coords)
                if obj_size > largest_border_object_size:
                    largest_border_object_size = obj_size
                    determined_border_color = color
                # Tie-breaking for largest border object size isn't specified,
                # assume the first one found with max size determines the color,
                # or that there won't be ties in the relevant cases.

    return determined_border_color

def get_median_low(data):
    """Calculates the median, choosing the lower value for even counts."""
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n == 0:
        return None # Or raise error
    if n % 2 == 1:
        return sorted_data[n // 2]
    else:
        # Lower median for even count
        return sorted_data[n // 2 - 1]

def transform(input_grid):
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Find all non-background objects
    all_objects = find_objects(grid)

    candidates = []
    # 2-4. Identify Candidate Objects/Subgrids
    for color, objects_list in all_objects.items():
        for obj_coords in objects_list:
            bbox = get_bounding_box(obj_coords)
            if bbox:
                min_r, min_c, max_r, max_c = bbox
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                bbox_area = height * width

                # Extract subgrid
                subgrid = grid[min_r : max_r + 1, min_c : max_c + 1]

                # Check if subgrid contains only object color and background (0)
                unique_colors_in_subgrid = np.unique(subgrid)
                allowed_colors = {color, 0}
                is_candidate = True
                for c_sub in unique_colors_in_subgrid:
                    if c_sub not in allowed_colors:
                        is_candidate = False
                        break

                if is_candidate:
                    candidates.append({
                        'color': color,
                        'bbox': bbox,
                        'area': bbox_area,
                        'subgrid': subgrid
                    })

    # 3. Handle no candidates
    if not candidates:
        return [[0]] # Default output

    # 4. Determine Border Color
    border_color = get_border_color(grid)

    # 5. Find Median Area
    candidate_areas = [cand['area'] for cand in candidates]
    median_area = get_median_low(candidate_areas)

    # 6. Filter by Median Area
    median_area_candidates = [cand for cand in candidates if cand['area'] == median_area]

    selected_candidate = None
    # 7. Select if only one candidate has median area
    if len(median_area_candidates) == 1:
        selected_candidate = median_area_candidates[0]
    # 8. Handle ties in median area
---
