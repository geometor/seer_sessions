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

<PIL.Image.Image image mode=RGB size=448x448 at 0x7AF8A4D0DC60>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x7AF8A4D0D000>

*text:*
Okay, let's analyze the transformation between the input and output grids.

**YAML Description of Observations**

```yaml
input_grid:
  objects:
    - color: 8 (azure)
      positions: [(1,1), (2,1), (2,2), (4,4), (4,5), (5,4)]
      shape: "Two L-shaped objects"
  dimensions: [7, 7]

output_grid:
  objects:
    - color: 8 (azure)
      positions: [(1,1), (2,1), (2,2), (4,4), (4,5), (5,4)]
      shape: "Two L-shaped objects"
    - color: 1 (blue)
      positions: [(1,2), (5,3)]
      shape: "Two single-cell objects"
  dimensions: [7, 7]
```

**Natural Language Program: Step-by-Step Transformation**

1.  **Identify Objects:** In the input grid, we can observe two L-shaped objects composed of azure (color 8) pixels.

2.  **Detect Changed Pixels**
    - Find pixels on the right side of the top-left azure L. Change the color of the pixel to blue (color 1).
    - Find pixels on the left side of the down-right azure L. Change the color of the pixel to blue (color 1).

3.  **Construct Output:** The output grid retains all azure colored pixels, except the specified two pixels which become blue.

**Elaborated Description of the Rule**

The transformation rule preserves most of the azure pixels, and adding two blue pixels, each one at specific relative positions related with the two initial L-shaped objects.


*text:*
```python
"""
The transformation rule preserves most of the azure pixels, and adds two blue pixels, each one at specific relative positions related with the two initial L-shaped objects.
Specifically, one blue pixel is placed to the immediate right of the top-left L-shaped object, and another blue pixel is placed to the immediate left of the bottom-right L-shaped object.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous regions of the specified color in the grid.
    Returns a list of coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
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
def get_l_shapes(objects):
    """
    Filter the identified L shapes.
    """
    l_shapes = []

    for obj in objects:
        if len(obj) == 3:
           #check if it is a L shape
           obj.sort()
           if (obj[0][0] == obj[1][0] and obj[1][0] == obj[2][0]-1 and obj[1][1] == obj[2][1] )  or \
              (obj[0][1] == obj[1][1] and obj[1][1] == obj[2][1]-1 and obj[1][0] == obj[2][0] )  :
                l_shapes.append(obj)

    return l_shapes
def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    azure_objects = find_objects(input_grid, 8)
    l_shapes = get_l_shapes(azure_objects)

    #Change pixels for the first 2 detected L shapes
    if len(l_shapes) >=2:

        #first L shape
        obj = l_shapes[0]
        obj.sort()
        if obj[0][0] == obj[1][0]: #vertical L
            output_grid[ obj[1][0]  , obj[1][1]+1 ] = 1
        else: #horizontal L
            output_grid[ obj[1][0]+1 , obj[1][1] ] = 1
        
        #second L shape
        obj = l_shapes[1]
        obj.sort()

        if obj[0][0] == obj[1][0]:#vertical L
            output_grid[obj[0][0] , obj[0][1]-1 ] = 1
        else: #horizontal L
            output_grid[ obj[0][0]-1 , obj[0][1] ] = 1
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

<PIL.Image.Image image mode=RGB size=448x448 at 0x7AF8A4D0DC00>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x7AF8A4D0D600>

*text:*
Okay, let's analyze the second example of the transformation between the input and output grids.

**YAML Description of Observations**

```yaml
input_grid:
  objects:
    - color: 8 (azure)
      positions: [(0,4), (0,5), (1,5), (2,2), (3,2), (3,3), (5,4), (6,3),(6,4)]
      shape: "Three L-shaped objects"
  dimensions: [7, 7]

output_grid:
  objects:
    - color: 8 (azure)
      positions:  [(0,4), (0,5), (1,5), (2,2), (3,2), (3,3), (5,4), (6,3),(6,4)]
      shape: "Three L-shaped objects"
    - color: 1 (blue)
      positions: [(1,4), (2,3), (5,3)]
      shape: "Three single-cell objects"
  dimensions: [7, 7]
```

**Natural Language Program: Step-by-Step Transformation**

1.  **Identify Objects:** In the input grid, we can observe three L-shaped objects composed of azure (color 8) pixels.

2.  **Detect Changed Pixels**
    - Find pixels on the left side of the top-right azure L. Change the color of the pixel to blue (color 1).
    - Find pixels on the left side of the middle-left azure L. Change the color of the pixel to blue (color 1).
     - Find pixels on the up side of the down-left azure L. Change the color of the pixel to blue (color 1).

3.  **Construct Output:** The output grid retains all azure colored pixels, except the specified three pixels which become blue.

**Elaborated Description of the Rule**

The transformation rule preserves most of the azure pixels, and adding three blue pixels, each one at specific relative positions related with the three initial L-shaped objects.

```python
"""
The transformation rule preserves most of the azure pixels, and adds three blue pixels, each one at specific relative positions related with the three initial L-shaped objects.
Specifically:
- one blue pixel is placed to the immediate left of the top-right L-shaped object.
- one blue pixel is placed to the immediate left of the middle-left L-shaped object.
- one blue pixel is placed to the immediate up of the bottom-left L-shaped object.
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous regions of the specified color in the grid.
    Returns a list of coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
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
def get_l_shapes(objects):
    """
    Filter the identified L shapes.
    """
    l_shapes = []

    for obj in objects:
        if len(obj) == 3:
           #check if it is a L shape
           obj.sort()
           if (obj[0][0] == obj[1][0] and obj[1][0] == obj[2][0]-1 and obj[1][1] == obj[2][1] )  or \
              (obj[0][1] == obj[1][1] and obj[1][1] == obj[2][1]-1 and obj[1][0] == obj[2][0] )  :
                l_shapes.append(obj)

    return l_shapes
def transform(input_grid):
    """
    Transforms the input grid according to the observed rule.
    """
    output_grid = np.copy(input_grid)
    azure_objects = find_objects(input_grid, 8)
    l_shapes = get_l_shapes(azure_objects)

    #Change pixels for the first 3 detected L shapes
    if len(l_shapes) >=3:

        #first L shape
        obj = l_shapes[0]
        obj.sort()
        if obj[0][0] == obj[1][0]: #vertical L
            output_grid[ obj[0][0]  , obj[0][1]-1 ] = 1
        else: #horizontal L
            output_grid[ obj[0][0]-1 , obj[0][1] ] = 1
        
        #second L shape
        obj = l_shapes[1]
        obj.sort()

        if obj[0][0] == obj[1][0]:#vertical L
            output_grid[obj[0][0] , obj[0][1]-1 ] = 1
        else: #horizontal L
            output_grid[ obj[0][0]-1 , obj[0][1] ] = 1

        #third L shape
        obj = l_shapes[2]
        obj.sort()

        if obj[0][0] == obj[1][0]:#vertical L
            output_grid[obj[1][0]-1 , obj[1][1] ] = 1
        else: #horizontal L
            output_grid[ obj[1][0] , obj[1][1]-1 ] = 1
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
