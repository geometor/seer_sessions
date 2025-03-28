```python
import numpy as np
from collections import deque

"""
Transforms the input grid by resizing green (3) frame objects based on the positions of magenta (6) markers.

1. Identifies all magenta markers and stores their coordinates.
2. Identifies all connected green objects (frames).
3. For each green frame:
    a. Calculates its initial bounding box.
    b. Finds magenta markers located strictly outside this initial box.
    c. Calculates a target bounding box based on these external markers, expanding outwards but stopping one step short of the marker's row/column.
    d. Determines the final new bounding box as the union of the initial box and the target expansion area.
    e. Draws a hollow green rectangle representing the perimeter of this new bounding box on an initially white output grid.
4. After drawing all resized frames, redraws all original magenta markers at their initial positions on the output grid.
"""

def find_objects(grid, color):
    """
    Finds all connected components of a given color in the grid using Breadth-First Search.

    Args:
        grid (np.array): The input grid.
        color (int): The color value to search for.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of pixels belonging to a connected object. Objects are connected
              cardinally (up, down, left, right).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                
                if obj_coords: # ensure we found something
                    objects.append(obj_coords)
    return objects

def get_bounding_box(obj_coords):
    """
    Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) inclusive.
               Returns None if obj_coords is empty.
    """
    if not obj_coords:
        return None
    
    min_row = min(r for r, c in obj_coords)
    min_col = min(c for r, c in obj_coords)
    max_row = max(r for r, c in obj_coords)
    max_col = max(c for r, c in obj_coords)
    
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    # Initialize output grid with white (0)
    output_grid = np.zeros_like(input_np) 

    # --- Step 1: Find Magenta Markers ---
    magenta_markers = []
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] == 6:
                magenta_markers.append((r, c))

    # --- Step 2: Find Green Objects (Frames) ---
    green_objects = find_objects(input_np, 3)
    
    # --- Step 3 & 4: Process each frame, calculate new bbox, draw frame ---
    for obj_coords in green_objects:
        # --- Step 3a: Calculate initial bounding box ---
        initial_bbox = get_bounding_box(obj_coords)
        if not initial_bbox:
            continue # Should not happen if find_objects returns non-empty sets
        
        initial_min_r, initial_min_c, initial_max_r, initial_max_c = initial_bbox

        # --- Step 3b: Find external markers ---
        external_markers = [
            (m_r, m_c) for m_r, m_c in magenta_markers 
            if not (initial_min_r <= m_r <= initial_max_r and initial_min_c <= m_c <= initial_max_c)
        ]

        # --- Step 3c: Calculate target boundaries based on external markers ---
        target_min_r = rows # Default: grid height (no markers above)
        target_max_r = -1   # Default: -1 (no markers below)
        target_min_c = cols # Default: grid width (no markers left)
        target_max_c = -1   # Default: -1 (no markers right)

        markers_above = [m_r for m_r, m_c in external_markers if m_r < initial_min_r]
        markers_below = [m_r for m_r, m_c in external_markers if m_r > initial_max_r]
        markers_left  = [m_c for m_r, m_c in external_markers if m_c < initial_min_c]
        markers_right = [m_c for m_r, m_c in external_markers if m_c > initial_max_c]

        if markers_above:
            # Lowest marker above defines target top row (+1 because boundary stops before marker)
            target_min_r = min(markers_above) + 1 
        if markers_below:
            # Highest marker below defines target bottom row (-1 because boundary stops before marker)
            target_max_r = max(markers_below) - 1
        if markers_left:
            # Rightmost marker left defines target left col (+1)
            target_min_c = min(markers_left) + 1 # Bugfix: Should be max(markers_left) + 1? No, min coordinate + 1. Example 1/3 analysis confirms min(coord) + 1. Example 1: marker (3,1), initial min_c 4 -> new_min_c min(4, 1+1)=2. Example 3: marker (6,1), initial min_c 4 -> new_min_c min(4, 1+1)=2.
        if markers_right:
            # Leftmost marker right defines target right col (-1)
            target_max_c = max(markers_right) - 1 # Bugfix: Should be min(markers_right) - 1? No, max coordinate - 1. Example 2 analysis confirms max(coord) - 1. Example 2: marker (2,11), initial max_c 6 -> new_max_c max(6, 11-1)=10. Example 3: marker (4,12), initial max_c 9 -> new_max_c max(9, 12-1)=11.

        # --- Step 3d: Determine final new bounding box ---
        # Union of initial box and target expansion area
        new_min_r = min(initial_min_r, target_min_r)
        new_max_r = max(initial_max_r, target_max_r)
        new_min_c = min(initial_min_c, target_min_c)
        new_max_c = max(initial_max_c, target_max_c)
        
        # Ensure calculated bounds are valid within the grid - clamp if necessary.
        # The logic should inherently keep them mostly valid, but clamping adds robustness.
        new_min_r = max(0, new_min_r)
        new_max_r = min(rows - 1, new_max_r)
        new_min_c = max(0, new_min_c)
        new_max_c = min(cols - 1, new_max_c)

        # --- Step 4e: Draw hollow green rectangle ---
        # Check if the calculated box has valid dimensions before drawing
        if new_min_r <= new_max_r and new_min_c <= new_max_c:
            # Draw top border
            output_grid[new_min_r, new_min_c:new_max_c+1] = 3
            # Draw bottom border
            output_grid[new_max_r, new_min_c:new_max_c+1] = 3
            # Draw left border
            output_grid[new_min_r:new_max_r+1, new_min_c] = 3
            # Draw right border
            output_grid[new_min_r:new_max_r+1, new_max_c] = 3
            
    # --- Step 5: Redraw Magenta Markers ---
    for r, c in magenta_markers:
        # Ensure marker is within bounds before drawing (should always be)
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = 6

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()
```