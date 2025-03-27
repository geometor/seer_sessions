import numpy as np
from collections import deque

"""
This program identifies all distinct objects (contiguous blocks of the same 
non-background color) in the input grid. For each object, it calculates its 
bounding box and the ratio of the object's pixels to the area of its bounding 
box (fill ratio). It then selects the object with the highest fill ratio. 
If there's a tie in fill ratios, it selects the object whose bounding box's 
top-left corner is highest up, and then furthest to the left. Finally, it 
extracts the rectangular region corresponding to the selected object's bounding 
box from the input grid and returns this subgrid as the output.
"""

def find_objects(grid, background_color=0):
    """
    Finds all distinct connected objects of the same non-background color.
    Uses 8-way connectivity (including diagonals).

    Args:
        grid (np.array): The input grid.
        background_color (int): The color designated as background.

    Returns:
        list: A list of dictionaries, each representing an object with 
              'color' and 'coords' (a set of (row, col) tuples).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            # Check if pixel is part of an object and not yet visited
            if grid[r, c] != background_color and not visited[r, c]:
                object_color = grid[r, c]
                current_object_coords = set()
                q = deque([(r, c)]) # Use a queue for BFS
                visited[r, c] = True
                
                # Perform BFS to find all connected pixels of the same color
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_coords.add((curr_r, curr_c))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                                
                            nr, nc = curr_r + dr, curr_c + dc
                            
                            # Check bounds, color match, and not visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] == object_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                # Store the found object if it has pixels
                if current_object_coords: 
                    objects.append({'color': object_color, 'coords': current_object_coords})
                    
    return objects

def get_bounding_box(coords):
    """
    Calculates the minimal bounding box for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples representing object pixels.

    Returns:
        tuple: (min_row, max_row, min_col, max_col) or None if coords is empty.
    """
    if not coords:
        return None 

    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    return (min_r, max_r, min_c, max_c)

def transform(input_grid):
    """
    Identifies objects, calculates fill ratios, selects the object with the 
    maximum fill ratio (using top-left tie-breaking), and extracts its 
    bounding box from the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The extracted subgrid corresponding to the selected 
                       object's bounding box. Returns [[]] if no objects found.
    """
    grid = np.array(input_grid, dtype=int)
    
    # Handle empty input grid edge case
    if grid.size == 0:
        return [[]]
        
    height, width = grid.shape
    background_color = 0

    # Find all objects in the grid
    objects = find_objects(grid, background_color)

    # If no objects are found, return an empty grid representation
    if not objects:
        return [[]] 

    max_fill_ratio = -1.0
    selected_object_bbox = None
    selected_object_coords = None # Keep track of coordinates for tie-breaking comparison

    # Iterate through each found object to calculate properties and find the best one
    for obj in objects:
        coords = obj['coords']
        pixel_count = len(coords)
        
        # Should not happen with current find_objects logic, but safety check
        if pixel_count == 0: 
             continue

        # Calculate the bounding box of the object
        bbox = get_bounding_box(coords)
        if bbox is None: # Should not happen if pixel_count > 0
            continue
            
        min_r, max_r, min_c, max_c = bbox
        
        # Calculate bounding box dimensions and area
        bbox_height = max_r - min_r + 1
        bbox_width = max_c - min_c + 1
        bbox_area = bbox_height * bbox_width

        # Calculate the fill ratio
        fill_ratio = pixel_count / bbox_area

        # Check if this object has a higher fill ratio or wins the tie-breaker
        update_selection = False
        if fill_ratio > max_fill_ratio:
            update_selection = True
        elif fill_ratio == max_fill_ratio:
            # Tie-breaking: prefer top-most (min_r), then left-most (min_c)
            current_min_r, _, current_min_c, _ = selected_object_bbox
            if min_r < current_min_r:
                update_selection = True
            elif min_r == current_min_r and min_c < current_min_c:
                update_selection = True

        # Update the selected object if necessary
        if update_selection:
            max_fill_ratio = fill_ratio
            selected_object_bbox = bbox
            # selected_object_coords = coords # Not strictly needed after selection

    # If somehow no object was selected (e.g., all objects had issues), return empty
    if selected_object_bbox is None:
         return [[]]

    # Extract the subgrid corresponding to the selected object's bounding box
    min_r, max_r, min_c, max_c = selected_object_bbox
    output_grid = grid[min_r:max_r+1, min_c:max_c+1]

    # Return the output grid as a list of lists
    return output_grid.tolist()