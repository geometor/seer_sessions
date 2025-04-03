```python
import numpy as np

"""
Recolors yellow objects based on their size.
- Identifies contiguous yellow (4) objects in the input grid.
- Counts the number of pixels (size) for each object.
- Recolors the object in the output grid based on its size:
    - Size 1 becomes maroon (9).
    - Size 2 becomes magenta (6).
    - Size 3 becomes red (2).
- Non-yellow pixels remain unchanged.
"""

def _find_object(grid, start_r, start_c, target_color, visited):
    """
    Finds all connected pixels of a target color starting from a seed point using BFS.

    Args:
        grid (np.ndarray): The input grid.
        start_r (int): Starting row index.
        start_c (int): Starting column index.
        target_color (int): The color of the object to find.
        visited (np.ndarray): A boolean grid to mark visited pixels across calls.

    Returns:
        set: A set of tuples representing the coordinates (row, col) of the object pixels.
             Returns an empty set if the start pixel is not the target color or already visited.
    """
    rows, cols = grid.shape
    if not (0 <= start_r < rows and 0 <= start_c < cols) or \
       visited[start_r, start_c] or \
       grid[start_r, start_c] != target_color:
        return set()

    obj_pixels = set()
    queue = [(start_r, start_c)]
    visited[start_r, start_c] = True # Mark as visited for the main loop

    while queue:
        r, c = queue.pop(0)
        obj_pixels.add((r, c))

        # Check neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               not visited[nr, nc] and \
               grid[nr, nc] == target_color:
                visited[nr, nc] = True # Mark as visited for the main loop
                queue.append((nr, nc))

    return obj_pixels

def transform(input_grid):
    """
    Transforms the input grid by recoloring yellow objects based on their size.

    Args:
        input_grid (np.ndarray): The 2D input grid.

    Returns:
        np.ndarray: The transformed 2D output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    
    # Keep track of pixels already processed as part of an object
    visited = np.zeros((rows, cols), dtype=bool)
    
    target_color = 4 # Yellow

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # If a pixel is yellow (4) and has not yet been processed
            if input_grid[r, c] == target_color and not visited[r, c]:
                # Identify the complete contiguous object
                object_pixels = _find_object(input_grid, r, c, target_color, visited)

                # If an object was found (should always be true if we enter here)
                if object_pixels:
                    # Count the size of the object
                    object_size = len(object_pixels)

                    # Determine the target color based on the object's size
                    new_color = -1 # Default/error value
                    if object_size == 1:
                        new_color = 9 # maroon
                    elif object_size == 2:
                        new_color = 6 # magenta
                    elif object_size == 3:
                        new_color = 2 # red
                    else:
                        # If size is not 1, 2, or 3, keep original color (optional rule)
                        # Or handle as an error, but based on examples, let's keep original color
                        new_color = target_color 

                    # Update the corresponding pixels in the output grid
                    if new_color != -1: # Only update if a valid size was found
                        for obj_r, obj_c in object_pixels:
                             # We already marked as visited in _find_object,
                             # now update the color in the output grid
                            output_grid[obj_r, obj_c] = new_color
            
            # If a pixel is not yellow or has already been visited, 
            # it retains its original value (already copied) or the updated color.

    return output_grid
```