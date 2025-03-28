import numpy as np
from collections import deque

"""
Transforms the input grid by resizing a green frame based on the location of external magenta markers, while preserving the original content within the frame's initial area.

1.  Initialize an output grid of the same dimensions as the input grid, filled with white (0).
2.  Find all coordinates of magenta (6) pixels (markers) and store them.
3.  Find all connected components of green (3) pixels. 
4.  If no green components exist, skip to step 9 (drawing markers).
5.  If green components exist, identify the "main" component (largest bounding box area, tie-breaking with top-left corner) and calculate its initial bounding box (`initial_bbox`).
6.  Copy the rectangular region defined by `initial_bbox` from the input grid to the corresponding region in the output grid.
7.  Identify magenta markers that lie strictly outside `initial_bbox`.
8.  Calculate the new bounding box (`new_bbox`) by potentially expanding `initial_bbox` based on external markers:
    a.  Expand top edge up to one row below the lowest external marker above the box.
    b.  Expand bottom edge down to one row above the highest external marker below the box.
    c.  Expand left edge leftwards to one column right of the rightmost external marker left of the box.
    d.  Expand right edge rightwards to one column left of the leftmost external marker right of the box.
    e.  If no external markers exist in a direction, the corresponding edge of `new_bbox` matches `initial_bbox`.
    f.  Clamp `new_bbox` coordinates to grid boundaries.
    g.  Draw the hollow perimeter of `new_bbox` onto the output grid using green (3), overwriting any previously copied content.
9.  Draw all original magenta markers (found in step 2) onto the output grid at their original coordinates, overwriting any existing pixels.
10. Return the final output grid.
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
    # Ensure non-negative dimensions before calculating area
    height = max(0, max_r - min_r + 1)
    width = max(0, max_c - min_c + 1)
    return height * width
    
def transform(input_grid):
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # 1. Initialize output grid with white (0)
    output_grid = np.zeros_like(input_np) 

    # 2. Find Magenta Markers
    magenta_markers = []
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] == 6:
                magenta_markers.append((r, c))

    # 3. Find Green Objects
    green_objects = find_objects(input_np, 3)
    
    main_green_object = None
    initial_bbox = None

    # 4. Check if green components exist
    if green_objects:
        # 5. Identify Main Green Object and its initial bounding box
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
                initial_bbox = bbox
                best_bbox_top_left = (min_r, min_c)
            elif area == max_area:
                # Tie-breaking: choose the one with the top-most, then left-most corner
                if (min_r, min_c) < best_bbox_top_left:
                    main_green_object = obj_coords
                    initial_bbox = bbox
                    best_bbox_top_left = (min_r, min_c)

    # --- Process if a main green object was found ---
    if initial_bbox:
        initial_min_r, initial_min_c, initial_max_r, initial_max_c = initial_bbox

        # 6. Copy the content within the initial bounding box
        output_grid[initial_min_r:initial_max_r+1, initial_min_c:initial_max_c+1] = \
            input_np[initial_min_r:initial_max_r+1, initial_min_c:initial_max_c+1]

        # 7. Identify external markers
        external_markers = [
            (m_r, m_c) for m_r, m_c in magenta_markers 
            if not (initial_min_r <= m_r <= initial_max_r and initial_min_c <= m_c <= initial_max_c)
        ]

        # 8. Calculate the new bounding box based on external markers
        target_min_r = initial_min_r
        target_max_r = initial_max_r
        target_min_c = initial_min_c
        target_max_c = initial_max_c

        markers_above = [m_r for m_r, m_c in external_markers if m_r < initial_min_r]
        markers_below = [m_r for m_r, m_c in external_markers if m_r > initial_max_r]
        markers_left  = [m_c for m_r, m_c in external_markers if m_c < initial_min_c]
        markers_right = [m_c for m_r, m_c in external_markers if m_c > initial_max_c]

        if markers_above:
            # Target top row stops one step *before* the lowest marker above
            target_min_r = min(markers_above) + 1 
        if markers_below:
            # Target bottom row stops one step *before* the highest marker below
            target_max_r = max(markers_below) - 1
        if markers_left:
            # Target left col stops one step *after* the rightmost marker to the left
            target_min_c = max(markers_left) + 1 
        if markers_right:
            # Target right col stops one step *before* the leftmost marker to the right
            target_max_c = min(markers_right) - 1

        # Determine final new bounding box: union of initial and target areas
        new_min_r = min(initial_min_r, target_min_r)
        new_max_r = max(initial_max_r, target_max_r)
        new_min_c = min(initial_min_c, target_min_c)
        new_max_c = max(initial_max_c, target_max_c)
        
        # Clamp bounds to grid dimensions
        new_min_r = max(0, new_min_r)
        new_max_r = min(rows - 1, new_max_r)
        new_min_c = max(0, new_min_c)
        new_max_c = min(cols - 1, new_max_c)

        # Draw the hollow green rectangle perimeter of the new bounding box
        if new_min_r <= new_max_r and new_min_c <= new_max_c: # Check validity
            # Draw top border
            if new_min_r < rows:
                output_grid[new_min_r, new_min_c:new_max_c+1] = 3
            # Draw bottom border
            if new_max_r >= 0:
                output_grid[new_max_r, new_min_c:new_max_c+1] = 3
            # Draw left border (excluding corners)
            if new_min_c < cols and new_max_r > new_min_r: 
                 output_grid[new_min_r+1:new_max_r, new_min_c] = 3
            # Draw right border (excluding corners)
            if new_max_c >= 0 and new_max_r > new_min_r: 
                 output_grid[new_min_r+1:new_max_r, new_max_c] = 3
            
    # 9. Draw ALL Magenta Markers (overwriting anything underneath)
    # This happens regardless of whether a green frame was found/processed
    for r, c in magenta_markers:
        # Ensure marker is within bounds before drawing
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = 6

    # 10. Convert back to list of lists for the expected output format
    return output_grid.tolist()