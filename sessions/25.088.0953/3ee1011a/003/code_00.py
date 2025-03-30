import numpy as np
from collections import deque
import math

"""
Identifies all distinct colored objects (contiguous non-white pixels) in the input grid.
Calculates the bounding box, area, and aspect ratio for each object.
Determines a 'center object' based on the minimum bounding box area, using aspect ratio closeness to 1 as a tie-breaker.
Sorts the remaining objects by bounding box area in ascending order. This defines the layer order from inside to outside.
Determines the output grid size (N x N) based on the largest dimension (width or height) of any object's bounding box.
Constructs the output grid by drawing concentric filled square layers, starting from the outermost layer and working inwards.
The outermost layer (N x N) uses the color of the object with the largest area (excluding the center object if it's not the largest).
Subsequent layers decrease in size by 2 (e.g., (N-2)x(N-2), (N-4)x(N-4)...) and use the colors of the objects in descending order of area.
The innermost layer uses the color of the 'center object'.
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
    """ Draws a filled centered square of given size and color onto the grid. """
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
    Transforms the input grid based on identified object properties.
    """
    input_np = np.array(input_grid, dtype=int)

    # 1. Identify Objects
    objects_found = find_objects(input_np)
    if not objects_found:
        # Return a minimal grid if no objects found
        return [[0]] 

    # 2. Analyze Objects (Calculate Bounding Box Properties)
    object_details = calculate_bounding_boxes(objects_found)
    if not object_details:
         # Should not happen if objects_found is not empty, but handle defensively
        return [[0]]

    # 3. Determine Output Size
    # Find the maximum dimension (width or height) among all bounding boxes
    max_dim = 0
    for obj in object_details:
        max_dim = max(max_dim, obj['width'], obj['height'])
    
    output_size = max_dim
    if output_size == 0: # Handle edge case where objects might be 0-dimensional (shouldn't happen)
        return [[0]]

    # 4. Order Objects for Layering
    # Sort primarily by area (ascending), secondarily by aspect ratio deviation from 1 (ascending)
    object_details.sort(key=lambda x: (x['area'], abs(x['aspect_ratio'] - 1)))
    
    # The sorted list `object_details` now represents the layers from inside to outside.
    # The first element is the 'center object'.
    
    # 5. Construct Output Layers (Draw Outside-In)
    # Initialize the N x N output grid with background color 0
    output_grid = np.zeros((output_size, output_size), dtype=int)
    
    num_layers = len(object_details)
    
    # Iterate through the layers from outside (largest area object) to inside (center object)
    for i in range(num_layers):
        # The object for the current layer (working from outside inwards)
        # Index `num_layers - 1 - i` corresponds to the object for the i-th layer from the outside
        obj_index = num_layers - 1 - i
        current_object = object_details[obj_index]
        
        # Calculate the size of the current square layer
        # Outermost layer (i=0) has size N, next (i=1) has N-2, etc.
        current_layer_size = output_size - (2 * i)
        
        # Ensure layer size is at least 1
        if current_layer_size < 1:
            current_layer_size = 1
            
        # Draw the filled square for this layer
        draw_centered_square(output_grid, current_layer_size, current_object['color'])

    # 6. Final Output
    return output_grid.tolist()