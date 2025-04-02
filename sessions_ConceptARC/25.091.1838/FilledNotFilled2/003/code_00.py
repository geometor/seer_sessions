import numpy as np
from collections import deque

"""
Transforms an input grid containing distinct non-white objects into an output grid filled with white (0).
The dimensions of the output grid are determined by the properties of the objects in the input grid.

1. Identify all contiguous blocks of non-white pixels (objects).
2. Calculate the bounding box height (H) and width (W) for each object.
3. Determine the overall maximum height (MaxH), maximum width (MaxW), and minimum width (MinW) across all objects.
4. Compare MaxH and MaxW:
   - If MaxH > MaxW: Output dimensions are MaxW x MaxW.
   - If MaxH <= MaxW: Output dimensions are MaxH x MinW.
5. Create an output grid with the calculated dimensions, filled entirely with white (0).
"""

def find_objects(grid: np.ndarray) -> list[tuple[int, set[tuple[int, int]]]]:
    """
    Finds all contiguous objects of the same non-background color using BFS.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A list of tuples, where each tuple contains (color, set_of_coordinates).
        Returns an empty list if no non-background objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0 # Define background color

    for r in range(rows):
        for c in range(cols):
            # If this pixel is not background and hasn't been visited
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)]) # Use deque for efficient pop(0)
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft() # BFS uses popleft
                    obj_coords.add((row, col))
                    
                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check boundaries and if the neighbor is valid (same color, not visited)
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Add the found object to the list
                if obj_coords:
                    objects.append((color, obj_coords))
    return objects

def get_bounding_box_dims(obj_coords: set[tuple[int, int]]) -> tuple[int, int]:
    """
    Calculates the height and width of the bounding box for a set of coordinates.

    Args:
        obj_coords: A set of (row, col) tuples representing the object's pixels.

    Returns:
        A tuple (height, width) of the bounding box. Returns (0, 0) if input is empty.
    """
    if not obj_coords:
        return 0, 0
        
    # Extract row and column indices
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    
    # Find min/max row and column to define the bounding box
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    # Calculate height and width (inclusive of boundaries)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    return height, width

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: The input grid represented as a list of lists.

    Returns:
        The transformed output grid as a list of lists.
    """
    # Convert input to numpy array for easier processing
    grid = np.array(input_grid, dtype=int)
    
    # Step 1: Identify all distinct non-white objects
    objects = find_objects(grid)
    
    # Handle edge case: no objects found
    if not objects:
        # Return a default 1x1 white grid if no objects are present
        return [[0]] 
        
    # Step 2: Calculate bounding box dimensions for each object
    object_dims = [get_bounding_box_dims(coords) for color, coords in objects]
    
    # Step 3: Aggregate properties - Max Height, Max Width, Min Width
    heights = [h for h, w in object_dims if h > 0] # Ensure we don't include 0 if an object somehow had 0 height/width
    widths = [w for h, w in object_dims if w > 0]
    
    # Handle edge case where heights/widths might be empty if filtering removed all
    if not heights or not widths:
         return [[0]] # Or another appropriate default/error handling

    max_h = max(heights)
    max_w = max(widths)
    min_w = min(widths)
    
    # Step 4: Determine output grid dimensions based on the rule
    out_h, out_w = 0, 0
    if max_h > max_w:
        # Rule 1: If MaxH > MaxW, output is MaxW x MaxW
        out_h = max_w
        out_w = max_w
    else: # max_h <= max_w
        # Rule 2: If MaxH <= MaxW, output is MaxH x MinW
        out_h = max_h
        out_w = min_w
        
    # Step 5: Create the output grid with calculated dimensions, filled with white (0)
    # Ensure dimensions are at least 1x1
    out_h = max(1, out_h)
    out_w = max(1, out_w)
    output_grid_np = np.zeros((out_h, out_w), dtype=int)
    
    # Convert back to list of lists for the required output format
    output_grid = output_grid_np.tolist()
    
    return output_grid