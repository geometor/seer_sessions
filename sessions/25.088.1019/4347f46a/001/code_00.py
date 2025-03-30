import numpy as np

"""
Identifies solid, non-white rectangular objects in the input grid and hollows them out. 
The border of each rectangle retains its original color, while the interior pixels are changed to white (0). 
Pixels not part of any rectangle remain unchanged.
"""

def find_objects(grid, visited, r, c, color):
    """
    Finds all connected pixels of the same color starting from (r, c) using BFS.
    Returns a list of coordinates [(r1, c1), (r2, c2), ...] belonging to the object.
    """
    rows, cols = grid.shape
    q = [(r, c)]
    obj_pixels = set()
    
    while q:
        curr_r, curr_c = q.pop(0)
        
        if not (0 <= curr_r < rows and 0 <= curr_c < cols) or \
           visited[curr_r, curr_c] or \
           grid[curr_r, curr_c] != color:
            continue
            
        visited[curr_r, curr_c] = True
        obj_pixels.add((curr_r, curr_c))
        
        # Add neighbors (4-connectivity is sufficient for solid rectangles)
        q.append((curr_r + 1, curr_c))
        q.append((curr_r - 1, curr_c))
        q.append((curr_r, curr_c + 1))
        q.append((curr_r, curr_c - 1))
        
    return list(obj_pixels)

def get_bounding_box(pixels):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a list of pixel coordinates."""
    if not pixels:
        return None
    min_r = min(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_r = max(r for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, min_c, max_r, max_c

def is_solid_rectangle(grid, pixels, bbox):
    """Checks if the object defined by pixels forms a solid rectangle within its bounding box."""
    if not bbox:
        return False
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    # Check if the number of pixels matches the bounding box area
    if len(pixels) != height * width:
        return False
        
    # Additionally, check if all pixels within the bounding box have the object's color
    # (This is slightly redundant if len(pixels) matches area, but good for robustness)
    obj_color = grid[pixels[0][0], pixels[0][1]]
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            if grid[r, c] != obj_color:
                return False # Found a pixel within bbox that doesn't match object color
                
    return True

def transform(input_grid):
    """
    Transforms the input grid by finding solid non-white rectangles and hollowing them out.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Keep track of visited pixels to avoid processing parts of the same object multiple times
    visited = np.zeros_like(input_np, dtype=bool)
    
    rectangles = []

    # Step 1: Identify all distinct, solid, non-white rectangular objects
    for r in range(rows):
        for c in range(cols):
            color = input_np[r, c]
            # If it's a non-white pixel and not visited yet
            if color != 0 and not visited[r, c]:
                # Find all connected pixels of the same color
                obj_pixels = find_objects(input_np, visited, r, c, color)
                
                if not obj_pixels:
                    continue

                # Determine the bounding box
                bbox = get_bounding_box(obj_pixels)

                # Check if the object is a solid rectangle
                if is_solid_rectangle(input_np, obj_pixels, bbox):
                    rectangles.append(bbox) # Store the bounding box

    # Step 2: Hollow out the identified rectangles in the output grid
    for bbox in rectangles:
        min_r, min_c, max_r, max_c = bbox
        
        # Iterate through the interior pixels of the rectangle
        # Only hollow if the rectangle is at least 3x3 (has an interior)
        if max_r - min_r > 1 and max_c - min_c > 1:
             for r_interior in range(min_r + 1, max_r):
                 for c_interior in range(min_c + 1, max_c):
                     # Set interior pixels to white (0)
                     output_grid[r_interior, c_interior] = 0

    # Convert back to list of lists if necessary (often standard ARC format)
    return output_grid.tolist()