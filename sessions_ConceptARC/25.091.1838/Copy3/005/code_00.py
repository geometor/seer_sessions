import numpy as np
from scipy.spatial.distance import euclidean
from collections import deque

"""
Transforms an input grid based on its width:

1. If the grid width is even:
   - Identify all distinct connected non-white objects where *all* pixels of the object lie in the left half of the grid (columns 0 to width/2 - 1).
   - Copy each of these identified objects to the right half of the grid using an offset of (0, width/2).
   - The output grid starts as a copy of the input, and copied pixels overwrite the existing content in the right half.

2. If the grid width is odd:
   - Identify a marker object: a horizontal 1x2 block of magenta pixels ([[6, 6]]).
   - Find the instance of this marker object whose top-left corner is closest (using Euclidean distance) to the geometric center of the grid.
   - The coordinates (r_marker, c_marker) of this marker's top-left corner define an offset vector.
   - If no such marker is found, the output is identical to the input.
   - Identify all distinct connected objects (non-white pixels) in the input grid using 4-connectivity.
   - For each identified object *except* the specific marker object instance used for the offset:
     - Copy the object to a new location in the output grid by adding the offset vector (r_marker, c_marker) to the coordinates of each pixel in the object.
     - Only pixels whose target coordinates land within the grid boundaries are placed.
     - Copied pixels overwrite the existing content at the target location. The original grid content and objects (including the marker) remain unless overwritten.
"""

def find_objects(grid, colors_to_ignore=[0]):
    """
    Finds all connected objects of the same color in the grid using 4-connectivity.

    Args:
        grid (np.array): The input grid.
        colors_to_ignore (list): List of color values to ignore (e.g., background).

    Returns:
        list: A list of tuples, where each tuple represents an object:
              (color, set_of_coordinates, top_left_coordinate).
              set_of_coordinates is a set of (row, col) tuples.
              top_left_coordinate is a tuple (min_row, min_col).
    """
    height, width = grid.shape
    visited = np.zeros((height, width), dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            # Check if the pixel is not ignored and not visited yet
            if color not in colors_to_ignore and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Track top-left for easy identification

                # Breadth-First Search (BFS) to find connected components
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)

                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds, has the same color, and hasn't been visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found object
                objects.append((color, obj_coords, (min_r, min_c)))
    return objects

def find_pattern(grid, pattern):
    """
    Finds all occurrences of a given 2D pattern in the grid.

    Args:
        grid (np.array): The input grid.
        pattern (np.array): The 2D pattern (subgrid) to search for.

    Returns:
        list: A list of (row, col) tuples representing the top-left coordinates
              of found pattern instances.
    """
    grid_h, grid_w = grid.shape
    pattern_h, pattern_w = pattern.shape
    locations = []

    # Iterate through possible top-left positions for the pattern
    for r in range(grid_h - pattern_h + 1):
        for c in range(grid_w - pattern_w + 1):
            # Extract the subgrid matching the pattern's dimensions
            subgrid = grid[r:r+pattern_h, c:c+pattern_w]
            # Compare the subgrid with the pattern
            if np.array_equal(subgrid, pattern):
                locations.append((r, c))
    return locations

def transform(input_grid):
    """
    Applies the transformation rule based on the input grid's width.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    # Initialize the output grid as a copy of the input grid
    output_np = np.copy(input_np) 

    # --- Determine transformation based on width parity ---
    if width % 2 == 0:
        # --- Even Width: Copy Left-Half Objects to Right Half ---
        
        # Calculate the midpoint column index
        mid = width // 2
        # Define the copy offset
        offset_dr, offset_dc = 0, mid
        
        # Find all distinct objects (non-white) in the entire input grid
        objects = find_objects(input_np, colors_to_ignore=[0]) 

        # Iterate through found objects to check if they are fully in the left half
        for color, coords, _ in objects:
            # Check if all pixels of the object are in the left half (column < mid)
            is_in_left_half = all(c < mid for r, c in coords)

            # If the object is entirely within the left half, copy it
            if is_in_left_half:
                # Iterate through each pixel of the object
                for r_p, c_p in coords:
                    # Calculate the target coordinates using the offset
                    target_r = r_p + offset_dr
                    target_c = c_p + offset_dc

                    # Check if the target coordinates are within the grid boundaries
                    # Note: target_c will always be >= mid because offset_dc is mid
                    if 0 <= target_r < height and target_c < width: 
                        # Place the object's pixel color at the target location in the output grid
                        output_np[target_r, target_c] = color
        
    else:
        # --- Odd Width: Offset Copy Based on Central Marker ---
        
        # Define the marker pattern: a horizontal 1x2 block of magenta (6)
        marker_pattern = np.array([[6, 6]]) 
        # Find all locations where this pattern occurs
        marker_locations = find_pattern(input_np, marker_pattern)

        # If no marker is found, the output is just the copy of the input
        if not marker_locations:
            return output_np.tolist()

        # Calculate the geometric center of the grid
        center_r = (height - 1) / 2.0
        center_c = (width - 1) / 2.0
        grid_center = (center_r, center_c)

        # Find the marker instance closest to the grid center
        closest_marker_loc = min(
            marker_locations,
            key=lambda loc: euclidean(loc, grid_center) # Use Euclidean distance
        )
        # The offset vector is the coordinates of the closest marker's top-left pixel
        offset_dr, offset_dc = closest_marker_loc 

        # Find all distinct objects (connected components of non-white pixels)
        objects = find_objects(input_np, colors_to_ignore=[0]) # Ignore white (0)
        
        # Define the relative coordinates for the marker pattern for precise identification
        marker_pixels_relative = {(0,0), (0,1)} # Relative coords for [[6, 6]] pattern

        # Iterate through all found objects to perform the copy
        for color, coords, top_left_coord in objects:
            
            # --- Check if the current object is the specific marker used for the offset ---
            is_the_offset_marker = False
            # Check color and top-left coordinate first for efficiency
            if color == 6 and top_left_coord == closest_marker_loc:
                 # Verify the exact shape/pixels relative to top-left to be sure
                 obj_pixels_relative = {(r - top_left_coord[0], c - top_left_coord[1]) for r, c in coords}
                 if obj_pixels_relative == marker_pixels_relative:
                     is_the_offset_marker = True

            # --- If it's NOT the offset marker, copy it ---
            if not is_the_offset_marker:
                # Iterate through each pixel of the object
                for r_p, c_p in coords:
                    # Calculate the target coordinates using the offset
                    target_r = r_p + offset_dr
                    target_c = c_p + offset_dc

                    # Check if the target coordinates are within the grid boundaries
                    if 0 <= target_r < height and 0 <= target_c < width:
                        # Place the object's pixel color at the target location in the output grid
                        output_np[target_r, target_c] = color

    # Convert the final NumPy array back to a list of lists before returning
    return output_np.tolist()