import numpy as np

"""
Identifies all distinct non-white objects in the input grid.
Calculates the bounding box height and width for each object.
Determines the overall maximum height (MaxH), maximum width (MaxW), and minimum width (MinW) across all objects.
Compares MaxH and MaxW to determine the output grid dimensions:
- If MaxH is equal to MaxW, the output dimensions are MaxH x MinW.
- If MaxH is less than MaxW, the output dimensions are MaxH x MaxH.
- If MaxH is greater than MaxW, the output dimensions are MaxW x MaxW.
Creates an output grid of the calculated dimensions filled entirely with white pixels (color 0).
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of tuples, where each tuple contains (color, set_of_coordinates).
              Returns an empty list if no objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0 # Assuming 0 is always the background

    for r in range(rows):
        for c in range(cols):
            # If this pixel is not background and hasn't been visited yet
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_coords = set()
                # Use Breadth-First Search (BFS) to find all connected pixels of the same color
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check boundaries and if the neighbor is valid
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Add the found object (color and coordinates) to the list
                if obj_coords:
                    objects.append((color, obj_coords))
    return objects

def get_bounding_box_dims(obj_coords):
    """
    Calculates the height and width of the bounding box for a set of coordinates.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (height, width) of the bounding box. Returns (0, 0) if input is empty.
    """
    if not obj_coords:
        return 0, 0
        
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    return height, width

def transform(input_grid):
    """
    Transforms the input grid based on the dimensions of the contained objects.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        np.array: The transformed output grid (filled with white).
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    
    # Find all distinct objects in the grid
    objects = find_objects(grid)
    
    # If no objects are found, return a default 1x1 white grid
    if not objects:
        return np.zeros((1, 1), dtype=int)
        
    # Calculate dimensions (height, width) for each object's bounding box
    object_dims = [get_bounding_box_dims(coords) for color, coords in objects]
    
    # Extract all heights and widths
    heights = [h for h, w in object_dims]
    widths = [w for h, w in object_dims]
    
    # Find the maximum height, maximum width, and minimum width across all objects
    max_h = max(heights)
    max_w = max(widths)
    min_w = min(widths)
    
    # Determine the output grid dimensions based on the comparison of MaxH and MaxW
    out_h, out_w = 0, 0
    if max_h == max_w:
        out_h = max_h
        out_w = min_w
    elif max_h < max_w:
        out_h = max_h
        out_w = max_h
    else: # max_h > max_w
        out_h = max_w
        out_w = max_w
        
    # Create the output grid with the calculated dimensions, filled with white (0)
    output_grid = np.zeros((out_h, out_w), dtype=int)
    
    return output_grid