import numpy as np
from collections import deque

"""
Identifies four distinct L-shaped objects (3 pixels of the same non-white color) in the input grid.
Maps each L-shape to a specific 2x2 quadrant in a 4x4 output grid based on its orientation.
The 2x2 representation preserves the object's color and shape, using white (0) for the empty cell within the L-shape's 2x2 bounding box.

Mapping rule:
- L-shape with empty bottom-right corner maps to output top-left quadrant.
- L-shape with empty top-right corner maps to output bottom-left quadrant.
- L-shape with empty top-left corner maps to output bottom-right quadrant.
- L-shape with empty bottom-left corner maps to output top-right quadrant.
"""

def find_objects(grid):
    """
    Finds connected components of the same non-background color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color' (int) and 'pixels' (list of tuples (r, c)).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and (r, c) not in visited:
                color = grid[r, c]
                obj_pixels = []
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if obj_pixels:
                    objects.append({'color': color, 'pixels': obj_pixels})
    return objects

def get_l_shape_details(color, pixels):
    """
    Determines the 2x2 representation and empty cell position for an L-shape object.

    Args:
        color (int): The color of the object.
        pixels (list): List of (row, col) tuples for the object's pixels.

    Returns:
        tuple: (shape_2x2 (np.array), empty_cell (tuple(r, c))), or None if not a valid L-shape.
               Empty cell coordinates are relative to the 2x2 shape (0,0), (0,1), (1,0), or (1,1).
    """
    if len(pixels) != 3:
        return None, None # Not an L-shape if pixel count is not 3

    min_r = min(r for r, c in pixels)
    max_r = max(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_c = max(c for r, c in pixels)

    height = max_r - min_r + 1
    width = max_c - min_c + 1

    if height != 2 or width != 2:
         return None, None # Not contained within a 2x2 bounding box

    shape_2x2 = np.zeros((2, 2), dtype=int)
    empty_cell_relative = None

    for r in range(2):
        for c in range(2):
            abs_r, abs_c = min_r + r, min_c + c
            if (abs_r, abs_c) in pixels:
                shape_2x2[r, c] = color
            else:
                # Check if we already found an empty cell - L shapes have only one
                if empty_cell_relative is not None:
                    return None, None # More than one empty cell in 2x2 box means not L-shape
                empty_cell_relative = (r, c)

    if empty_cell_relative is None:
        # This should not happen if pixel count is 3 and bbox is 2x2
        return None, None 

    return shape_2x2, empty_cell_relative


def transform(input_grid):
    """
    Transforms the input grid based on the L-shape mapping rule.

    Args:
        input_grid (np.array): The input grid as a numpy array.

    Returns:
        np.array: The transformed 4x4 output grid.
    """
    # Initialize a 4x4 output grid with the background color (white, 0)
    output_grid = np.zeros((4, 4), dtype=int)
    
    # Find all distinct non-background objects in the input grid
    objects = find_objects(np.array(input_grid))
    
    # Expect exactly 4 L-shaped objects
    if len(objects) != 4:
        # Handle error or unexpected input - perhaps return empty or input?
        # For now, proceed assuming valid input structure as per examples.
        print(f"Warning: Expected 4 objects, found {len(objects)}")

    # Process each found object
    for obj in objects:
        color = obj['color']
        pixels = obj['pixels']
        
        # Determine the L-shape's 2x2 representation and its orientation (empty cell position)
        shape_2x2, empty_cell = get_l_shape_details(color, pixels)
        
        if shape_2x2 is None or empty_cell is None:
             # Skip if the object is not a valid L-shape
            print(f"Warning: Skipping invalid object with color {color} at {pixels[0]}")
            continue

        # Determine the target quadrant based on the empty cell position
        target_r, target_c = 0, 0 # Default top-left
        
        if empty_cell == (1, 1): # Empty bottom-right -> Top-Left
            target_r, target_c = 0, 0
        elif empty_cell == (0, 1): # Empty top-right -> Bottom-Left
            target_r, target_c = 2, 0
        elif empty_cell == (0, 0): # Empty top-left -> Bottom-Right
            target_r, target_c = 2, 2
        elif empty_cell == (1, 0): # Empty bottom-left -> Top-Right
            target_r, target_c = 0, 2
        else:
            # Should not happen with valid L-shapes
             print(f"Warning: Unexpected empty cell position {empty_cell} for object color {color}")
             continue

        # Place the 2x2 shape into the determined quadrant
        output_grid[target_r:target_r+2, target_c:target_c+2] = shape_2x2
            
    return output_grid.tolist() # Return as list of lists as per ARC standard