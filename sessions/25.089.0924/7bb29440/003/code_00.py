import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects in the input grid composed of non-white (0) pixels, considering pixels connected orthogonally and diagonally (8-way connectivity). Filter this set to include only objects that contain at least one blue (1) pixel.
For each identified object:
    a. Count the total number of magenta (6) pixels it contains (magenta_count).
    b. Count the total number of yellow (4) pixels it contains (yellow_count).
    c. Calculate its total area by counting all its non-white pixels (area).
    d. Determine the topmost row index occupied by any of its pixels (top_row_index).
Select the target object using the following priority sequence:
    a. The object with the highest magenta_count.
    b. If there's a tie, select from the tied objects the one with the lowest yellow_count.
    c. If there's still a tie, select from the tied objects the one with the largest area.
    d. If there's still a tie, select from the tied objects the one that appears lowest in the grid (i.e., has the largest top_row_index).
Determine the minimum and maximum row and column indices (bounding box) of the selected target object.
Create a new output grid whose dimensions match the height and width of the bounding box.
Copy each pixel belonging to the selected target object from the input grid into the new output grid, preserving its original color and adjusting its position relative to the top-left corner of the bounding box.
The resulting grid is the final output.
"""

def find_objects_diag(grid):
    """
    Finds all contiguous objects of non-white pixels in the grid using 8-way 
    (diagonal included) connectivity, keeping only those with at least one blue pixel.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of objects, where each object is represented as a list of 
              tuples (row, col, color).
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If pixel is non-white and not visited, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                has_blue = False
                
                while q:
                    row, col = q.popleft()
                    color = grid[row, col]
                    # Check if object contains blue
                    if color == 1:
                        has_blue = True
                    obj_pixels.append((row, col, color))

                    # Check 8 neighbors (orthogonal and diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            nr, nc = row + dr, col + dc
                            # Check bounds, non-white color, and visited status
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] != 0 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Add object to list only if it contained at least one blue pixel
                if has_blue:
                    objects.append(obj_pixels)
                    
    return objects

def analyze_object(obj_pixels):
    """
    Analyzes an object (list of pixels) to calculate its properties for selection.

    Args:
        obj_pixels (list): List of (row, col, color) tuples for the object.

    Returns:
        dict: A dictionary containing 'magenta_count', 'yellow_count', 
              'area', 'top_row_index', and the original 'pixels'.
    """
    magenta_count = 0
    yellow_count = 0
    min_r = float('inf')
    
    for r, c, color in obj_pixels:
        if color == 6:
            magenta_count += 1
        elif color == 4:
            yellow_count += 1
        min_r = min(min_r, r) # Find the topmost row index
        
    area = len(obj_pixels) # Area is the total count of pixels in the object
    
    return {
        'magenta_count': magenta_count,
        'yellow_count': yellow_count,
        'area': area,
        'top_row_index': min_r,
        'pixels': obj_pixels 
    }

def get_bounding_box(obj_pixels):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) of an object."""
    if not obj_pixels:
        # Should not happen if objects are found, but handle defensively
        return 0, 0, -1, -1 
    rows = [p[0] for p in obj_pixels]
    cols = [p[1] for p in obj_pixels]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return min_r, min_c, max_r, max_c

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for easier handling
    grid_np = np.array(input_grid, dtype=int)

    # 1. Identify all distinct composite_shape objects using 8-way connectivity
    objects_pixels = find_objects_diag(grid_np)

    # Handle case where no valid objects are found
    if not objects_pixels:
        return [] # Return empty grid or handle as per specific ARC task conventions

    # 2. Analyze each object's properties
    analyzed_objects = [analyze_object(obj) for obj in objects_pixels]

    # 3. Select the target object based on sorting criteria
    # Sort key uses a tuple: (-MaxM, MinY, -MaxA, -MaxTR) 
    # Negative sign reverses order for maximization
    analyzed_objects.sort(key=lambda x: (
        -x['magenta_count'], 
         x['yellow_count'], 
        -x['area'], 
        -x['top_row_index'] 
    ))
    
    # The best object is the first one after sorting
    selected_object = analyzed_objects[0]
    selected_pixels = selected_object['pixels']

    # 4. Determine bounding box of the selected object
    min_r, min_c, max_r, max_c = get_bounding_box(selected_pixels)
    
    # Calculate output grid dimensions
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # 5. Create the output grid (initialize with background color 0)
    output_grid_np = np.zeros((height, width), dtype=int) 

    # 6. Copy pixels from the selected object to the output grid
    for r, c, color in selected_pixels:
        # Adjust coordinates to be relative to the output grid's top-left corner
        out_r, out_c = r - min_r, c - min_c
        # Preserve the original color
        output_grid_np[out_r, out_c] = color 

    # Convert the final numpy array back to a list of lists for the expected format
    output_grid = output_grid_np.tolist()

    return output_grid