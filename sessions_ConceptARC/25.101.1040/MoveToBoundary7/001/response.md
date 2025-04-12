```python
"""
Identifies the two distinct colored objects in the input grid against a white background.
Determines the smaller object (based on bounding box area) as the "mover" and the larger as "stationary".
Calculates the translation needed to move the "mover" object directly towards the "stationary" object until they are adjacent (1 pixel apart) along the primary axis of separation (horizontal or vertical).
Applies this translation to the mover object, erasing it from its original position and drawing it in the new position, leaving the stationary object and background unchanged.
"""

import numpy as np
from collections import deque

def find_objects(grid: np.ndarray, background_color: int = 0) -> list[dict]:
    """
    Finds connected components (objects) of non-background colors in the grid.

    Args:
        grid: The input grid as a numpy array.
        background_color: The integer value representing the background.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'color', 'coords' (set of (r, c) tuples), and 'bbox'
        (min_r, min_c, max_r, max_c). Returns empty list if no objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (including diagonals for connectivity)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))

                objects.append({
                    'color': color,
                    'coords': coords,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def get_bounding_box(coords: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a set of coordinates."""
    if not coords:
        return (0, 0, 0, 0)
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def calculate_area(bbox: tuple[int, int, int, int]) -> int:
    """Calculates the area of a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    return (max_r - min_r + 1) * (max_c - min_c + 1)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Moves the smaller of two objects adjacent to the larger object.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    background_color = 0 # Assuming white is background

    # 1. Identify the two distinct colored objects
    objects = find_objects(input_np, background_color)

    # Ensure exactly two objects are found
    if len(objects) != 2:
        # If not exactly two objects, return the original grid
        return input_grid

    # 2. Determine bounding boxes and areas
    obj1 = objects[0]
    obj2 = objects[1]
    obj1['area'] = calculate_area(obj1['bbox'])
    obj2['area'] = calculate_area(obj2['bbox'])

    # 3. Designate mover (smaller) and stationary (larger)
    if obj1['area'] <= obj2['area']: # Treat equal area case arbitrarily or check pixel count? Sticking to area for now.
        mover = obj1
        stationary = obj2
    else:
        mover = obj2
        stationary = obj1

    # Extract bounding box coordinates for easier access
    m_min_r, m_min_c, m_max_r, m_max_c = mover['bbox']
    s_min_r, s_min_c, s_max_r, s_max_c = stationary['bbox']

    # 4. Determine the primary axis of separation and direction
    # Calculate center points (approximate)
    mover_center_r = (m_min_r + m_max_r) / 2
    mover_center_c = (m_min_c + m_max_c) / 2
    stat_center_r = (s_min_r + s_max_r) / 2
    stat_center_c = (s_min_c + s_max_c) / 2

    delta_r = stat_center_r - mover_center_r
    delta_c = stat_center_c - mover_center_c

    move_horizontally = abs(delta_c) >= abs(delta_r) # Move along the axis with greater separation

    # 5. Calculate the target position and translation delta (dx, dy)
    dx = 0
    dy = 0

    if move_horizontally:
        # Move left or right
        if delta_c > 0: # Mover is to the left of stationary, move right
            target_min_c = s_min_c - 1 - (m_max_c - m_min_c)
            dx = target_min_c - m_min_c
        else: # Mover is to the right of stationary, move left
            target_min_c = s_max_c + 1
            dx = target_min_c - m_min_c
    else:
        # Move up or down
        if delta_r > 0: # Mover is above stationary, move down
            target_min_r = s_min_r - 1 - (m_max_r - m_min_r)
            dy = target_min_r - m_min_r
        else: # Mover is below stationary, move up
            target_min_r = s_max_r + 1
            dy = target_min_r - m_min_r

    # 6. Create the output grid: erase old, draw new
    # Erase mover from original position
    mover_color = mover['color']
    for r, c in mover['coords']:
        output_grid[r, c] = background_color

    # Draw mover at the new position
    for r, c in mover['coords']:
        new_r, new_c = r + dy, c + dx
        # Check bounds just in case, although logic should keep it within grid
        if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
            output_grid[new_r, new_c] = mover_color
        else:
             # This case indicates an issue with calculation or assumptions
             print(f"Warning: Calculated new position ({new_r}, {new_c}) is out of bounds.")


    # Convert back to list of lists for the final output
    return output_grid.tolist()
```