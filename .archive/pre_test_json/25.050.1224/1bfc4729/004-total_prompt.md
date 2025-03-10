# 1bfc4729 • 004 • example_2 - CODE

---

**input**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x79CABAB79690>

**output**
```
6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 6
6 6 6 6 6 6 6 6 6 6
6 0 0 0 0 0 0 0 0 6
6 0 0 0 0 0 0 0 0 6
7 0 0 0 0 0 0 0 0 7
7 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7
7 0 0 0 0 0 0 0 0 7
7 7 7 7 7 7 7 7 7 7
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x79CABB63AA10>
Okay, let's analyze the transformation between the input and output grids.

**YAML Summary of Observations**

```yaml
input_objects:
  - color: 6 (magenta)
    position: (2, 2)
    shape: single cell
  - color: 7 (orange)
    position: (7, 7)
    shape: single cell
output_objects:
  - color: 6 (magenta)
    shape: 10x2 frame (top and bottom) and two 3x1 lines
  - color: 7 (orange)
      shape: 10x2 frame (top and bottom) and two 3x1 lines
```

**Natural Language Program: Step-by-step Transformation**

1.  **Identify Single Cells:** Locate all single-cell objects in the input grid. In this case, we find two: a magenta (6) cell at (2, 2) and an orange (7) cell at (7, 7).

2.  **Expand and frame based on color:**
    *   If the object is magenta (6), replicate it to top and bottom row. Then draw two lines, 3 cells down from the top, and 3 cells up from the bottom.
    *   If the object is orange (7), replicate it to top and bottom row. Then draw two lines, 3 cells down from the top, and 3 cells up from the bottom.

**Transformation Rule Summary**

The transformation rule involves taking each single-cell object in the input, and create frame and columns, depending on the original cell color.

```python
"""
The transformation rule involves taking each single-cell object in the input, 
and create frame and columns, depending on the original cell color.
If the object is magenta (6), replicate it to top and bottom row. 
Then draw two lines, 3 cells down from the top, and 3 cells up from the bottom.
If the object is orange (7), replicate it to top and bottom row. 
Then draw two lines, 3 cells down from the top, and 3 cells up from the bottom.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through the input grid to find single-cell objects
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] != 0:
                color = input_grid[r,c]

                # replicate color to top and bottom rows
                output_grid[0, :] = color
                output_grid[rows - 1, :] = color

                # draw vertical lines
                output_grid[r+1:r+4,0] = color
                output_grid[r+1:r+4,cols-1] = color

    return output_grid
```


**input**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x79CABB63BA60>

**output**
```
1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 1
1 1 1 1 1 1 1 1 1 1
1 0 0 0 0 0 0 0 0 1
1 0 0 0 0 0 0 0 0 1
4 0 0 0 0 0 0 0 0 4
4 0 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 4 4
4 0 0 0 0 0 0 0 0 4
4 4 4 4 4 4 4 4 4 4
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x79CABB63B6D0>
Okay, let's analyze the second example's transformation.

**YAML Summary of Observations**

```yaml
input_objects:
  - color: 1 (blue)
    position: (2, 6)
    shape: single cell
  - color: 4 (yellow)
    position: (7, 5)
    shape: single cell
output_objects:
  - color: 1 (blue)
    shape: 10x2 frame (top and bottom) and two 3x1 lines
  - color: 4 (yellow)
    shape: 10x2 frame (top and bottom) and two 3x1 lines
```

**Natural Language Program: Step-by-step Transformation**

1.  **Identify Single Cells:** Locate all single-cell objects in the input grid. In this case, we find two: a blue (1) cell at (2, 6) and a yellow (4) cell at (7, 5).

2.  **Expand and frame based on color:**
    *   If the object is blue (1), replicate it to top and bottom row. Then draw two lines, 3 cells down from the top, and 3 cells up from the bottom.
    *   If the object is yellow (4), replicate it to top and bottom row. Then draw two lines, 3 cells down from the top, and 3 cells up from the bottom.

**Transformation Rule Summary**

The transformation rule is consistent with the previous example.  It involves taking each single-cell object in the input, and create frame and columns, depending on the original cell color. The position of the identified single cell determines at what height we draw the vertical bars.

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
