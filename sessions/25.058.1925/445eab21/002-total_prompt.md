# 445eab21 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 7 7 7 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F218F4D0>

**output:**
```
8 8
8 8
```

<PIL.Image.Image image mode=RGB size=128x128 at 0x78E5F264F9D0>

## train_2

**input:**
```
6 6 6 6 6 0 0 0 0 0
6 0 0 0 6 0 0 0 0 0
6 0 0 0 6 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 0 0
0 0 7 0 0 0 0 7 0 0
0 0 7 0 0 0 0 7 0 0
0 0 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F20EF850>

**output:**
```
7 7
7 7
```

<PIL.Image.Image image mode=RGB size=128x128 at 0x78E5F218F350>

## train_3

**input:**
```
0 4 4 4 4 4 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 2 2 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F218F850>

**output:**
```
4 4
4 4
```

<PIL.Image.Image image mode=RGB size=128x128 at 0x78E5F218FED0>
<PIL.Image.Image image mode=RGB size=2000x818 at 0x78E5F214A9D0>Okay, let's analyze this ARC task.

**Perception of Elements:**

The task involves 2D grids of colored pixels. The input grids contain two distinct shapes, each formed by a contiguous block of a single color. One shape is always larger and 'L' shaped, while the smaller shape comprises the output and is always a 2x2 block of the same color. The background is always white (0).  The colors of the shapes vary across examples, but the output always matches the color of the larger "L" shaped object.

**YAML Block (Facts):**


```yaml
objects:
  - name: LargeShape
    type: L-shaped block
    properties:
      color: variable (orange, azure, magenta, yellow)
      size: variable
      position: variable
  - name: SmallShape
    type: 2x2 square block
    properties:
      color: variable (orange, azure, magenta, yellow)
      size: fixed (2x2)
      position: variable
  - name: Background
    type: grid
    properties:
      color: white (0)
      size: variable (10x10)
      position: fixed

actions:
  - name: Extract
    description: Isolate the color of the LargeShape.

relations:
  - subject: SmallShape
    predicate: has_same_color_as
    object: LargeShape
  - subject: Output
    predicate: is
    object: SmallShape

```


**Natural Language Program:**

1.  **Identify the LargeShape:** Find the largest contiguous block of non-white pixels forming an "L" shape.
2.  **Determine the Target Color**: Note the color value of the LargeShape.
3.  **Construct Output:** Create a 2x2 grid.
4.  **Color the Output:** Fill all cells in the 2x2 with the Target Color

In simpler terms: The output is a 2x2 square of pixels that has the same color as the larger L-shaped object in the input.

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
{{ natural language description of the transformation rule }}
"""

{{ imports }}

def transform(input_grid):
    # initialize output_grid

    # change output pixels 

    return output_grid

```
