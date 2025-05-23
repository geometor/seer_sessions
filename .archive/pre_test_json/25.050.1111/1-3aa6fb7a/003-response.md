# 1-3aa6fb7a • 003 • example_2 - NLP

---
Okay, let's analyze the second example.

**YAML Description of Observations**

```yaml
input_grid:
  objects:
    - color: 8 (azure)
      shape: three L-shaped structures and one single cell
      positions:
        - top-left corner of the first 'L': (0, 4)
        - top-left corner of the second 'L': (2, 2)
        - top-left corner of the third 'L': (6,3)
        - single cell: (5,5)
    - color: 0 (white)
      shape: background
      positions:
        - all other cells

output_grid:
  objects:
    - color: 8 (azure)
      shape: three L-shaped structures and one single cell
      positions:
        - top-left corner of the first 'L': (0, 4)
        - top-left corner of the second 'L': (2, 2)
        - top-left corner of the third 'L': (6,3)
        - single cell: (5,5) # assuming single cells persist

    - color: 1 (blue)
      shape: single cells
      positions:
        - (1, 4)
        - (2, 3)
        - (5,3)
    - color: 0 (white)
      shape: background
      positions:
        - all other cells
```

**Natural Language Program: Step-by-Step Transformation**

1.  **Identify Objects:** In the input grid, we see three distinct "L"-shaped objects and one single cell, all of color 8 (azure), against a background of color 0 (white).

2.  **Transformation Rule:** The transformation places a blue cell (color 1) next to specific parts of the azure L-shapes and single azure cell.
    *   For all L shaped objects we change to 1(blue) the cell adjacent to the right or on top of the uppermost-leftmost cell. If the azure cell right next to the uppermost-leftmost is out of the grid, the cell on top is chosen.

3. **Apply Transformation**

**Transformation Rule Summary**
The azure color 8 objects are preserved. A blue (1) cell is placed on top or at the right of uppermost and leftmost azure cell, in each azure L-shaped object. If placing to the right is not within bounds, placing on top is selected.

```python
"""
The azure color 8 objects are preserved. A blue (1) cell is placed on top or at the right of uppermost and leftmost azure cell, in each azure L-shaped object. If placing to the right is not within bounds, placing on top is selected.
"""

import numpy as np

def find_top_left_cell(grid, color):
    """Finds the uppermost and leftmost cell of a given color."""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    min_row_index = np.argmin(rows)
    min_col_index = np.argmin(cols)

    min_row = rows[min_row_index]
    indices = np.where(rows == min_row)[0]
    min_col = cols[indices[np.argmin(cols[indices])]]
    return min_row, min_col

def find_bottom_most_cell(grid, color):
    """Finds the bottom-most cell of given color"""
    rows, cols = np.where(grid == color)
    if len(rows) == 0:
        return None
    max_row_index = np.argmax(rows)

    max_row = rows[max_row_index]
    return max_row

def get_l_objects(grid,color):
    """ Get all separated L shaped objects """
    objects = []
    visited = set()
    rows, cols = grid.shape
    
    def is_valid(r,c):
        return 0 <= r < rows and 0 <= c < cols
    
    def dfs(r,c, current_object):
        if (r,c) in visited or not is_valid(r,c) or grid[r,c] != color:
            return
        visited.add((r,c))
        current_object.append((r,c))
        
        dfs(r+1,c,current_object)
        dfs(r-1,c,current_object)
        dfs(r,c+1, current_object)
        dfs(r,c-1,current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == color and (r,c) not in visited:
                current_object = []
                dfs(r,c,current_object)
                objects.append(current_object)
    return objects
        

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    objects = get_l_objects(input_grid,8)
    
    for obj in objects:

    # Find top-left of first L
        obj_rows = [r for r, _ in obj]
        obj_cols = [c for _, c in obj]

        min_row_index = np.argmin(obj_rows)
        min_row = obj_rows[min_row_index]

        indices = np.where(np.array(obj_rows) == min_row)[0]
        min_col = obj_cols[indices[np.argmin(np.array(obj_cols)[indices])]]
        top_left = (min_row, min_col)
      # Place blue cell to the right of the top-left of the first L
        if top_left[1] + 1 < output_grid.shape[1]:
          output_grid[top_left[0], top_left[1] + 1] = 1
        elif top_left[0] -1 >= 0:
          output_grid[top_left[0]-1,top_left[1]] = 1

    return output_grid
```

