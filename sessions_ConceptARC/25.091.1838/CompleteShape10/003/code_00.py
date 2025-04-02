import numpy as np
from collections import deque

"""
Fill horizontal gaps within the row-wise extent of the main non-background object.

1. Identify the background color (assumed white/0).
2. Find the largest contiguous non-background object and its color (fill_color).
3. Iterate through each row of the grid.
4. For each row containing the object, find the minimum (min_col) and maximum (max_col) column index of the object's pixels.
5. Fill any background-colored pixels within that row between min_col and max_col (inclusive) with the fill_color.
"""

def _find_objects(grid, background_color):
    """
    Finds all contiguous objects of non-background colors using BFS.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color designated as background.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'pixels' (set of (r, c) tuples), and 'size'.
              Returns an empty list if no non-background objects are found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If it's a non-background pixel and not visited yet, start BFS
            if grid[r, c] != background_color and not visited[r, c]:
                obj_color = grid[r, c]
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    current_object_pixels.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == obj_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Add the found object to the list
                if current_object_pixels:
                    objects.append({
                        'color': obj_color,
                        'pixels': current_object_pixels,
                        'size': len(current_object_pixels)
                    })
                    
    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    # 1. Identify background color (assuming 0 based on examples)
    background_color = 0
    # Potential improvement: Calculate most frequent color if background isn't always 0
    # colors, counts = np.unique(input_np, return_counts=True)
    # background_color = colors[np.argmax(counts)]

    # 2. Find all non-background objects
    objects = _find_objects(input_np, background_color)

    # If no non-background objects, return the original grid
    if not objects:
        return output_grid.tolist() 

    # Find the largest object
    largest_object = max(objects, key=lambda obj: obj['size'])
    fill_color = largest_object['color']
    # Get just the coordinates for efficient lookup later if needed, but not strictly necessary for this approach
    # object_pixels_coords = largest_object['pixels'] 

    # 3. Iterate through each row
    for r in range(rows):
        # 4. Find column indices of the object's pixels in the current row
        row_pixels_indices = np.where(input_np[r, :] == fill_color)[0]

        # 5. If the object exists in this row
        if len(row_pixels_indices) > 0:
            # Find the horizontal extent (min and max columns)
            min_col = np.min(row_pixels_indices)
            max_col = np.max(row_pixels_indices)

            # 6. Fill background pixels within the horizontal extent
            for c in range(min_col, max_col + 1):
                if output_grid[r, c] == background_color:
                    output_grid[r, c] = fill_color

    # Convert the result back to list of lists format
    return output_grid.tolist()