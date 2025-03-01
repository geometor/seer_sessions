# 6aa20dc0 • 018 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate all connected components (clusters) of non-azure (8) colored pixels within the input grid.

2.  **Analyze Colored Pixels:** For each identified cluster, record the original positions of the colored pixels.

3.  **Replicate and Shift:**
     For each non-azure pixel in the original figure:
          Replicate that pixel, along with all non-azure pixels below and to the
		  right of that pixel in the input figure, in a new position, shifted
		  diagonally by a specific amount relative to its position in the original image. Specifically the
		  shift is down and to the right, and the amount is based on the original position
		  of the pixel in the original cluster in the input image.

4.  **Preserve Background:**  All azure (8) pixels in the input grid that are not replaced by the replicated objects remain unchanged in the output grid.
"""

import numpy as np

def find_objects(grid):
    """Finds connected components of non-azure pixels."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] == 8
        ):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)
        dfs(row + 1, col + 1, current_object)  # Diagonal
        dfs(row - 1, col - 1, current_object)  # Diagonal
        dfs(row + 1, col - 1, current_object)
        dfs(row -1, col + 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 8 and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # Initialize output grid with the same dimensions and background color
    output_grid = np.full_like(input_grid, 8)

    # Find the non-azure objects in the input grid
    objects = find_objects(input_grid)

    # we expect one object
    assert len(objects) == 1, f"expected one object, got: {len(objects)}, {objects}"
    object_pixels = objects[0]

    # iterate the object pixels
    for row, col in object_pixels:
        # shift the pixel down and to the right by its initial row, col
        color = input_grid[row,col]
        output_row = row + row
        output_col = col + col

        # copy to the new location
        if 0 <= output_row < output_grid.shape[0] and 0 <= output_col < output_grid.shape[1]:
            output_grid[output_row, output_col] = color

            # replicate to all positions down and right
            for r, c in object_pixels:
                if r >= row and c >= col:
                    orow = r + row
                    ocol = c + col
                    if 0 <= orow < output_grid.shape[0] and 0 <= ocol < output_grid.shape[1]:
                        output_grid[orow, ocol] = input_grid[r,c]

    return output_grid
```
