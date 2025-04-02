```python
import numpy as np
from collections import Counter, deque

"""
Identifies all distinct connected objects (shapes) of non-white pixels in the input grid using 8-way connectivity (including diagonals).
Determines the orientation (Horizontal, Vertical, or Diagonal) for each shape with 2 or more pixels.
Counts the number of shapes for each orientation.
Identifies the majority orientation (the one with the highest count). Assumes a unique majority based on examples. If there is a tie for the majority, all shapes are kept.
Creates the output grid by removing shapes (setting their pixels to white/0) whose orientation does not match the majority orientation. Shapes with no determined orientation (e.g., single pixels) and shapes matching the majority orientation are kept.
"""

def find_objects(grid):
    """
    Finds all connected objects of the same color in the grid using BFS.
    Uses 8-way connectivity (includes diagonals).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'coords' (list of (r, c) tuples) and 'color' (int).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    coords.append((row, col))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            
                            if 0 <= nr < height and 0 <= nc < width and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                if coords: 
                    objects.append({'coords': coords, 'color': color})
    return objects

def get_orientation(coords):
    """
    Determines the orientation of an object based on its pixel coordinates.

    Args:
        coords (list): A list of (row, col) tuples representing the object's pixels.

    Returns:
        str or None: "Horizontal", "Vertical", "Diagonal", or None if orientation
                     cannot be determined (e.g., single pixel).
    """
    if len(coords) < 2:
        return None  # Cannot determine orientation for single pixel or empty list

    rows = {r for r, c in coords}
    cols = {c for r, c in coords}

    is_horizontal = len(rows) == 1
    is_vertical = len(cols) == 1

    if is_horizontal:
        return "Horizontal"
    elif is_vertical:
        return "Vertical"
    else:
        # Any other multi-pixel shape is considered Diagonal for this task
        return "Diagonal"

def transform(input_grid):
    """
    Transforms the input grid by keeping only the shapes that belong to the
    majority orientation category (Horizontal, Vertical, or Diagonal).

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)

    # 1. Find all distinct objects
    objects = find_objects(grid)

    # 2. Determine orientation for each object and store details
    object_details = []
    orientations = []
    for obj in objects:
        coords = obj['coords']
        orientation = get_orientation(coords)
        object_details.append({'coords': coords, 'orientation': orientation})
        if orientation:  # Only consider valid orientations (H, V, D) for counting
            orientations.append(orientation)

    # 3. Count orientations
    orientation_counts = Counter(orientations)

    # 4. Find the majority orientation
    majority_orientation = None
    max_count = 0
    if orientation_counts:
        max_count = max(orientation_counts.values())
        majority_orientations = [o for o, c in orientation_counts.items() if c == max_count]
        
        # Assume unique majority based on examples. If tied, keep all shapes.
        if len(majority_orientations) == 1:
            majority_orientation = majority_orientations[0]
            # print(f"Majority Orientation: {majority_orientation} (Count: {max_count})") # Debug
        # else: print("Tie or no valid orientations found. Keeping all shapes.") # Debug

    # 5. & 6. Create output grid by filtering shapes
    # Iterate through objects and remove those not matching the majority orientation
    for obj_detail in object_details:
        coords = obj_detail['coords']
        orientation = obj_detail['orientation']

        # Condition to remove: A unique majority exists, AND the object has a valid 
        # orientation, AND that orientation does not match the majority.
        if majority_orientation is not None and \
           orientation is not None and \
           orientation != majority_orientation:
            # 8. Change pixels of non-majority objects to background color
            for r, c in coords:
                output_grid[r, c] = 0

    # 9. Return the final grid
    return output_grid.tolist()
```