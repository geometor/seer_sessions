import numpy as np
from collections import deque

"""
Identify the largest contiguous non-white object (main_shape) and a 
single-pixel non-white object (target_pixel) in the input grid.
Recolor the main_shape with the color of the target_pixel.
Set the original location of the target_pixel to white (0).
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in the grid.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'color', 'coords' (list of (r, c) tuples), and 'size'.
        Returns an empty list if no non-white objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If the pixel is non-white and not visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True

                while q:
                    row, col = q.popleft()
                    obj_coords.append((row, col))

                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'size': len(obj_coords)
                })
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the specified rules.

    Args:
        input_grid: A 2D numpy array representing the input grid.

    Returns:
        A 2D numpy array representing the transformed output grid.
    """
    # Find all non-white objects in the input grid
    objects = find_objects(input_grid)

    if not objects:
        return input_grid.copy() # Return copy if no objects found

    # Identify the main shape (largest object) and the target pixel (single pixel object)
    main_shape = None
    target_pixel_obj = None
    
    # Find the object with the maximum size
    max_size = 0
    for obj in objects:
        if obj['size'] > max_size:
            max_size = obj['size']
            
    # Separate objects into potential main shapes and potential target pixels
    potential_main_shapes = [obj for obj in objects if obj['size'] == max_size]
    potential_target_pixels = [obj for obj in objects if obj['size'] == 1 and obj['size'] != max_size]

    # Assuming exactly one main shape and one target pixel based on examples
    if len(potential_main_shapes) == 1 and len(potential_target_pixels) == 1:
        main_shape = potential_main_shapes[0]
        target_pixel_obj = potential_target_pixels[0]
    else:
        # Fallback or error handling if assumptions don't hold
        # For now, let's try finding the largest and *any* single pixel object
        # if the strict condition fails, but prefer the distinct color one if multiple singles exist
        objects.sort(key=lambda x: x['size'], reverse=True)
        if len(objects) >= 2:
            main_shape = objects[0]
            single_pixel_candidates = [obj for obj in objects[1:] if obj['size'] == 1]
            if len(single_pixel_candidates) == 1:
                 target_pixel_obj = single_pixel_candidates[0]
            elif len(single_pixel_candidates) > 1:
                 # If multiple single pixels, maybe pick one not adjacent? Or first one?
                 # Based on examples, it seems unique. Let's just pick the first.
                 target_pixel_obj = single_pixel_candidates[0]

    # Check if both main_shape and target_pixel_obj were found
    if main_shape is None or target_pixel_obj is None:
        # If we couldn't identify the objects as expected, return the original grid
        # This might happen if there's only one object, or multiple large objects, etc.
        return input_grid.copy()

    # Get the target color from the target pixel object
    target_color = target_pixel_obj['color']

    # Get the coordinates of the target pixel
    target_pixel_loc = target_pixel_obj['coords'][0] # It's a list containing one tuple

    # Initialize the output grid as a copy of the input
    output_grid = input_grid.copy()

    # Recolor the main shape in the output grid
    for r, c in main_shape['coords']:
        output_grid[r, c] = target_color

    # Change the original location of the target pixel to white
    output_grid[target_pixel_loc[0], target_pixel_loc[1]] = 0

    return output_grid