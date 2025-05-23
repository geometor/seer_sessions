# 1-3aa6fb7a • 003 • example_2 - NLP

---

**input**
```
0 0 0 0 0 0 0
0 8 0 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x71EE31D39F30>

**output**
```
0 0 0 0 0 0 0
0 8 1 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x71EE31D3A950>
Okay, let's analyze the transformation between the input and output grids.

**YAML Summary of Observations**

```yaml
input_grid:
  objects:
    - color: 8 (azure)
      shape: L-shape (2x2 block with one cell removed)
      positions: [[1,1], [2,1], [2,2]]
    - color: 8 (azure)
      shape: L-shape (inverted)
      positions: [[3,4], [3,5], [4,5]]
  grid_size: [7, 7]

output_grid:
  objects:
    - color: 8 (azure)
      shape: L-shape
      positions: [[1,1], [2,1], [2,2]]
    - color: 8 (azure)
      shape: L-shape (inverted)
      positions: [[3,4], [3,5], [4,5]]
    - color: 1 (blue)
      shape: single cell
      positions: [[1,2], [4,4]]
  grid_size: [7, 7]

```

**Natural Language Program: Step-by-Step Transformation**

1.  **Identify Objects:** In the input grid, we observe two distinct L-shaped objects, both of color 8 (azure).

2.  **Detect Change**: The first object made of 8 is at position (1,1), and the second is at (3,4). The target cell to change is the cell next to the top right corner of the L-shape.

3.  **Action - Single Cell Replacement:** Select the cell to the top-right of each L-shape with value 0.

4.  **Coloring:** Change the color of the identified cell from 0 (white) to 1 (blue).

5. **Preservation of other objects:** the L-shape objects with color 8 should be preserved.

**Summary of the rule**

The transformation rule identifies azure L-shaped (3 cells) objects within the grid. For each of those objects, it locates a cell on its top-right corner and colors it in blue. Other cells are kept unchanged.

```python
"""
The transformation rule identifies azure L-shaped (3 cells) objects within the grid. For each of those objects, it locates a cell on its top-right corner and colors it in blue. Other cells are kept unchanged.
"""

import numpy as np

def find_l_shapes(grid, color):
    """
    Finds L-shaped objects of a specified color in the grid.
    Returns a list of coordinate tuples, each representing an L-shape.  
    An L shape is defined by these relative coordinates:
      (0,0) (1,0)
            (1,1)
      and rotations.
    Each coordinate returned contains the "corner" of the L.
    """
    
    l_shapes = []
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            # Check for the four possible L-shape orientations
            if grid[r, c] == color and grid[r + 1, c] == color and grid[r + 1, c + 1] == color:
                l_shapes.append((r, c))  # Top-left corner
            if grid[r, c] == color and grid[r, c+1] == color and grid[r+1, c] == color:
                l_shapes.append((r,c))
            if grid[r, c+1] == color and grid[r+1, c+1] == color and grid[r+1, c] == color:
                l_shapes.append((r,c))
            if grid[r, c] == color and grid[r, c + 1] == color and grid[r + 1, c + 1] == color:
                l_shapes.append((r, c))  # Top-left corner

    return l_shapes

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    Find azure L-shapes, and change the color of cell adjacent to its top-right to blue.
    """
    output_grid = np.copy(input_grid)
    l_shapes = find_l_shapes(input_grid, 8)

    for r, c in l_shapes:
      # determine the orientation and find the top-right corner
      if input_grid[r,c] == 8 and input_grid[r+1,c] == 8 and input_grid[r+1,c+1] == 8: # original orientation
        # change top-right cell to blue if it is white
        if r < input_grid.shape[0] -1 and c < input_grid.shape[1] -2 and input_grid[r,c+2] == 0:
          output_grid[r,c+2] = 1
      if input_grid[r,c] == 8 and input_grid[r,c+1] == 8 and input_grid[r+1,c] == 8: # 90 degree
        if r > 0  and c < input_grid.shape[1] -1 and input_grid[r-1,c] == 0:
          output_grid[r-1,c] = 1

      if input_grid[r,c+1] == 8 and input_grid[r+1,c] == 8 and input_grid[r+1,c+1] == 8: #270 degree
        if r < input_grid.shape[0] -1 and c >0 and input_grid[r+1,c-1] == 0:
          output_grid[r+1,c-1] = 1
      if input_grid[r,c] == 8 and input_grid[r,c+1] == 8 and input_grid[r+1,c+1] == 8: # 180 degree
        if c < input_grid.shape[1] - 1 and r < input_grid.shape[0] -2 and input_grid[r+2,c+1] == 0:
          output_grid[r+2,c+1] = 1
      
    return output_grid
```

**input**
```
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 8 0 0 0 0
0 0 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 8 0 0
0 0 0 8 8 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x71EE31D204F0>

**output**
```
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 8 1 0 0 0
0 0 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 1 8 0 0
0 0 0 8 8 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x71EE31D20D60>
**Instructions**

- Describe in natural language the step-by-step transformation observed between the input and output grids.
- Focus on identifying objects, their properties (predicates), and the actions performed on them.
- Be as clear and concise as possible, providing a complete description of the transformation rule.
