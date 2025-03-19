# d0f5fe59 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Azure Objects:** Locate all distinct azure (8) colored objects within the input grid. A distinct object is defined as a contiguous block of azure pixels.

2.  **Determine Object Corners/Extremities:** From the set of input images, we can see a "staircase pattern" of the azure objects.

3. **Create Output Grid:** Create a new grid with a number of rows equal to number of rows where at least one distinct object in the original object is present in the "staircase" and a number of columns equals to the number of columns that contain an object in the original "staircase".

4.  **Populate Output Grid:** Starting from the top left, create azure colored pixels in the correct relative position.
    - row 1 corresponds to the first row where a distinct azure object appears, following the staircase pattern
    - column 1 correspond to the first column where a distinct azure object appears following the staircase pattern

In other words, the output grid represents the relative diagonal positions of the azure objects by a single azure pixel, essentially creating a "diagonal" representation of the objects.
"""

import numpy as np

def find_objects(grid):
    """
    Finds distinct objects (contiguous blocks of non-zero pixels) in a grid.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_object):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] == 0:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule.
    """
    # Find distinct azure objects
    azure_objects = find_objects(np.array(input_grid))

    # Determine rows and cols for "staircase"
    rows_with_objects = set()
    cols_with_objects = set()

    for obj in azure_objects:
        for r, c in obj:
           rows_with_objects.add(r)
           cols_with_objects.add(c)

    rows_with_objects = sorted(list(rows_with_objects))
    cols_with_objects = sorted(list(cols_with_objects))
   
    # Build mapping based on row and column indices
    row_map = {rows_with_objects[i]: i for i in range(len(rows_with_objects))}
    col_map = {cols_with_objects[i]: i for i in range(len(cols_with_objects))}


    # Create output grid
    output_grid_rows = len(rows_with_objects)
    output_grid_cols = len(cols_with_objects)

    output_grid = np.zeros((output_grid_rows, output_grid_cols), dtype=int)


    # Populate output grid based on relative positions
    for obj in azure_objects:
      # determine object "corner"
      first_row = min([r for r, c in obj])
      first_col = min([c for r,c in obj])

      # find place in output
      output_row = row_map[first_row]
      output_col = col_map[first_col]

      output_grid[output_row, output_col] = 8
      

    return output_grid.tolist()
```
