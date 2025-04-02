import numpy as np
from collections import defaultdict

"""
Identify all contiguous groups of connected, non-white pixels (objects) in the input grid. 
Calculate the size (pixel count) for each object. 
Determine the minimum size among all objects. 
Identify all objects that have this minimum size. 
From this set of minimum-sized objects, select the one whose color has the highest numerical value. 
Return the color value of this selected object.
"""

def _find_objects(grid):
    """
    Finds all connected objects of the same non-white color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, each representing an object 
              with keys 'color' and 'size'.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if pixel is part of an object (non-white) and not yet visited
            if color != 0 and not visited[r, c]:
                size = 0
                object_color = color
                q = [(r, c)] # Queue for Breadth-First Search (BFS)
                visited[r, c] = True
                
                # Perform BFS to find all connected pixels of the same color
                while q:
                    row, col = q.pop(0)
                    size += 1
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check boundaries and if neighbor has the same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == object_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                objects.append({'color': object_color, 'size': size})
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid based on object size and color.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        int: The color value determined by the transformation rule.
    """
    # Find all objects in the grid
    objects = _find_objects(np.array(input_grid))

    # Handle cases with no objects (though unlikely based on examples)
    if not objects:
        # Decide on a default behavior, e.g., return 0 or raise error
        # For now, let's assume there's always at least one object
        # based on the training examples. If test cases violate this,
        # we might need to adjust.
        return 0 # Or perhaps raise ValueError("No objects found")

    # Calculate the minimum size among all objects
    min_size = min(obj['size'] for obj in objects)

    # Filter objects to keep only those with the minimum size
    min_size_objects = [obj for obj in objects if obj['size'] == min_size]

    # From the minimum-sized objects, find the one with the maximum color value
    # The max function with a key sorts by color if sizes are equal (which they are here)
    # or picks the highest color if there's only one min-sized object.
    result_object = max(min_size_objects, key=lambda obj: obj['color'])

    # Return the color of the selected object
    return result_object['color']
