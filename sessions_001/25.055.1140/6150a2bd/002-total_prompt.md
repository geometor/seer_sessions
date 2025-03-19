# 6150a2bd • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
3 3 8
3 7 0
5 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x75DC67A644C0>

**output:**
```
0 0 5
0 7 3
8 3 3
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x75DC67A659F0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a 3x3 grid of colored pixels. Each pixel is represented by a single digit integer (0-9), corresponding to a specific color. The transformation between the input and output grids appears to involve a rotation and possibly some color changes, but it's not immediately obvious without further analysis. The overall size and shape of the grid remain constant.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    dimensions: 3x3
    elements: pixels
    properties:
      color: integer (0-9)
  - transformation:
      type: rotation
      details: "90 degrees counter-clockwise"
```


**Natural Language Program:**

The input grid is rotated 90 degrees counter-clockwise to produce the output grid.

1.  **Rotate**: rotate the entire input grid by 90 degrees in the counter-clockwise direction

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
