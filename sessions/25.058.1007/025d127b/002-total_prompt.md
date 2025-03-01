# 025d127b • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0
0 6 0 0 6 0 0 0 0
0 0 6 0 0 6 0 0 0
0 0 0 6 0 0 6 0 0
0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0
0 0 2 0 0 2 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x896 at 0x7EE12139A530>

**output:**
```
0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0
0 0 6 0 0 6 0 0 0
0 0 0 6 0 0 6 0 0
0 0 0 0 6 0 6 0 0
0 0 0 0 6 6 6 0 0
0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 2 0 2 0 0 0
0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x896 at 0x7EE1213C1A90>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0
0 8 0 0 0 0 8 0 0
0 0 8 0 0 0 0 8 0
0 0 0 8 0 0 0 0 8
0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x512 at 0x7EE1213C1C70>

**output:**
```
0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 0 0
0 0 8 0 0 0 0 8 0
0 0 0 8 0 0 0 0 8
0 0 0 0 8 0 0 0 8
0 0 0 0 8 8 8 8 8
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x512 at 0x7EE1213C1BD0>
<PIL.Image.Image image mode=RGB size=1212x1842 at 0x7EE1213C2170>Okay, here's my analysis of the provided input-output pairs, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The task involves 2D grids where each cell contains a single digit integer representing a color. The primary elements are colored regions or "objects" within the grid. The transformation appears to selectively remove parts of these objects. Specifically, it seems to remove the "innermost" pixels of the colored objects, leaving only the outer "border" pixels.

**YAML Block - Facts:**


```yaml
objects:
  - type: shape
    description: Contiguous regions of non-zero pixels.
    properties:
      - color:  The integer value of the pixels (0-9).
      - border: The outermost layer of pixels of the shape.
      - interior: The pixels within the border.
      - bounding_box: smallest rectangle around shape
actions:
  - name: remove_interior
    description: Removes the interior pixels of a shape, leaving only the border.
relationships:
  - type: containment
    description:  Interior pixels are contained within the border pixels.
```


**Natural Language Program:**

1.  **Identify Shapes:** Find all contiguous regions of non-zero pixels. Consider each of these regions as a separate "shape".

2.  **Define Border:** For each shape, identify its "border" pixels. A border pixel is a non-zero pixel that has at least one neighboring zero-valued pixel (either horizontally, vertically, or diagonally).

3.  **Remove Interior:** Remove all "interior" pixels. Interior pixels are those which are not border cells.

4.  **Construct Output:** Create a new grid, identical in size to the input grid. Copy only the border pixels of each identified shape to the corresponding positions in the output grid. All other pixels in the output grid should be 0.

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
