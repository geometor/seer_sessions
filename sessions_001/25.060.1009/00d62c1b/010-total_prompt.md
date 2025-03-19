# 00d62c1b • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 3 0 3 0 0
0 0 0 3 0 3 3 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC253DE41D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0
0 0 0 3 0 3 0 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 0 0 0 3 4 3 0 0
0 0 0 3 0 3 3 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC253D4F750>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, most of which are white (0). There's a distinct shape formed by green (3) pixels. The transformation seems to involve identifying a specific location within the green shape and changing its color to yellow (4).

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      - rows: 10
      - columns: 10
      - cells: pixels
      - values: {0: white, 3: green, 4: yellow}
  - type: shape
    properties:
      - color: green
      - composition: contiguous green pixels
    actions:
      - identify_center: locates a specific pixel within the shape

  - type: pixel
    properties:
    - color: changes from green to yellow.
    location:
     - determined by its position properties.
```


**Natural Language Program:**

1.  **Identify the green shape:** Find all contiguous blocks of green (3) pixels within the input grid. In this example, there is only one such shape.
2.  **Locate Center:** Determine the pixel at row 4 and column 6 in the grid.
3. **Change to Yellow** if that pixel is green, change it to yellow (4).

The core concept is to find a very specific coordinate and recolor it.

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
