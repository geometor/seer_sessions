```python
import numpy as np
import math
from collections import deque

"""
Transforms an input grid based on blue/green shapes and a yellow marker.

1. Initialize the output grid with the same dimensions as the input, filled with azure (8).
2. Identify all distinct contiguous shapes composed of blue (1) or green (3) pixels using 8-way connectivity. Store the set of pixel coordinates for each shape. Let N be the number of shapes found.
3. Locate the single yellow (4) marker pixel at position (mr, mc).
4. Apply rules based on the number of shapes (N):
    * If N > 1:
        * Fill the exact pixel locations of every blue/green shape with red (2).
        * Fill the entire column mc (the marker's column) with red (2), overwriting previous fills.
    * If N == 1:
        * Let the single shape be S.
        * Calculate the minimum Manhattan distance (min_dist) from the marker's position (mr, mc) to any pixel belonging to shape S.
        * If min_dist <= 2:
            * Calculate the centroid (average row, average column) of the pixels in S. Determine the centroid's column index cc (floor of the average column value).
            * Fill the exact pixel locations of shape S with red (2).
            * Fill the entire column cc (the centroid's column index) with red (2), overwriting previous fills.
        * If min_dist > 2:
            * Fill the entire column mc (the marker's column index) with red (2).
    * If N == 0:
        * (Assumption based on examples and lack of N=0 case) Fill the marker's column mc with red (2). If no marker, return the background grid.
5. Return the final output grid.
"""

def find_shapes(input_grid_np, shape_colors):
    """
    Identifies contiguous shapes of specified colors using 8-way connectivity
    and returns their pixel coordinates.

    Args:
        input_grid_np (np.array): The input grid.
        shape_colors (list): List of colors that constitute shapes.

    Returns:
        tuple: (list_of_shapes, num_shapes)
            list_of_shapes: A list where each element is a dict:
                            {'pixels': set((r, c), ...)}
            num_shapes: The total number of distinct shapes found.
    """
    rows, cols = input_grid_np.shape
    shape_mask = np.isin(input_grid_np, shape_colors)
    visited = np.zeros_like(shape_mask, dtype=bool)
    current_label = 0
    shapes = []

    for r in range(rows):
        for c in range(cols):
            if shape_mask[r, c] and not visited[r, c]:
                current_label += 1
                component_pixels = set()
                q = deque([(r, c)]) # Use deque for efficient BFS
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    component_pixels.add((row, col))

                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               shape_mask[nr, nc] and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                shapes.append({'pixels': component_pixels})

    return shapes, current_label

def calculate_min_manhattan_dist_to_pixels(marker_pos, shapes):
    """
    Calculates the minimum Manhattan distance from the marker position
    to any pixel belonging to any of the shapes.

    Args:
        marker_pos (tuple): (row, col) of the marker.
        shapes (list): List of shape dictionaries, each with a 'pixels' set.

    Returns:
        float: Minimum Manhattan distance, or infinity if no shapes/pixels.
    """
    if not shapes:
        return float('inf')

    mr, mc = marker_pos
    min_dist = float('inf')

    for shape in shapes:
        if not shape['pixels']:
            continue
        for r, c in shape['pixels']:
            dist = abs(mr - r) + abs(mc - c)
            min_dist = min(min_dist, dist)

    return min_dist

def calculate_centroid_column(pixels):
    """
    Calculates the floor of the average column index for a set of pixels.

    Args:
        pixels (set): Set of (row, col) tuples.

    Returns:
        int: The floor of the average column index, or -1 if no pixels.
    """
    if not pixels:
        return -1
    
    # Ensure float division
    avg_c = sum(c for r, c in pixels) / float(len(pixels)) 
    return math.floor(avg_c)

def transform(input_grid):
    """
    Applies the transformation rule based on shapes, marker, and distance.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    background_color = 8 # azure
    fill_color = 2 # red
    shape_colors = [1, 3] # blue, green
    marker_color = 4 # yellow

    # 1. Initialize output_grid with background color
    output_grid = np.full_like(input_grid_np, background_color)

    # 2. Identify shapes and their properties
    shapes, num_shapes = find_shapes(input_grid_np, shape_colors)

    # 3. Locate the marker
    marker_coords = np.argwhere(input_grid_np == marker_color)
    
    # Handle case where marker might be missing (though unlikely based on examples)
    if marker_coords.size == 0:
        # If no marker, return background grid as per implicit rules
        return output_grid.tolist() 

    marker_pos = tuple(marker_coords[0]) # (mr, mc)
    mr, mc = marker_pos

    # 4/5. Apply rules based on number of shapes (N)
    if num_shapes == 0:
        # Fill marker column if no shapes exist
        output_grid[:, mc] = fill_color

    elif num_shapes == 1:
        # Case: N == 1
        single_shape = shapes[0]
        min_dist = calculate_min_manhattan_dist_to_pixels(marker_pos, shapes)
        
        if min_dist <= 2:
            # Marker "close": Fill shape pixels + centroid column
            cc = calculate_centroid_column(single_shape['pixels'])
            if cc != -1: # Ensure centroid column is valid
                # Fill shape pixels
                for r, c in single_shape['pixels']:
                    output_grid[r, c] = fill_color
                # Fill centroid column (overwriting shape pixels in that column)
                output_grid[:, cc] = fill_color 
            else:
                 # Should not happen if num_shapes == 1 and pixels exist
                 print("Warning: Could not calculate centroid column for single shape.")
                 # Fallback? Maybe fill marker column? Let's fill marker column as a guess.
                 output_grid[:, mc] = fill_color 
        
        else: # min_dist > 2
            # Marker "distant": Fill only marker column
            output_grid[:, mc] = fill_color

    else: # num_shapes > 1
        # Case: N > 1: Fill all shape pixels + marker column
        for shape in shapes:
            for r, c in shape['pixels']:
                output_grid[r, c] = fill_color
        # Fill marker column (overwriting shape pixels in that column)
        output_grid[:, mc] = fill_color 
        
    # 6. Return the modified output grid
    return output_grid.tolist()
```