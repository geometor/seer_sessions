# 1-3aa6fb7a • 004 • example_2 - CODE

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x78CDEFF12EC0>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x78CDEFF12740>

*text:*
Okay, let's analyze the transformation between the input and output grids.

**YAML Description**

```yaml
observations:
  input_grid:
    objects:
      - color: 8
        shape: two separate 2x1 vertical shapes and one 1x2 horizontal shape.
        positions: 
          - (1,1) and (2,1) # top-left azure region
          - (3,5) and (4,5) # bottom-right azure region. The separate single azure is on (4,4)
        
      - color: 0
        shape: background
        positions: fills the remaining cells

  output_grid:
    objects:
      - color: 8
        shape: same as input.
        positions: 
          - (1,1) and (2,1)
          - (3,5) and (4,5)
      - color: 1
        shape: single cell
        positions:
          - (1,2) # top-left azure region replaced with 1
          - (4,4) # bottom right azure region replaced with 1
      - color: 0
        shape: background
        positions: fills the remaining cells
```

**Natural Language Program: Step-by-Step Transformation**

1.  **Identify Objects:** In the input grid, we have two separate regions of color `8` (azure). One is the vertical shape of size two composed by stacked azure cells on the second column. The second element is an horizontal shape composed by two azure cells side by side on the fifth column. There is a separate single azure cell on (4,4).

2.  **Predicate:** Select one azure object with only one cell. If it is not unique, then iterate.

3.  **Action, Change Color:** Change the color of the top cell of the vertical object from `8` to `1` (blue) and change the color of the left cell of the horizontal object from `8` to `1`.

In summary, two azure cells, top and left on each azure shape, were replaced by blue cells.


*text:*
```python
"""
The transformation rule identifies separate regions of color '8' (azure) in the input grid. 
It changes the color of the top cell of the 2x1 vertical azure shapes and the left cell of the 1x2 horizontal shape from '8' to '1' (blue).
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous regions of the specified color in the grid.
    Returns a list of tuples, where each tuple contains the coordinates of cells in an object.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))

        # Check adjacent cells (up, down, left, right)
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the rule:
    - Find azure (color 8) objects.
    - Change the top cell of vertical 2x1 shapes to blue (color 1).
    - Change the left cell of horizontal 1x2 shapes to blue (color 1).
    """
    output_grid = np.copy(input_grid)
    azure_objects = find_objects(input_grid, 8)

    for obj in azure_objects:
        # Sort the object coordinates by row and column
        sorted_obj = sorted(obj, key=lambda x: (x[0], x[1]))

        # Check for 2x1 vertical shape
        
        if len(sorted_obj) == 2 :
            #check if it's vertical
            if sorted_obj[0][1] == sorted_obj[1][1]:
                output_grid[sorted_obj[0]] = 1  # Change top cell to blue
            else:
                output_grid[sorted_obj[0]] = 1  # Change left cell to blue
            

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x78CDEFF12E60>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x78CDEFF12560>

*text:*
Okay, let's analyze the second example transformation.

**YAML Description**

```yaml
observations:
  input_grid:
    objects:
      - color: 8
        shape:  two 2x1 vertical shapes, and two 1x2 horizontal shapes.
        positions:
          - (0,4) and (0,5) #top horizontal shape
          - (1,5) and (2,5) # right vertical shape
          - (2,2) and (3,2) # left vertical shape
          - (6,3) and (6,4) # down horizontal shape
      - color: 0
        shape: background
        positions: fills the remaining cells

  output_grid:
    objects:
      - color: 8
        shape: same as input, but with some cells changed to color 1.
        positions:
          - (0,4) and (0,5)
          - (2,5) and (3,5)
          - (2,2) and (3,2)
          - (6,3) and (6,4)
      - color: 1
        shape: single cell replacements within the original azure shapes.
        positions:
          - (1,4) # top horizontal azure region, left is colored
          - (1,5) # right vertical azure region, top is colored
          - (5,3) # down azure horizontal region, left is colored
          - (2,3) # left vertical azure region, top is colored
      - color: 0
        shape: background
        positions: fills the remaining cells
```

**Natural Language Program: Step-by-Step Transformation**

1.  **Identify Objects:** The input grid contains azure (color 8) objects. They come in pairs of vertical or horizontal shapes.

2.  **Predicate:** Differentiate the two main shapes: 2x1 vertical and 1x2 horizontal.

3.  **Action, Change Color:** Within each azure shape, specific cells change color.
    *   For vertical shapes: The *top* cell changes from color 8 to 1.
    *   For horizontal shapes: The *left* cell changes from color 8 to 1.

In summary, the transformation identifies vertical and horizontal azure colored shapes. On the vertical shapes, the upper azure cell is replaced with a blue cell and on the horizontal shapes the left azure cell is replaced with a blue cell.

The natural language program and the python code are still valid.

**INSTRUCTIONS**

- generate a Python module to represent the natural language program 
- follow the template below
- all common math and science libraries are available
- create docstring only at top - but comment the workflow in the function
- use helper functions for common operations like finding objects, counting,
  measuring, moving, etc. 

remember - we are working iteratively - so this code will inform your future
self as we converge on the solution

*template:*

```python
"""
{ natural language description of the transformation rule }
"""

{ imports }

def transform(input_grid):
    # initialize output_grid

    # change output pixels 

    return output_grid

```
