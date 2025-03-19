# 694f12f3 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 4 4 4 4 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F0A59D17070>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 2 2 2 4 0 0 0 0
0 4 2 2 2 4 0 0 0 0
0 4 2 2 2 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 4 1 1 4 0
0 0 0 0 0 4 4 4 4 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F0A5ADF5F90>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves two grids (input and output) of size 10x10. The primary colors involved are yellow (4), red (2), blue(1), and white (0). The input grid contains two distinct yellow (4) rectangular shapes, one in the top-left and another in the bottom-right. The output grid shows modifications within these yellow shapes. The inner parts of yellow shapes are changed into other colors.

**YAML Block (Facts):**


```yaml
objects:
  - id: shape1
    type: rectangle
    color: yellow (4)
    position: top-left
    dimensions:
      height: 5
      width: 6
  - id: shape2
    type: rectangle
    color: yellow (4)
    position: bottom-right
    dimensions:
      height: 3
      width: 4
  - id: innershape1
    type: rectangle
    color: red(2)
    position: inside shape1
    dimensions:
      height: 3
      width: 3
  - id: innershape2
    type: rectangle
    color: blue(1)
    position: inside shape2
    dimensions:
      height: 1
      width: 2

actions:
  - type: fill_inside
    target: shape1
    color: red (2)
  - type: fill_inside
    target: shape2
    color: blue (1)

relationships:
    - type: contains
      from: shape1
      to: innershape1
    - type: contains
      from: shape2
      to: innershape2
```


**Natural Language Program:**

1.  **Identify** all rectangular shapes of color yellow (4) in the input grid.
2.  For each identified yellow rectangle:
    *   Determine the dimensions (height and width) of the rectangle.
    *   Calculate the dimensions of an inner rectangle:
        *   Inner rectangle height =  Outer rectangle height - 2
        *   Inner rectangle width = Outer rectangle width - 2
    *    Determine the color of the inner rectangle. The top left rectangle gets filled with Red(2) and the bottom right with Blue(1).
    *   **Fill** the inner area of the yellow rectangle with a new rectangle, leaving a one-pixel yellow border, and changing the color of the inner pixels as defined above.

Essentially, the transformation finds yellow rectangles and fills their inner area with different colors, keeping the external borders. The top left gets filled red, and bottom right gets filled blue.

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
