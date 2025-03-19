# b548a754 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0
0 3 2 2 2 3 0 0 0 0 8
0 3 2 2 2 3 0 0 0 0 0
0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x704 at 0x7F4C231A8A50>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 3 3 3 3 3 3
0 3 2 2 2 2 2 2 2 2 3
0 3 2 2 2 2 2 2 2 2 3
0 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x704 at 0x7F4C231AAED0>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

*   The input and output are grids of digits, representing colored pixels.
*   The primary colors involved are white (0), green (3), red (2), and azure (8).
*   The input contains a connected green object, a connected red object inside it, and a single azure pixel.
*    The output seems to extend the green and red object to the right edge of non-white area.

**YAML Block (Facts):**


```yaml
objects:
  - id: green_object
    color: green
    shape: rectangle-like
    property: encloses red_object
  - id: red_object
    color: red
    shape: rectangle-like
    property: enclosed by green_object
  - id: azure_pixel
      color: azure
      shape: single pixel

actions:
  - type: extension
    target: green_object
    description: extend green to right edge.
  - type: extension
     target: red_object
     description: extend red to right edge.

relationships:
    - green_object contains red_object
```


**Natural Language Program:**

1.  Identify the green object and the red object it encloses.
2.  Find the right most edge of the colored area (non zero pixels area). In this specific instance it stops before the single azure pixel.
3.  Extend the green object horizontally to the right edge of colored section.
4.  Extend the red object horizontally, within the green object, to the same right edge.
5. Leave all other pixels as zero/white.


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
