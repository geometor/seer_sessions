import numpy as np
from collections import deque

"""
Identify the two distinct non-white contiguous objects in the input grid.
For each object, determine its bounding box.
Calculate the area of each object's bounding box.
Compare the areas and identify the object with the larger bounding box area.
Construct the output grid as a 2x2 grid filled entirely with the color of the object having the larger bounding box area.
"""

def find_objects(grid):
    """
    Finds all distinct contiguous objects of the same non-background color.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'coords' (set of (row, col) tuples).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    background_color = 0  # Assuming white (0) is the background

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and (r, c) not in visited:
                color = grid[r, c]
                coords = set()
                queue = deque([(r, c)])
                visited.add((r, c))
                
                while queue:
                    curr_r, curr_c = queue.popleft()
                    coords.add((curr_r, curr_c))
                    
                    # Check 4-directional neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                            
                if coords: # Ensure we found at least one pixel for the object
                    objects.append({'color': color, 'coords': coords})
                    
    return objects

def get_bounding_box(coords):
    """
    Calculates the bounding box for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (min_row, min_col, max_row, max_col) representing the bounding box.
               Returns None if coords is empty.
    """
    if not coords:
        return None
    
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    
    return (min_r, min_c, max_r, max_c)

def calculate_area(bbox):
    """
    Calculates the area of a bounding box.

    Args:
        bbox (tuple): (min_row, min_col, max_row, max_col).

    Returns:
        int: The area (height * width). Returns 0 if bbox is None.
    """
    if bbox is None:
        return 0
        
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    return height * width

def transform(input_grid):
    """
    Transforms the input grid based on the identified rule.
    Finds two non-white objects, compares their bounding box areas,
    and creates a 2x2 output grid filled with the color of the larger object.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The 2x2 output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Find all non-white objects in the grid
    objects = find_objects(grid_np)
    
    # Expecting exactly two objects based on training examples
    if len(objects) != 2:
        # Handle unexpected input: return an empty or default grid, or raise error
        # For this task, based on examples, we assume exactly two objects.
        # Returning an empty 2x2 grid or based on first object might be alternatives.
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning default.")
        # Let's return a default 2x2 black grid if the assumption fails
        return [[0, 0], [0, 0]] 

    # Get the two objects
    obj1 = objects[0]
    obj2 = objects[1]
    
    # Calculate bounding box and area for each object
    bbox1 = get_bounding_box(obj1['coords'])
    bbox2 = get_bounding_box(obj2['coords'])
    
    area1 = calculate_area(bbox1)
    area2 = calculate_area(bbox2)
    
    # Determine the target color based on the larger bounding box area
    if area1 > area2:
        target_color = obj1['color']
    elif area2 > area1:
        target_color = obj2['color']
    else:
        # Tie-breaking rule: Not explicitly defined by examples.
        # Let's assume the object appearing lower (larger min_row) wins in a tie.
        # If min_rows are also equal, default to the second object found (obj2).
        if bbox1[0] > bbox2[0]: # obj1 starts lower
             target_color = obj1['color']
        else: # obj2 starts lower or they start at the same row
             target_color = obj2['color']
        print(f"Warning: Bounding box areas are equal ({area1}). Using tie-breaking rule.")


    # Construct the 2x2 output grid filled with the target color
    output_grid = np.full((2, 2), target_color, dtype=int)
    
    # Return the output grid as a list of lists
    return output_grid.tolist()
