# 6150a2bd • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
5 5 2
1 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F0A5ADF6350>

**output:**
```
0 0 0
0 0 1
2 5 5
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F0A7365D4F0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves two 3x3 grids. The input grid contains colored pixels with numerical values representing different colors (0: white, 1: blue, 2: red, 5: gray). The output grid appears to be a rotated version of the input grid, but with the colors inverted, top-to-bottom.

**YAML Block (Facts):**


```yaml
facts:
  - type: grid
    dimensions: 3x3
    description: Input and output grids are 3x3 matrices.
  - object: pixels
    properties:
      - color: Represented by integers 0-9.
      - position: Defined by row and column indices.
  - transformation: rotation
    type: counter-clockwise
    degrees: 90 #This will need verification later, but looks like it
    description: The input grid appears to be rotated 90 degrees counter-clockwise to form the output grid.
  - transformation: color_inversion
    description: input is mirrored vertically, top-to-bottom
```


**Natural Language Program:**

1.  **Mirror:** Take the input grid and flip the rows vertically. The top row becomes the bottom, and the bottom row becomes the top, keeping their relative ordering.


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
