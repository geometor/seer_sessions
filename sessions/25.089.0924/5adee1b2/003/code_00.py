"""
Transformation Rule:
1. Identify marker pairs in the first two columns (col 0, col 1) of the input grid. These pairs define a mapping from an object color (col 0) to a frame color (col 1). Store the coordinates of these marker pixels.
2. Find all distinct contiguous objects (4-way connectivity) in the grid composed of a single non-background color, excluding the pixels identified as markers.
3. For each identified object:
    a. Determine its color.
    b. Check if this color has a corresponding frame color defined by the markers.
    c. If a frame color exists:
        i. Calculate the bounding box of the object (min_row, min_col, max_row, max_col).
        ii. Define an expanded bounding box by extending the original box by one pixel in all directions (clamped to grid boundaries).
        iii. Iterate through all pixels within the expanded bounding box.
        iv. If a pixel is within the expanded box but outside the original object's bounding box, it belongs to the frame area.
        v. If a pixel belongs to the frame area and its current color in the output grid is the background color (0), update its color to the determined frame color.
4. The final output grid contains the original input elements plus the newly drawn frames, ensuring original elements and other frames are not overwritten.
"""

import numpy as np
from collections import deque

def find_objects(grid, marker_coords):
    """
    Finds all distinct contiguous objects (4-way connected) of the same color 
    in the grid, excluding coordinates specified in marker_coords.

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
            # Check if the pixel is non-background and not visited (and not a marker)
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

                        # Check bounds, color match, and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == object_color and \
                           (nr, nc) not in visited:
                            
                            visited.add((nr, nc))
                            current_object_coords.add((nr, nc))
                            q.append((nr, nc))
                
                # Store the found object if it has coordinates
                if current_object_coords: 
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
    # Scan columns 0 and 1 for vertical non-background pairs
    for r in range(height):
        # Check if cells in col 0 and col 1 are non-background
        if input_grid[r, 0] != 0 and input_grid[r, 1] != 0:
             # Assume these form a marker pair
             object_color = input_grid[r, 0]
             frame_color = input_grid[r, 1]
             # Add/update the mapping
             color_map[object_color] = frame_color
             # Record marker coordinates
             marker_coords.add((r, 0))
             marker_coords.add((r, 1))

    # --- Step 2: Find all distinct objects (excluding markers) ---
    objects = find_objects(input_grid, marker_coords)

    # --- Step 3 & 4: Process each object and draw frame if applicable ---
    for obj in objects:
        obj_color = obj['color']
        
        # Check if this object's color requires a frame according to the markers
        if obj_color in color_map:
            frame_color = color_map[obj_color]
            coords = obj['coords']
            
            # Calculate the original bounding box of the object
            min_r = min(r for r, c in coords)
            max_r = max(r for r, c in coords)
            min_c = min(c for r, c in coords)
            max_c = max(c for r, c in coords)
            
            # Define the expanded bounding box coordinates (1 pixel outwards)
            # Clamp coordinates to the grid boundaries
            frame_min_r = max(0, min_r - 1)
            frame_max_r = min(height - 1, max_r + 1)
            frame_min_c = max(0, min_c - 1)
            frame_max_c = min(width - 1, max_c + 1)

            # --- Step 4: Draw the frame ---
            # Iterate through all pixels within the expanded bounding box
            for r in range(frame_min_r, frame_max_r + 1):
                for c in range(frame_min_c, frame_max_c + 1):
                    # Check if the current pixel (r, c) is *outside* the original object's bounding box
                    is_outside_original_box = (r < min_r or r > max_r or 
                                               c < min_c or c > max_c)
                    
                    # If it's part of the frame area (outside original box) 
                    # AND the corresponding pixel in the output grid is currently background (0)
                    if is_outside_original_box and output_grid[r, c] == 0:
                        # Draw the frame pixel
                        output_grid[r, c] = frame_color
                            
    return output_grid