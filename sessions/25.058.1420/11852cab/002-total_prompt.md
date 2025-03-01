# 11852cab • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 8 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 8 0 3 0 8 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608D12F750>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 8 0 3 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 8 0 3 0 8 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 3 0 8 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608CEF5C70>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 3 0 4 0 3 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608CEF6350>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 2 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 3 0 4 0 3 0 0 0
0 0 0 4 0 4 0 0 0 0
0 0 2 0 3 0 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608CEF63F0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 8 0 1 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608CEF6210>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 4 0 4 0 0 0
0 0 0 8 0 1 0 8 0 0
0 0 0 0 4 0 4 0 0 0
0 0 0 8 0 8 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7A608CEF5E50>
<PIL.Image.Image image mode=RGB size=2000x1330 at 0x7A608C34AA30>Okay, here's my analysis of the provided examples, structured as a report:

**Perception of Elements:**

The task involves 2D grids where each cell contains a single digit (0-9), representing a color. The input grids appear to have a central "cross" or "plus" shape formed by colored pixels (non-zero values). The transformation seems to involve duplicating some parts of this cross shape.

**YAML Fact Documentation:**


```yaml
facts:
  - object: grid
    type: 2D array
    properties:
      - dimensions: 10x10
      - cell_values: integers (0-9)
      - color_representation:  {0: white, 1: blue, 2: red, 3: green, 4: yellow, 8: azure}

  - object: cross_shape
    properties:
      - composition: contiguous non-zero pixels
      - shape:  '+' (plus sign)
      - location: centered (approximately)

  - action: duplication
    description: Replication of certain parts of the cross shape.
    parameters:
      - source: vertical arms of the cross
      - destination: potentially new rows added below and/or above existing non-zero rows

  - relation: adjacency
    description:  Pixels are adjacent horizontally, vertically, or diagonally. Relevant for defining the cross shape.
```


**Natural Language Program:**

1.  **Identify the Cross:** Locate the central "cross" shape in the input grid. This is defined as a set of contiguous, non-zero pixels forming a plus shape.

2.  **Identify Arms:** the arms of the cross shape can be found by color. In at least one
    case, the input cross has more than 4 arms.

3.  **Duplicate Vertical Arms:** If there are vertical arms of the cross, create
    a copy of it in the row adjacent to the center of the cross.

4.  **No change of other pixels**: Do not make any other changes to any other pixels.

In summary the logic is duplicating the cross arms above or below the center row.

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
