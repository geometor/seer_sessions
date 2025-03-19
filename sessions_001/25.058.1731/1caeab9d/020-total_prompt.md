# 1caeab9d • 020 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 1 0 2 0 0 0 0 0 0
0 1 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x320 at 0x7C36045DD550>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 2 0 0 4 0 0 0
0 1 0 2 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x320 at 0x7C36044BF750>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The colors are represented by single-digit integers. The input grid transforms into the output grid based on a seemingly simple rule. The primary colors present are blue (1), red (2), and yellow (4). The background is white (0). The shapes appear to be single, isolated pixels.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color: [0, 1, 2, 4]  # white, blue, red, yellow
      position: [row, column]
  - type: grid
    properties:
      dimensions: [rows, columns]

actions:
  - name: move_down
    description: Certain colored pixels shift downwards.
    parameters:
      - color: [1, 2, 4]
      - rows: int

relationships:
  - type: spatial
    description: Pixels are arranged in a 2D grid.
    elements: [pixel, pixel]
```


**Natural Language Program:**

1.  **Identify Target Pixels:** Locate all pixels of color blue (1), red (2), and yellow (4).
2.  **Conditional Check**: Of these pixels, select those which have a white (0) pixel directly above them.
3.  **Move Down:** Shift the selected pixel's location one row down, replacing any element at the position one row down.
4.  **Blank Above**: Set the position of the previous row to white/empty (0)

In essence, the transformation rule is a conditional downward shift of colored pixels (1, 2, and 4) if the pixel above them is white (0).

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
