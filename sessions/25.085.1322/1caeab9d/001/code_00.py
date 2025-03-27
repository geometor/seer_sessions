import numpy as np
from collections import deque

"""
Identify all distinct, contiguous, non-white rectangular objects in the input grid.
Determine the common height (obj_h) of these objects and the maximum row index (max_obj_row) occupied by any object pixel.
Calculate the target starting row (output_start_row) for the output assembly: base_start_row = max_obj_row - obj_h + 1. If the grid height (H_grid) is 5 or less, decrement the base_start_row by 1.
Sort the identified objects based on their leftmost column index (min_col) in ascending order.
Create an output grid of the same dimensions as the input, filled with the background color (white, 0).
Place the sorted objects horizontally adjacent to each other in the output grid, starting from column 0 and row output_start_row.
The color and shape of each object are preserved.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of the same non-background color in the grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'pixels' (list of (r, c) tuples),
              'min_row', 'max_row', 'min_col', 'max_col', 'height', 'width'.
              Returns an empty list if no objects are found.
    """
    objects = []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    background_color = 0

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'min_row': min_r,
                    'max_row': max_r,
                    'min_col': min_c,
                    'max_col': max_c,
                    'height': max_r - min_r + 1,
                    'width': max_c - min_c + 1
                })
    return objects

def transform(input_grid):
    """
    Transforms the input grid by identifying colored rectangular objects,
    sorting them left-to-right, and arranging them horizontally adjacent
    at a calculated vertical position in the output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize output_grid with the background color (white, 0)
    output_grid = np.zeros_like(input_np, dtype=int)

    # Find all non-white objects
    objects = find_objects(input_np)

    # If no objects are found, return the empty grid
    if not objects:
        return output_grid.tolist() # Convert back to list of lists

    # Assume all objects have the same height (as observed in examples)
    # Find the common height and the overall maximum row index
    obj_h = objects[0]['height'] # Get height from the first object
    max_obj_row = 0
    for obj in objects:
        max_obj_row = max(max_obj_row, obj['max_row'])
        # Optional: Add a check here if object heights are inconsistent

    # Determine the vertical placement (output_start_row)
    h_grid = height
    base_start_row = max_obj_row - obj_h + 1
    if h_grid <= 5:
        output_start_row = base_start_row - 1
    else:
        output_start_row = base_start_row

    # Ensure start row is not negative (edge case if objects are at the very top)
    output_start_row = max(0, output_start_row)

    # Sort objects based on their leftmost column (min_col)
    objects.sort(key=lambda obj: obj['min_col'])

    # Place sorted objects into the output grid
    current_col = 0
    for obj in objects:
        obj_color = obj['color']
        obj_width = obj['width']
        # Iterate through the pixels of the object relative to its own bounding box
        for r, c in obj['pixels']:
            # Calculate relative coordinates within the object's bounding box
            rel_r = r - obj['min_row']
            rel_c = c - obj['min_col']

            # Calculate target coordinates in the output grid
            target_r = output_start_row + rel_r
            target_c = current_col + rel_c

            # Place the pixel if within output grid bounds
            if 0 <= target_r < height and 0 <= target_c < width:
                output_grid[target_r, target_c] = obj_color
            # else: # Optional: handle cases where assembly might go out of bounds
                # print(f"Warning: Pixel placement out of bounds: ({target_r}, {target_c})")


        # Update the starting column for the next object
        current_col += obj_width

    # Convert the result back to a list of lists
    return output_grid.tolist()