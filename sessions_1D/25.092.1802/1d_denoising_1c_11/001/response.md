```python
import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects composed of any single non-background color (color 0 / white) in the input grid using 4-way adjacency. Calculate the size (number of pixels) of each object. Find the object with the largest size. Create a new output grid of the same dimensions as the input, initially filled with the background color (0). Set the pixels in the output grid corresponding to the largest object's pixels to the color of that object. Return the resulting output grid. If no non-background objects are found, return the grid filled with background color. If multiple objects share the largest size, select the first one encountered during the search.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-background colors in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of objects, where each object is a dictionary
              containing 'color', 'pixels' (list of (r, c) tuples),
              and 'size'. Returns an empty list if no objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(rows):
        for c in range(cols):
            # If the cell is not background, not visited, start a search
            if grid[r, c] != background_color and not visited[r, c]:
                current_color = grid[r, c]
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True

                # Breadth-First Search (BFS) for contiguous pixels of the same color
                while q:
                    row, col = q.popleft()
                    current_object_pixels.append((row, col))

                    # Check 4 adjacent neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check boundaries and if the neighbor is valid
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and \
                           grid[nr, nc] == current_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Store the found object
                objects.append({
                    'color': current_color,
                    'pixels': current_object_pixels,
                    'size': len(current_object_pixels)
                })

    return objects

def transform(input_grid):
    """
    Transforms the input grid by keeping only the largest contiguous object
    of a non-background color and setting everything else to background (0).
    """
    # Convert input list of lists to numpy array if necessary
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    background_color = 0

    # Initialize the output grid filled with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Find all non-background objects in the input grid
    objects = find_objects(grid)

    # If no objects are found, return the background-filled grid
    if not objects:
        return output_grid.tolist() # Convert back to list of lists for ARC standard

    # Find the object with the maximum size
    # If there's a tie, max() will return the first one encountered
    largest_object = max(objects, key=lambda obj: obj['size'])

    # Draw the largest object onto the output grid
    object_color = largest_object['color']
    for r, c in largest_object['pixels']:
        output_grid[r, c] = object_color

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```