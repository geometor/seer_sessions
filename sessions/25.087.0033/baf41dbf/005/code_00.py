import numpy as np
from collections import deque

"""
Transforms the input grid by finding the main green (3) frame object, resizing it based on the positions of external magenta (6) markers, and drawing the resized frame on a new grid along with the original markers.

1. Identifies all magenta markers and stores their coordinates.
2. Identifies all connected green objects (potential frames).
3. If green objects exist, determines the "main" green object based on the largest bounding box area. Ties are broken by the top-left corner position (min_row, then min_col).
4. Calculates the initial bounding box of this main green object.
5. Finds magenta markers located strictly outside the main object's initial bounding box.
6. Calculates a target bounding box based on these external markers:
    - Top boundary extends towards the lowest marker above, stopping one step before it.
    - Bottom boundary extends towards the highest marker below, stopping one step before it.
    - Left boundary extends towards the rightmost marker to the left, stopping one step before it.
    - Right boundary extends towards the leftmost marker to the right, stopping one step before it.
7. Determines the final new bounding box as the union of the initial box and the target expansion area. Coordinates are clamped to grid bounds.
8. Creates an output grid initialized to white (0).
9. Draws a hollow green rectangle representing the perimeter of the new bounding box on the output grid.
10. Redraws all original magenta markers at their initial positions on the output grid.
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
              cardinally (up, down, left, right). Returns an empty list if no
              objects of the specified color are found.
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

def get_bbox_area(bbox):
    """Calculates the area of a bounding box."""
    if not bbox:
        return 0
    min_r, min_c, max_r, max_c = bbox
    return (max_r - min_r + 1) * (max_c - min_c + 1)

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

    # --- Step 2: Find Green Objects ---
    green_objects = find_objects(input_np, 3)
    
    main_green_object = None
    if green_objects:
        # --- Step 3: Identify Main Green Object ---
        max_area = -1
        best_bbox_top_left = (rows, cols) # Initialize with max possible values

        for obj_coords in green_objects:
            bbox = get_bounding_box(obj_coords)
            if not bbox: continue
            
            area = get_bbox_area(bbox)
            min_r, min_c, _, _ = bbox
            
            if area > max_area:
                max_area = area
                main_green_object = obj_coords
                best_bbox_top_left = (min_r, min_c)
            elif area == max_area:
                # Tie-breaking: choose the one with the top-most, then left-most corner
                if (min_r, min_c) < best_bbox_top_left:
                    main_green_object = obj_coords
                    best_bbox_top_left = (min_r, min_c)

    # --- Process the main frame if found ---
    if main_green_object:
        # --- Step 4: Calculate initial bounding box ---
        initial_bbox = get_bounding_box(main_green_object)
        if not initial_bbox: # Should not happen if main_green_object is valid
             # Draw only markers if frame finding failed unexpectedly
             for r, c in magenta_markers:
                 if 0 <= r < rows and 0 <= c < cols:
                     output_grid[r, c] = 6
             return output_grid.tolist()

        initial_min_r, initial_min_c, initial_max_r, initial_max_c = initial_bbox

        # --- Step 5: Find external markers ---
        external_markers = [
            (m_r, m_c) for m_r, m_c in magenta_markers 
            if not (initial_min_r <= m_r <= initial_max_r and initial_min_c <= m_c <= initial_max_c)
        ]

        # --- Step 6: Calculate target boundaries based on external markers ---
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
            # Rightmost marker left defines target left col (+1) - use max coord
            target_min_c = max(markers_left) + 1 
        if markers_right:
            # Leftmost marker right defines target right col (-1) - use min coord
            target_max_c = min(markers_right) - 1

        # --- Step 7: Determine final new bounding box ---
        # Union of initial box and target expansion area
        new_min_r = min(initial_min_r, target_min_r)
        new_max_r = max(initial_max_r, target_max_r)
        new_min_c = min(initial_min_c, target_min_c)
        new_max_c = max(initial_max_c, target_max_c)
        
        # --- Step 8: Clamp bounds to grid dimensions ---
        new_min_r = max(0, new_min_r)
        new_max_r = min(rows - 1, new_max_r)
        new_min_c = max(0, new_min_c)
        new_max_c = min(cols - 1, new_max_c)

        # --- Step 9 & 10: Draw hollow green rectangle ---
        # Check if the calculated box has valid dimensions before drawing
        if new_min_r <= new_max_r and new_min_c <= new_max_c:
            # Draw top border
            output_grid[new_min_r, new_min_c:new_max_c+1] = 3
            # Draw bottom border
            output_grid[new_max_r, new_min_c:new_max_c+1] = 3
            # Draw left border (excluding corners already drawn)
            if new_max_r > new_min_r: # Avoid index error for single row boxes
                 output_grid[new_min_r+1:new_max_r, new_min_c] = 3
            # Draw right border (excluding corners already drawn)
            if new_max_r > new_min_r and new_max_c > new_min_c: # Avoid index error and overdraw for single row/col boxes
                 output_grid[new_min_r+1:new_max_r, new_max_c] = 3
            
    # --- Step 11: Redraw Magenta Markers ---
    # This happens regardless of whether a green frame was found/processed
    for r, c in magenta_markers:
        # Ensure marker is within bounds before drawing (should always be)
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = 6

    # Convert back to list of lists for the expected output format
    return output_grid.tolist()