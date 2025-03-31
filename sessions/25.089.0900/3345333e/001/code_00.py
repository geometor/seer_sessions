import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all distinct, contiguous groups of non-white (non-0) pixels in the input grid. These are the "objects".
2. For each identified object:
    a. Determine its bounding box (the smallest rectangle containing all its pixels).
    b. Calculate the area of the bounding box (width * height).
    c. Count the number of pixels belonging to the object.
    d. Calculate the object's "solidity" by dividing its pixel count by its bounding box area.
3. Identify the object(s) whose calculated solidity is exactly 1.0. These objects are solid rectangles.
4. Create the output grid by copying the input grid.
5. For every pixel belonging to any identified solid rectangular object, change its color in the output grid to white (0).
6. The modified grid is the final output.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color in the grid.
    Uses 8-way connectivity (including diagonals).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' and 'pixels' (a set of (row, col) tuples).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If pixel is background (0) or already visited, skip
            if grid[r, c] == 0 or (r, c) in visited:
                continue
                
            # Start BFS to find a new object
            current_color = grid[r, c]
            current_object_pixels = set()
            q = deque([(r, c)])
            visited.add((r, c))
            
            while q:
                row, col = q.popleft()
                current_object_pixels.add((row, col))
                
                # Check 8 neighbors (including diagonals)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue # Skip self
                            
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if not visited and has the same color
                            if (nr, nc) not in visited and grid[nr, nc] == current_color:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                                
            # Store the found object
            if current_object_pixels:
                objects.append({'color': current_color, 'pixels': current_object_pixels})
                
    return objects

def get_bounding_box(pixels):
    """
    Calculates the bounding box for a set of pixels.

    Args:
        pixels (set): A set of (row, col) tuples.

    Returns:
        dict: A dictionary containing 'min_row', 'max_row', 'min_col', 'max_col'.
              Returns None if the pixels set is empty.
    """
    if not pixels:
        return None
        
    min_r = min(r for r, c in pixels)
    max_r = max(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_c = max(c for r, c in pixels)
    
    return {'min_row': min_r, 'max_row': max_r, 'min_col': min_c, 'max_col': max_c}

def calculate_solidity(pixel_count, bounding_box):
    """
    Calculates the solidity of an object.

    Args:
        pixel_count (int): The number of pixels in the object.
        bounding_box (dict): The bounding box dictionary.

    Returns:
        float: The solidity value (pixel_count / bounding_box_area).
               Returns 0 if bounding_box is None or area is 0.
    """
    if not bounding_box:
        return 0.0
        
    bbox_height = bounding_box['max_row'] - bounding_box['min_row'] + 1
    bbox_width = bounding_box['max_col'] - bounding_box['min_col'] + 1
    bbox_area = bbox_height * bbox_width
    
    if bbox_area == 0:
        return 0.0 # Should not happen for non-empty objects
        
    return pixel_count / bbox_area

def transform(input_grid):
    """
    Transforms the input grid by removing solid rectangular objects.

    Args:
        input_grid (list of lists): The input grid representation.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Find all non-background objects in the input grid
    objects = find_objects(input_np)
    
    # Identify pixels belonging to solid rectangular objects
    pixels_to_remove = set()
    for obj in objects:
        pixels = obj['pixels']
        pixel_count = len(pixels)
        
        if pixel_count == 0:
            continue
            
        # Calculate bounding box and solidity
        bounding_box = get_bounding_box(pixels)
        solidity = calculate_solidity(pixel_count, bounding_box)
        
        # Check if the object is a solid rectangle (solidity == 1.0)
        # Use a small tolerance for floating point comparison
        if abs(solidity - 1.0) < 1e-9:
            pixels_to_remove.update(pixels)
            
    # Remove the identified pixels by setting them to background color (0)
    for r, c in pixels_to_remove:
        output_grid[r, c] = 0
        
    # Convert the result back to a list of lists
    return output_grid.tolist()