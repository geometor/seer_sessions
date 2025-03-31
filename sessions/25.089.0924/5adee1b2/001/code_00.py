import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify marker pairs in the first two columns (col 0, col 1) of the input grid. These pairs define a mapping from an object color (col 0) to a frame color (col 1).
2. Find all distinct contiguous objects in the grid that are not part of the markers identified in step 1. An object is defined as a connected group of pixels of the same non-background color.
3. For each identified object:
    a. Determine its color.
    b. Check if this color has a corresponding frame color defined by the markers.
    c. If a frame color exists:
        i. Calculate the bounding box of the object.
        ii. Draw a rectangular frame one pixel outside this bounding box using the corresponding frame color.
        iii. The frame should only be drawn onto background (white) pixels in the output grid, preserving the original objects, markers, and potentially overlapping frames.
4. The final output grid contains the original input elements plus the newly drawn frames.
"""

def find_objects(grid, marker_coords):
    """
    Finds all distinct contiguous objects of the same color in the grid,
    excluding coordinates specified in marker_coords.

    Args:
        grid (np.array): The input grid.
        marker_coords (set): A set of (row, col) tuples representing marker locations.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int) and 'coords' (set of (row, col) tuples).
    """
    height, width = grid.shape
    visited = set(marker_coords) # Start with markers as visited
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r, c] != 0 and (r, c) not in visited:
                object_color = grid[r, c]
                current_object_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                current_object_coords.add((r, c))

                while q:
                    row, col = q.popleft()

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and color match
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == object_color and \
                           (nr, nc) not in visited:
                            
                            visited.add((nr, nc))
                            current_object_coords.add((nr, nc))
                            q.append((nr, nc))
                
                if current_object_coords: # Ensure we found something
                     objects.append({'color': object_color, 'coords': current_object_coords})

    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    
    # --- Step 1: Identify Markers and Create Color Map ---
    color_map = {}
    marker_coords = set()
    for r in range(height):
        # Check if both column 0 and 1 have non-background colors
        # And they are vertically aligned markers (typical ARC pattern)
        # We assume markers are just pairs in the first two columns
        if input_grid[r, 0] != 0 and input_grid[r, 1] != 0:
             # Basic check: ensure they are different colors or handle specific logic if needed
             # For this task, they just form a pair.
             object_color = input_grid[r, 0]
             frame_color = input_grid[r, 1]
             color_map[object_color] = frame_color
             marker_coords.add((r, 0))
             marker_coords.add((r, 1))

    # --- Step 2: Find all distinct objects (excluding markers) ---
    objects = find_objects(input_grid, marker_coords)

    # --- Step 3 & 4: Process each object and draw frame if applicable ---
    for obj in objects:
        obj_color = obj['color']
        
        # Check if this object's color has a corresponding frame color
        if obj_color in color_map:
            frame_color = color_map[obj_color]
            coords = obj['coords']
            
            # Calculate bounding box
            min_r = min(r for r, c in coords)
            max_r = max(r for r, c in coords)
            min_c = min(c for r, c in coords)
            max_c = max(c for r, c in coords)
            
            # Define frame coordinates (one pixel outside bounding box)
            frame_min_r = max(0, min_r - 1)
            frame_max_r = min(height - 1, max_r + 1)
            frame_min_c = max(0, min_c - 1)
            frame_max_c = min(width - 1, max_c + 1)

            # Draw the frame onto the output grid
            for r in range(frame_min_r, frame_max_r + 1):
                for c in range(frame_min_c, frame_max_c + 1):
                    # Check if the current coordinate is on the perimeter of the frame box
                    is_perimeter = (r == frame_min_r or r == frame_max_r or 
                                    c == frame_min_c or c == frame_max_c)
                    
                    if is_perimeter:
                        # Only draw frame on background pixels of the output grid
                        if output_grid[r, c] == 0:
                            output_grid[r, c] = frame_color
                            
    return output_grid
