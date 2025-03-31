import numpy as np
from collections import deque
import operator

"""
Identifies all distinct, single-color objects in the input grid. Classifies 
objects into 'simple hollow rectangles' (at least 3x3, pixels exactly form the 
bounding box perimeter, interior is all white) and 'other objects'. 
Selects one 'other object' as the pattern source based on the largest pixel 
count (ties broken by top-most, then left-most bounding box corner). Extracts the 
pattern from the interior of the pattern source's bounding box. Selects the two 
'simple hollow rectangles' with the largest bounding box area (ties broken by 
top-most, then left-most corner). Tiles the extracted pattern into the interior 
of the selected target rectangles, using the color of each target rectangle's 
frame. Outputs the modified grid.
"""

def find_object_pixels(grid, start_row, start_col, visited):
    """
    Finds all connected pixels (4-connectivity) of the same color starting 
    from (start_row, start_col) that haven't been visited yet.
    Updates the visited set.
    Returns:
        - object_pixels (set): Set of (row, col) tuples for the object.
        - color (int): The color index of the object.
        - bbox (tuple): (min_row, min_col, max_row, max_col).
        - pixel_count (int): Number of pixels in the object.
    Returns (None, -1, None, 0) if the starting pixel is invalid (background or visited).
    """
    rows, cols = grid.shape
    color = grid[start_row, start_col]
    
    # Check if starting pixel is already visited or is background
    if color == 0 or (start_row, start_col) in visited:
        return None, -1, None, 0

    q = deque([(start_row, start_col)])
    object_pixels = set()
    pixel_count = 0
    min_r, min_c = start_row, start_col
    max_r, max_c = start_row, start_col
    
    visited.add((start_row, start_col)) # Mark start as visited immediately

    while q:
        r, c = q.popleft()
        
        # Add to object and update bounds
        object_pixels.add((r, c))
        pixel_count += 1
        min_r = min(min_r, r)
        max_r = max(max_r, r)
        min_c = min(min_c, c)
        max_c = max(max_c, c)
        
        # Add valid, unvisited neighbors of the same color to the queue
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == color and (nr, nc) not in visited:
                 visited.add((nr, nc)) # Mark neighbor as visited when adding to queue
                 q.append((nr, nc))
                 
    bbox = (min_r, min_c, max_r, max_c)
    return object_pixels, color, bbox, pixel_count

def is_simple_hollow_rectangle(grid, object_pixels, bbox):
    """
    Checks if a set of object pixels forms a simple hollow rectangle.
    Returns (is_hollow (bool), area (int) if hollow else 0).
    """
    if not object_pixels: return False, 0
    min_row, min_col, max_row, max_col = bbox
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    # Check 1: Minimum size 3x3
    if height < 3 or width < 3: return False, 0

    # Check 2: All object pixels must be exactly on the bounding box perimeter
    expected_perimeter_pixels = set()
    # Top and bottom rows
    for c in range(min_col, max_col + 1):
        expected_perimeter_pixels.add((min_row, c))
        expected_perimeter_pixels.add((max_row, c))
    # Left and right columns (excluding corners already added)
    for r in range(min_row + 1, max_row):
        expected_perimeter_pixels.add((r, min_col))
        expected_perimeter_pixels.add((r, max_col))
        
    # Compare the actual object pixels with the expected perimeter pixels
    if object_pixels != expected_perimeter_pixels:
        return False, 0 

    # Check 3: All interior pixels must be white (0)
    for r in range(min_row + 1, max_row):
        for c in range(min_col + 1, max_col):
            if grid[r, c] != 0:
                return False, 0 # Non-white pixel found inside

    # If all checks pass, it's a simple hollow rectangle
    area = height * width
    return True, area

def extract_pattern_grid(grid, source_bbox):
    """
    Extracts the 2D pattern from the interior of the source object's bounding box.
    Returns a numpy array representing the pattern, or None if no interior exists.
    """
    min_r, min_c, max_r, max_c = source_bbox
    pattern_h = max_r - min_r - 1
    pattern_w = max_c - min_c - 1

    if pattern_h <= 0 or pattern_w <= 0:
        return None # No interior to extract pattern from

    pattern = grid[min_r + 1 : max_r, min_c + 1 : max_c]
    return pattern

def tile_fill_interior(output_grid, target_bbox, target_color, pattern_grid):
    """
    Fills the interior of the target rectangle by tiling the pattern grid.
    Modifies output_grid in place.
    """
    if pattern_grid is None or pattern_grid.size == 0:
        return # Cannot fill if pattern is invalid or empty

    min_r, min_c, max_r, max_c = target_bbox
    pattern_h, pattern_w = pattern_grid.shape

    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            # Calculate corresponding pattern coordinates using modulo
            rel_r = r - (min_r + 1)
            rel_c = c - (min_c + 1)
            p_r = rel_r % pattern_h
            p_c = rel_c % pattern_w

            # Check the color in the pattern grid
            pattern_pixel_color = pattern_grid[p_r, p_c]

            # If the pattern pixel is not background (0), fill with target color
            if pattern_pixel_color != 0:
                output_grid[r, c] = target_color


def transform(input_grid):
    # Convert input to numpy array and initialize output grid
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    rows, cols = input_grid_np.shape
    visited = set()
    
    all_objects = []

    # 1. Identify and Classify Objects
    for r in range(rows):
        for c in range(cols):
            pixels, color, bbox, pixel_count = find_object_pixels(input_grid_np, r, c, visited)
            
            if pixels: # If a valid object was found
                is_hollow, area = is_simple_hollow_rectangle(input_grid_np, pixels, bbox)
                all_objects.append({
                    'pixels': pixels,
                    'color': color,
                    'bbox': bbox,
                    'pixel_count': pixel_count,
                    'is_hollow': is_hollow,
                    'area': area if is_hollow else 0 # Store area only if hollow
                })

    # Separate into hollow rectangles and potential pattern sources
    hollow_rects = [o for o in all_objects if o['is_hollow']]
    other_objects = [o for o in all_objects if not o['is_hollow']]

    # 2. Select Pattern Source
    pattern_source_object = None
    if other_objects:
        # Sort by pixel_count (desc), min_row (asc), min_col (asc)
        other_objects.sort(key=lambda x: (-x['pixel_count'], x['bbox'][0], x['bbox'][1]))
        pattern_source_object = other_objects[0]

    # 3. Extract Pattern
    pattern_grid = None
    if pattern_source_object:
        pattern_grid = extract_pattern_grid(input_grid_np, pattern_source_object['bbox'])

    # 4. Select Target Rectangles
    target_rectangles = []
    if hollow_rects:
        # Sort by area (desc), min_row (asc), min_col (asc)
        hollow_rects.sort(key=lambda x: (-x['area'], x['bbox'][0], x['bbox'][1]))
        target_rectangles = hollow_rects[:2] # Select top two

    # 5. Tile Fill Interiors
    if pattern_grid is not None and pattern_grid.size > 0: # Check if pattern is valid
        for target in target_rectangles:
            tile_fill_interior(output_grid, target['bbox'], target['color'], pattern_grid)

    # Convert back to list of lists and return
    return output_grid.tolist()