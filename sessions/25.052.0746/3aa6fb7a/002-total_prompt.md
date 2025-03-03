# 1-3aa6fb7a • 002 • example_1 - CODE

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

![Image](001-example_1_input.png)


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

![Image](001-example_1_output.png)

Okay, let's analyze the transformation between the input and output grids.

**YAML Summary of Observations**

```yaml
task: 001-example_1
input_grid_size: 7x7
output_grid_size: 7x7
objects:
  - color: 8 (azure)
    instances:
      - shape: L-shape (2x2 block with one cell removed)
        position: (1,1) - (2,2)
      - shape: Reverse L-shape (2x2 block with one cell removed)
        position: (3,4) - (4,5)
colors_count:
  0: 45
  8: 4
```

**Natural Language Description of the Transformation**

1.  **Identify Objects:** In the input grid, we can identify two distinct objects of color 8 (azure). One is an "L" shape in the top-left corner, created from the top-left corner of a 2x2 block with one square removed. The other object is a mirrored "L" shape in the bottom-right corner made from the bottom-right corner of a 2x2 block, with one square removed.

2.  **Detect Change:** We find a change in the color from '8' to '1' in 2 positions in the grid.

3.  **Transformation rule:** Change to '1' (blue) the color of cell at the right of the top-left corner object. Do the same to the cell at the left of the second object at the bottom-right.

**Step-by-step explanation**
1. The code iterates through the all the input matrix
2. When a cell of color '8' is found, it checks if the cell is the right-most cell of an "L" object and if the cell at its right exists and is '0'. Then changes the color of the cell on its right to '1'.
3.  Also it checks if a cell is the left-most cell of a mirrored "L" and the cell at its left exists and is '0'. If this condition is met, the cell inmediately at the left is changed to color '1'.

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
