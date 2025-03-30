import numpy as np
from collections import deque
import math

"""
Identifies all distinct colored objects (contiguous non-white pixels) in the input grid.
Calculates the bounding box, area, and aspect ratio for each object.
Determines a 'center object' based on the minimum bounding box area, using aspect ratio closeness to 1 as a tie-breaker.
Sorts the remaining objects by bounding box area in ascending order.
Determines the output grid size based on the largest dimension (width or height) of the object with the largest bounding box area.
Constructs the output grid by drawing concentric square layers, starting from the innermost layer.
The innermost layer uses the color of the 'center object'. Subsequent layers outwards use the colors of the other objects, ordered by their ascending bounding box area.
The size of the layers increases by 2 units (width and height) for each step outwards. The final layer fills the entire output grid.
"""

def find_objects(grid):
    """
    Finds all contiguous blocks of non-background (non-zero) pixels.

    Args:
        grid (np.array): Input grid.

    Returns:
        list: A list of objects, where each object is a tuple containing:
              - color (int): The color of the object.
              - coordinates (list): A list of (row, col) tuples for pixels belonging to the object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If pixel is not background (0) and not visited
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                obj_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                # Breadth-First Search (BFS) to find connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_coords.append((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_coords:
                    objects.append((color, obj_coords))
                    
    return objects

def calculate_bounding_boxes(objects):
    """
    Calculates bounding box properties for each object.

    Args:
        objects (list): List of objects from find_objects.

    Returns:
        list: A list of dictionaries, each containing object properties:
              'color', 'coords', 'bbox' (min_r, min_c, max_r, max_c), 
              'width', 'height', 'area', 'aspect_ratio'.
              Returns empty list if input objects list is empty.
    """
    object_details = []
    if not objects:
        return object_details

    for color, coords in objects:
        if not coords: continue # Skip if an object somehow has no coordinates

        rows = [r for r, c in coords]
        cols = [c for r, c in coords]
        
        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)
        
        height = max_r - min_r + 1
        width = max_c - min_c + 1
        area = width * height
        
        # Calculate aspect ratio (larger dim / smaller dim), handle 0 dim case
        if min(width, height) > 0:
            aspect_ratio = max(width, height) / min(width, height)
        else:
            # Should not happen for valid objects, but handle defensively
            aspect_ratio = float('inf') 

        object_details.append({
            'color': color,
            'coords': coords,
            'bbox': (min_r, min_c, max_r, max_c),
            'width': width,
            'height': height,
            'area': area,
            'aspect_ratio': aspect_ratio
        })
        
    return object_details

def draw_centered_square(grid, layer_size, color):
    """ Draws a centered square of given size and color onto the grid. """
    grid_size = grid.shape[0] # Assuming square grid
    if layer_size <= 0:
        return # Cannot draw non-positive size square

    # Calculate top-left corner for centering
    start_r = (grid_size - layer_size) // 2
    start_c = (grid_size - layer_size) // 2
    
    # Ensure calculated coordinates are within bounds (can happen if layer_size > grid_size)
    start_r = max(0, start_r)
    start_c = max(0, start_c)
    end_r = min(grid_size, start_r + layer_size)
    end_c = min(grid_size, start_c + layer_size)

    # Fill the square area
    grid[start_r:end_r, start_c:end_c] = color


def transform(input_grid):
    """
    Transforms the input grid by finding objects, ordering them by size,
    and drawing them as concentric layers in a new output grid.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # 1. Find all colored objects
    objects_found = find_objects(np.array(input_grid))
    if not objects_found:
        # Handle cases with no objects if necessary, maybe return empty or input grid?
        # For now, assume valid inputs have objects. Returning small default grid.
        return np.zeros((1, 1), dtype=int) 

    # 2. Calculate bounding box properties for each object
    object_details = calculate_bounding_boxes(objects_found)
    if not object_details:
        return np.zeros((1, 1), dtype=int) # Should not happen if objects_found is not empty

    # 3. Identify the 'center object' (min area, tie-break with aspect ratio closest to 1)
    # Sort by area ascending, then by aspect ratio deviation from 1 ascending
    object_details.sort(key=lambda x: (x['area'], abs(x['aspect_ratio'] - 1)))
    center_object = object_details[0]
    
    # 4. Separate other objects and sort them by area ascending
    other_objects = object_details[1:]
    # No need to re-sort 'other_objects' as they are already sorted by area (primary key)

    # 5. Identify the object with the largest bounding box area among *all* objects
    # This is needed to determine the output size. Since object_details is sorted by area,
    # the last element *might* not be the one with the largest max(width, height).
    # We need the object whose max dimension determines the output grid size.
    largest_dim_object = max(object_details, key=lambda x: max(x['width'], x['height']))
    output_size = max(largest_dim_object['width'], largest_dim_object['height'])

    # 6. Create the N x N output grid, initialize with a default value (e.g., 0)
    output_grid = np.zeros((output_size, output_size), dtype=int)

    # 7. Determine the order of objects for drawing layers (inside-out)
    # Order: center object, then other objects sorted by area ascending.
    drawing_order = [center_object] + other_objects # Already sorted correctly

    # 8. Draw layers from inside out
    num_layers = len(drawing_order)
    # Calculate the size of the innermost layer
    innermost_layer_size = output_size - 2 * (num_layers - 1)
    if innermost_layer_size < 1:
        innermost_layer_size = 1 # Ensure layer size is at least 1

    for i, obj in enumerate(drawing_order):
        current_layer_size = innermost_layer_size + 2 * i
        draw_centered_square(output_grid, current_layer_size, obj['color'])

    return output_grid.tolist() # Return as list of lists per spec