import numpy as np
from collections import deque

"""
Identify all distinct contiguous objects of non-white pixels in the input grid.
Verify that exactly two such objects exist.
For each object, determine its topmost row index.
Select the object with the smaller topmost row index (the higher object).
Crop the selected object to its bounding box and return it as the output grid.
Pixels within the bounding box but not part of the object remain white (0).
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-white pixels in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              with keys 'color', 'pixels' (set of (r, c) tuples),
              'bbox' (min_row, min_col, max_row, max_col), and 'top_row'.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                # Found the start of a new object
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))

                    # Update bounding box and top row
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c),
                    'top_row': min_r
                })
    return objects

def crop_object(grid, obj):
    """
    Creates a new grid containing only the specified object,
    cropped to its bounding box.

    Args:
        grid (np.array): The original input grid (needed for pixel values).
        obj (dict): The object dictionary containing 'pixels' and 'bbox'.

    Returns:
        np.array: The cropped output grid.
    """
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    # Initialize output grid with background color (white)
    output_grid = np.zeros((height, width), dtype=int)

    # Copy object pixels to the output grid, adjusting coordinates
    for r, c in obj['pixels']:
        output_r = r - min_r
        output_c = c - min_c
        # Ensure coordinates are within the bounds of the new grid
        if 0 <= output_r < height and 0 <= output_c < width:
             output_grid[output_r, output_c] = grid[r, c] # Use original grid color

    return output_grid


def transform(input_grid):
    """
    Transforms the input grid according to the rule: find the highest
    of the two non-white objects and return it cropped to its bounding box.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)

    # Find all non-white objects in the grid
    objects = find_objects(grid_np)

    # Verify there are exactly two objects
    if len(objects) != 2:
        # This case shouldn't happen based on the examples, but good to handle
        # Returning an empty grid or raising an error could be options.
        # For now, let's return the input unchanged or an empty grid if undefined.
        print(f"Warning: Expected 2 objects, found {len(objects)}. Returning empty grid.")
        return [[]] # Or maybe return input_grid? Task description implies success case.

    # Find the object with the minimum top_row index (highest object)
    selected_object = min(objects, key=lambda obj: obj['top_row'])

    # Crop the selected object to its bounding box
    output_grid_np = crop_object(grid_np, selected_object)

    # Convert the output numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid