# f25fbde4 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x716635C5C750>

**output:**
```
0 0 4 4 4 4 0 0
0 0 4 4 4 4 0 0
4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4
0 0 4 4 4 4 0 0
0 0 4 4 4 4 0 0
```

<PIL.Image.Image image mode=RGB size=512x384 at 0x716635C5DE50>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0
0 0 0 4 4 0 0 0 0
0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x716635C5DC50>

**output:**
```
0 0 4 4 0 0
0 0 4 4 0 0
4 4 4 4 0 0
4 4 4 4 0 0
0 0 0 0 4 4
0 0 0 0 4 4
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x71663578F2D0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x71663578E050>

**output:**
```
0 0 4 4 0 0
0 0 4 4 0 0
4 4 4 4 0 0
4 4 4 4 0 0
0 0 4 4 0 0
0 0 4 4 0 0
0 0 4 4 4 4
0 0 4 4 4 4
```

<PIL.Image.Image image mode=RGB size=384x512 at 0x71663578C4D0>
<PIL.Image.Image image mode=RGB size=1856x1168 at 0x71663578D0D0>Okay, let's analyze the provided input-output pairs to understand the transformation.

**Perception of Elements:**

The task involves 2D grids where cells have one of two colors: white (0) or yellow (4). The primary object appears to be a contiguous shape formed by yellow pixels. The transformation seems to involve manipulating this yellow shape. The size of the output grid is smaller (fewer rows/columns) than the input grid in all of the examples given so far. The transformation expands the input yellow object down and to the right (or up and to the left depending on one's interpretation) and alters the shape to more resemble a filled rectangle.

**YAML Block (Facts):**


```yaml
objects:
  - name: YellowShape
    type: ContiguousRegion
    color: Yellow (4)
    properties:
      - initial_shape: Irregular
      - final_shape: Rectangle-like

actions:
  - name: Expand
    agent: YellowShape
    type: GeometricTransformation
    parameters:
      direction: Down and Right, with shape altering

relationships:
  - subject: YellowShape
    relation: ContainedWithin
    object: InputGrid

  - subject: YellowShape
    relation: TransformsTo
    object: ExpandedYellowShape

  - subject: InputGrid
    relation: Contains
    object: YellowShape
  
  - subject: OutputGrid
    relation: Contains
    object: ExpandedYellowShape
```


**Natural Language Program:**

1.  **Identify the Yellow Shape:** Locate the contiguous region of yellow (4) pixels within the input grid.
2.  **Bounding Box and Expansion:**
    -   Determine the bounding box of the yellow shape, expanding on the right and bottom, filling it in.
    -   From the original box's top-left, extend a rectangle down and to the
        right to fill in the area encompassed by the original shape.
3.  **Output:** Create a new grid containing only the filled expanded yellow shape (with 0s as padding), where the bounding edges of the shape are aligned with the edges of the output image.


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
