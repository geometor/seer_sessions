"""
1.  **Identify the Gray Line:** Find the vertical column composed entirely of gray (5) pixels.

2.  **Locate Objects:** Identify all contiguous blocks of non-black, non-gray pixels to the *left* of the gray line.

3.  **Preserve based on Adjacency and Connectedness to object adjacent to the gray line:**
    *   Iterate through each object to the left of the gray line
    *   If the object contains any pixels adjacent to the gray line, keep *only* the connected component of pixels of that object which are connected to the part of the object adjacent to the gray line.
    *  If the object has no pixels adjacent, remove the whole object.

4.  **Construct Output:** Create a new grid with the same height as the input grid.

5. **Determine output width:** The output grid width is determined by the distance from column 0 to the gray line.

6. **Populate the Output Grid:** Copy the *preserved* parts of objects from the input grid to the output grid, maintaining their original row positions and column positions relative to the gray line.
"""

import numpy as np
from scipy.ndimage import label

def find_gray_line(grid):
    """Finds the vertical line of gray (5) pixels."""
    rows, cols = grid.shape
    for j in range(cols):
        is_gray_line = True
        for i in range(rows):
            if grid[i, j] != 5:
                is_gray_line = False
                break
        if is_gray_line:
            return j
    return -1  # Should not happen

def get_objects(grid, gray_line_col):
    """Identifies objects to the left of the gray line."""
    mask = (grid != 0) & (grid != 5)
    mask[:, gray_line_col:] = False  # Only consider pixels to the left
    labeled_array, num_features = label(mask)
    objects = []
    for i in range(1, num_features + 1):
        objects.append((labeled_array == i).astype(int))
    return objects

def is_adjacent_to_gray_line(object_mask, gray_line_col):
    """Checks if an object is adjacent to the gray line."""
    rows, cols = object_mask.shape
    for r in range(rows):
        for c in range(cols):
            if object_mask[r, c] == 1:
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and nc == gray_line_col:
                        return True
    return False

def get_connected_component(object_mask, gray_line_col):
    """
    Gets the connected component of an object that's adjacent to the gray
    line, by using a seed fill.
    """
    rows, cols = object_mask.shape
    seed_row, seed_col = -1, -1 # initialize

    # find the seed point in the object - adjacent to gray
    for r in range(rows):
        for c in range(cols):
            if object_mask[r,c] == 1:
                for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and nc == gray_line_col:
                        seed_row, seed_col = r, c
                        break
        if seed_row != -1:
            break

    # now flood fill
    if seed_row == -1:
        return np.zeros_like(object_mask)

    visited = np.zeros_like(object_mask)
    queue = [(seed_row, seed_col)]
    visited[seed_row, seed_col] = 1
    connected_component = np.zeros_like(object_mask)
    connected_component[seed_row, seed_col] = 1

    while queue:
      r, c = queue.pop(0)
      for dr, dc in [(0,1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            if object_mask[nr, nc] == 1 and visited[nr, nc] == 0:
                visited[nr,nc] = 1
                connected_component[nr, nc] = 1
                queue.append((nr, nc))
    return connected_component

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    gray_line_col = find_gray_line(input_grid)
    output_width = gray_line_col + 1 # output width
    output_grid = np.zeros((input_grid.shape[0], output_width), dtype=int)

    # get objects
    objects = get_objects(input_grid, gray_line_col)

    # iterate through located objects
    for obj_mask in objects:
        # preserve/remove based on rules
        if is_adjacent_to_gray_line(obj_mask, gray_line_col):
            preserved_component = get_connected_component(obj_mask, gray_line_col)

            # copy to output grid
            rows, cols = preserved_component.shape
            for r in range(rows):
                for c in range(cols):
                    if preserved_component[r,c] == 1:
                        output_grid[r,c] = input_grid[r,c]

    return output_grid.tolist()