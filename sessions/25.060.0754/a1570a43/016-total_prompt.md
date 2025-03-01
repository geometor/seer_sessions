# a1570a43 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 2 2 0 0 0 0 0
0 3 2 2 2 2 0 3 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x576 at 0x7A1754162D50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 2 2 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 2 2 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x576 at 0x7A174C7009D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors involved are white (0), red (2), and green (3).  The transformation seems to involve a rearrangement or shifting of the red (2) pixels, while the green (3) pixels remain fixed. The input has a cross shape made of red, and it appears to be rotating.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 9x10 (rows x columns)
      cells: integers representing colors (0-9)
  - type: pixel
    properties:
      color:
        - 0 (white)
        - 2 (red)
        - 3 (green)
      position: (row, column)
  - type: shape
    properties:
        color: 2
        form: cross
actions:
  - type: re_arrange
    agent: red shape
    target_object: red pixels
relationships:
  - green pixels: stationary
  - red pixels: form a cross shape, move or are re-arranged
```


**Natural Language Program:**

1.  **Identify Objects:** Locate all pixels with the color green (3) and red (2) within the input grid.
2.  **Green Preservation:** Maintain the positions of the green (3) pixels in the output grid; they do not move.
3.  **Red Cross Rotation:** Red (2) pixels creates the shape of a cross. The cross in the input is rotated 90 degrees clockwise to create the shape of the red cross in the output.
4.    The bounding box surrounding cross is shifted one pixel down to re-create the output.

In summary it is the red pixels in the shape of the cross that are transformed.

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
