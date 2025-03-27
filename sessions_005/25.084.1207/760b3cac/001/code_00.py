import numpy as np
from collections import deque

"""
Identifies the azure (8) object in the input grid.
Determines the bounding box of the azure object.
Calculates the center column index within the bounding box: `center_col_in_bbox = min_col + floor((max_col - min_col) / 2)`.
Checks the color of the pixel at the bottom-center position of the bounding box: `(max_row, center_col_in_bbox)`.
If this pixel is azure (8), the transformation reflects the azure object horizontally across the vertical line immediately to the right of its bounding box (axis x = max_col + 0.5).
If this pixel is not azure (e.g., white 0), the transformation reflects the azure object horizontally across the vertical line immediately to the left of its bounding box (axis x = min_col - 0.5).
The reflected azure pixels are added to the grid. The original azure object and all other elements (like the yellow object) remain unchanged.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid.
    Uses Breadth-First Search (BFS).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_coords.append((curr_r, curr_c))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if current_object_coords:
                    objects.append(current_object_coords)
                    
    return objects

def get_bounding_box(object_coords):
    """Calculates the bounding box (min_row, max_row, min_col, max_col) for a list of coordinates."""
    if not object_coords:
        return None
    
    rows = [r for r, c in object_coords]
    cols = [c for r, c in object_coords]
    
    min_row = min(rows)
    max_row = max(rows)
    min_col = min(cols)
    max_col = max(cols)
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Transforms the input grid by reflecting the azure object based on a specific rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    azure_color = 8

    # Find azure objects
    azure_objects = find_objects(input_grid, azure_color)

    # Assuming there is only one azure object per grid based on examples
    if not azure_objects:
        return output_grid # No azure object found, return original grid
        
    azure_object_coords = azure_objects[0]
    
    # Get the bounding box
    bbox = get_bounding_box(azure_object_coords)
    if bbox is None:
         return output_grid # Should not happen if azure_objects is not empty

    min_row, max_row, min_col, max_col = bbox

    # Determine the center column within the bounding box
    # Using integer division //
    center_col_in_bbox = min_col + (max_col - min_col) // 2 
    
    # Check the pixel at the bottom-center of the bounding box
    reflect_right = False
    # Ensure the calculated center column is within grid bounds (should be, but good practice)
    if 0 <= max_row < rows and 0 <= center_col_in_bbox < cols:
         if input_grid[max_row, center_col_in_bbox] == azure_color:
             reflect_right = True

    # Perform reflection based on the check
    for r, c in azure_object_coords:
        reflected_r = r
        if reflect_right:
            # Reflect across axis x = max_col + 0.5
            # Formula: reflected_col = max_col + (max_col - c) + 1 = 2 * max_col - c + 1
            reflected_c = 2 * max_col - c + 1
        else:
            # Reflect across axis x = min_col - 0.5
            # Formula: reflected_col = min_col - (c - min_col) - 1 = 2 * min_col - c - 1
            reflected_c = 2 * min_col - c - 1

        # Check if the reflected coordinates are within the grid bounds
        if 0 <= reflected_r < rows and 0 <= reflected_c < cols:
            # Add the reflected pixel to the output grid
            output_grid[reflected_r, reflected_c] = azure_color

    return output_grid