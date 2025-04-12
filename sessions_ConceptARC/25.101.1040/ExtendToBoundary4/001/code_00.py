"""
This module transforms an input grid based on the ARC task rules.
The transformation identifies a horizontal and a vertical line within the grid.
It finds the shortest path composed of white pixels (color 0) connecting these two lines.
These identified 'gap' pixels are then filled with a specific color determined by the orientation
of the gap path:
- If the gap path is vertical (all gap pixels share the same column), it's filled with the color
  of the vertical line.
- If the gap path is horizontal (all gap pixels share the same row), it's filled with the color
  of the horizontal line.
"""

import numpy as np
from collections import deque

def find_objects(grid_np: np.ndarray) -> list[dict]:
    """
    Finds connected components (objects) of the same non-background color (0)
    in the grid and identifies those that form straight horizontal or vertical lines.

    Args:
        grid_np: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a line object
        and contains its color, pixels, orientation ('horizontal' or 'vertical'),
        and bounding coordinates/indices. Returns an empty list if no lines are found.
    """
    rows, cols = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid_np[r, c]
            # If it's a non-background color (not 0) and not visited yet
            if color != 0 and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Perform Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    # Update bounding box
                    min_r, max_r = min(min_r, row), max(max_r, row)
                    min_c, max_c = min(min_c, col), max(max_c, col)

                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check grid boundaries and if neighbor is the same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid_np[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # After finding all pixels of the object, check if it forms a straight line
                is_line = False
                orientation = None
                if len(obj_pixels) > 0:
                     # Calculate object's width and height from bounding box
                     width = max_c - min_c + 1
                     height = max_r - min_r + 1
                     
                     # A vertical line has width 1 and height equal to the number of pixels
                     if width == 1 and height == len(obj_pixels):
                         orientation = 'vertical'
                         is_line = True
                     # A horizontal line has height 1 and width equal to the number of pixels
                     elif height == 1 and width == len(obj_pixels):
                         orientation = 'horizontal'
                         is_line = True
                
                # Store the object details if it's identified as a line
                if is_line:
                     objects.append({
                         'color': color,
                         'pixels': sorted(obj_pixels), # Sort pixels for consistent processing
                         'orientation': orientation,
                         'row': min_r if orientation == 'horizontal' else None, # Row index for H-line
                         'col': min_c if orientation == 'vertical' else None,   # Col index for V-line
                         'rows': (min_r, max_r) if orientation == 'vertical' else None, # Row span for V-line
                         'cols': (min_c, max_c) if orientation == 'horizontal' else None, # Col span for H-line
                     })
    return objects

def manhattan_distance(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points (row, col)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies a horizontal and a vertical line, finds the white pixel gap
    between their closest points, and fills the gap based on its orientation.

    Args:
        input_grid: A list of lists representing the input grid with integer colors.

    Returns:
        A list of lists representing the transformed output grid. Returns the
        original grid if the expected pattern (one horizontal, one vertical line)
        is not found or if no gap exists.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify; the original input remains unchanged
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # --- 1. Identify the horizontal and vertical lines ---
    # Find all line objects in the grid
    objects = find_objects(input_np)

    h_line = None
    v_line = None
    # Assign the found lines based on their orientation
    for obj in objects:
        if obj['orientation'] == 'horizontal':
            h_line = obj
        elif obj['orientation'] == 'vertical':
            v_line = obj
    
    # Check if exactly one horizontal and one vertical line were found
    # If not, the input doesn't match the expected pattern, return the original grid
    if h_line is None or v_line is None:
         return input_grid 

    # --- 2. Find the pair of closest pixels between the two lines ---
    min_dist = float('inf')
    h_closest = None # Pixel on the horizontal line closest to the vertical line
    v_closest = None # Pixel on the vertical line closest to the horizontal line

    # Compare every pixel in the horizontal line with every pixel in the vertical line
    for hp in h_line['pixels']:
        for vp in v_line['pixels']:
            # Calculate the Manhattan distance between the pair of pixels
            dist = manhattan_distance(hp, vp)
            # If this distance is smaller than the minimum found so far, update
            if dist < min_dist:
                min_dist = dist
                h_closest = hp
                v_closest = vp

    # If closest points couldn't be determined (e.g., if a line was empty, though find_objects should prevent this)
    if h_closest is None or v_closest is None:
        return input_grid 

    # --- 3. Determine the gap path, axis, and fill color ---
    gap_pixels = [] # List to store coordinates (row, col) of pixels in the gap
    fill_color = 0  # Color to fill the gap with (initialized to background)

    hr, hc = h_closest # Coordinates of the closest pixel on the H-line
    vr, vc = v_closest # Coordinates of the closest pixel on the V-line

    # Check if the closest points align vertically (share the same column index)
    if hc == vc:
        # This indicates a potential vertical gap along column 'hc'
        # Rule: Fill vertical gap with the vertical line's color
        fill_color = v_line['color']
        # Iterate through rows strictly between the closest points' rows
        # The range ensures we only consider pixels *between* the lines
        for r in range(min(hr, vr) + 1, max(hr, vr)):
            # Check if the coordinate is within the grid bounds
            if 0 <= r < rows and 0 <= hc < cols:
                 # If the pixel at (r, hc) is white (0), it's part of the gap
                 if input_np[r, hc] == 0:
                     gap_pixels.append((r, hc))
                 else:
                     # If any pixel on this path isn't white, it's not a valid gap
                     gap_pixels = [] # Discard potential gap pixels found so far
                     break # Stop checking this path
            else: # If coordinate is out of bounds, path is invalid
                 gap_pixels = []
                 break

    # Check if the closest points align horizontally (share the same row index)
    elif hr == vr:
        # This indicates a potential horizontal gap along row 'hr'
        # Rule: Fill horizontal gap with the horizontal line's color
        fill_color = h_line['color']
        # Iterate through columns strictly between the closest points' columns
        for c in range(min(hc, vc) + 1, max(hc, vc)):
             # Check if the coordinate is within the grid bounds
             if 0 <= hr < rows and 0 <= c < cols:
                  # If the pixel at (hr, c) is white (0), it's part of the gap
                  if input_np[hr, c] == 0:
                      gap_pixels.append((hr, c))
                  else:
                      # If any pixel on this path isn't white, it's not a valid gap
                      gap_pixels = [] # Discard potential gap pixels
                      break # Stop checking this path
             else: # If coordinate is out of bounds, path is invalid
                 gap_pixels = []
                 break
    
    # If the closest points are neither vertically nor horizontally aligned,
    # it implies a diagonal relationship or an unexpected configuration.
    # In such cases, gap_pixels remains empty, and no filling occurs.

    # --- 4. Fill the identified gap pixels in the output grid ---
    # Check if a valid gap was found (gap_pixels is not empty) and a fill color was determined
    if gap_pixels and fill_color != 0:
        # Iterate through the coordinates of the gap pixels
        for r_gap, c_gap in gap_pixels:
            # Update the corresponding pixel in the output grid with the fill color
            output_np[r_gap, c_gap] = fill_color

    # Convert the modified NumPy array back to a standard Python list of lists
    return output_np.tolist()