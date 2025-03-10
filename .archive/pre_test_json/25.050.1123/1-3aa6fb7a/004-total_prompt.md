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

<PIL.Image.Image image mode=RGB size=448x448 at 0x766F27D36230>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x766F27D36A70>
Okay, let's analyze the transformation between the input and output grids.

**YAML Description**

```yaml
input_grid:
  objects:
    - color: 8
      positions: [(1, 1), (2, 1), (2, 2), (4, 4), (4, 5), (5,4)]
      shape: "Two separate L shapes"
  background_color: 0

output_grid:
  objects:
    - color: 8
      positions: [(1, 1), (2, 1), (2, 2), (4, 4), (4, 5), (5,4)]
      shape: "Two separate L shapes"
    - color: 1
      positions: [(1,2), (5,4)]
      shape: "single pixels inside the L shapes"
  background_color: 0
```

**Natural Language Program**

1.  **Identify Objects:** In the input grid, we observe two distinct "L" shaped objects formed by the color 8 (azure).

2.  **Locate Insertion Points:** In both azure L shapes there is one pixel with color 0 bordered by two sides by azure pixels.

3. **Color Changing**: For each detected "L", a color 1 (blue) dot is placed in a location that is inside the L, one cell down and one cell to the right from the top-left pixel, and respectively, one cell up of the bottom-right pixel.

**Step-by-step transformation description**
The input azure L shapes are preserved. Two blue pixels are added inside the azure shapes.

```python
"""
The input azure L shapes are preserved. Two blue pixels are added inside the azure shapes,
one cell down and one cell to the right from the top-left pixel of the "L" shape, 
and respectively, one cell up of the bottom-right pixel.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the given color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def find_l_shapes(obj):
    #rule to detect 2x2 L shapes from the object
    if len(obj) != 3: return []
    obj.sort()
    if (obj[1][0] == obj[0][0]+1 and obj[1][1] == obj[0][1] and
        obj[2][0] == obj[1][0] and obj[2][1] == obj[1][1]+1) or \
       (obj[1][0] == obj[0][0] and obj[1][1] == obj[0][1]+1 and
        obj[2][0] == obj[1][0]+1 and obj[2][1] == obj[1][1]):
            return obj
    else: return []

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find objects of color 8 (azure)
    azure_objects = find_objects(input_grid, 8)
    
    #detect L shapes
    l_shapes = []
    for obj in azure_objects:
      l = find_l_shapes(obj)
      if len(l) > 0: l_shapes.append(l)

    # Place blue (1) pixels inside detected "L" shapes
    for l_shape in l_shapes:
        #get coordinates
        l_shape.sort()
        #check the orientation and set the insertion point
        if l_shape[1][0] > l_shape[0][0]:
          output_grid[l_shape[0][0] + 1, l_shape[0][1] + 1] = 1
        else:
          output_grid[l_shape[2][0] -1, l_shape[2][1]-1] = 1  
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

<PIL.Image.Image image mode=RGB size=448x448 at 0x766F27D21360>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x766F27D213F0>
Okay, let's analyze the second example provided.

**YAML Description**

```yaml
input_grid:
  objects:
    - color: 8
      positions: [(0, 4), (0, 5), (1, 5), (2, 2), (3, 2), (3, 3), (5,4), (6,4), (6,5)]
      shape: "Three separate L shapes"
  background_color: 0

output_grid:
  objects:
    - color: 8
      positions:  [(0, 4), (0, 5), (1, 5), (2, 2), (3, 2), (3, 3), (5,4), (6,4), (6,5)]
      shape: "Three separate L shapes"
    - color: 1
      positions: [(1, 4), (2, 3), (5,3)]
      shape: "single pixels inside the L shapes"
  background_color: 0
```

**Natural Language Program**

1.  **Identify Objects:** The input grid contains three distinct "L" shaped objects of color 8 (azure).

2.  **Locate Insertion Points:** Similar to the previous example, we look for the "inner corner" of each "L" shape.

3.  **Color Changing:** Within each "L" shape, place a color 1 (blue) pixel at the inner corner of L.

**Step-by-step transformation description**
The input azure L shapes are preserved. Three blue pixels are added inside the azure shapes at locations that depend on the shape orientation.

The python implementation is the same.
```python
"""
The input azure L shapes are preserved. Two blue pixels are added inside the azure shapes,
one cell down and one cell to the right from the top-left pixel of the "L" shape, 
and respectively, one cell up of the bottom-right pixel.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous regions of the given color
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def find_l_shapes(obj):
    #rule to detect 2x2 L shapes from the object
    if len(obj) != 3: return []
    obj.sort()
    if (obj[1][0] == obj[0][0]+1 and obj[1][1] == obj[0][1] and
        obj[2][0] == obj[1][0] and obj[2][1] == obj[1][1]+1) or \
       (obj[1][0] == obj[0][0] and obj[1][1] == obj[0][1]+1 and
        obj[2][0] == obj[1][0]+1 and obj[2][1] == obj[1][1]):
            return obj
    else: return []

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find objects of color 8 (azure)
    azure_objects = find_objects(input_grid, 8)
    
    #detect L shapes
    l_shapes = []
    for obj in azure_objects:
      l = find_l_shapes(obj)
      if len(l) > 0: l_shapes.append(l)

    # Place blue (1) pixels inside detected "L" shapes
    for l_shape in l_shapes:
        #get coordinates
        l_shape.sort()
        #check the orientation and set the insertion point
        if l_shape[1][0] > l_shape[0][0]:
          output_grid[l_shape[0][0] + 1, l_shape[0][1] + 1] = 1
        else:
          output_grid[l_shape[2][0] -1, l_shape[2][1]-1] = 1  
    return output_grid
```

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
