```python
import numpy as np
from collections import deque

"""
Identify all contiguous non-background (non-zero) objects in the input grid.
Calculate the size (pixel count) of each object.
Select the object with the largest size.
Determine the minimal bounding box (top row, bottom row, left column, right column) enclosing this largest object.
Extract the portion of the input grid defined by this bounding box.
Return the extracted subgrid as the output.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-zero color in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of objects. Each object is represented as a dictionary
              containing 'color' (int) and 'pixels' (set of (row, col) tuples).
              Returns an empty list if the grid has no non-zero pixels.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is non-background and not visited yet
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                current_object_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                current_object_pixels.add((r, c))

                # Breadth-First Search (BFS) to find connected pixels of the same color
                while q:
                    row, col = q.popleft()

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if neighbor is same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            current_object_pixels.add((nr, nc))
                            q.append((nr, nc))
                
                # Store the found object
                objects.append({'color': color, 'pixels': current_object_pixels})
                
    return objects

def get_bounding_box(pixels):
    """
    Calculates the minimal bounding box for a set of pixel coordinates.

    Args:
        pixels (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        tuple: (min_row, max_row, min_col, max_col)
               Returns None if the pixel set is empty.
    """
    if not pixels:
        return None
    
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    
    min_row = min(rows)
    max_row = max(rows)
    min_col = min(cols)
    max_col = max(cols)
    
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Finds the largest contiguous non-background object in the input grid,
    determines its bounding box, and extracts that region as the output grid.
    """
    # Convert input list of lists to numpy array for easier slicing
    grid = np.array(input_grid, dtype=int)
    
    # Find all non-background objects
    objects = find_objects(grid)
    
    # Handle cases with no non-background objects
    if not objects:
        # Depending on requirements, could return empty grid, original, etc.
        # Let's return a 1x1 white grid as a placeholder.
        return np.array([[0]], dtype=int) 

    # Find the largest object based on pixel count
    largest_object = max(objects, key=lambda obj: len(obj['pixels']))
    
    # Get the bounding box of the largest object
    min_row, max_row, min_col, max_col = get_bounding_box(largest_object['pixels'])
    
    # Extract the subgrid defined by the bounding box
    # Note: Slicing is exclusive of the end index, so add 1 to max indices
    output_grid = grid[min_row : max_row + 1, min_col : max_col + 1]
    
    return output_grid

```