# e40b9e2f • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 0 7 4 7 0 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BBB6D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 7 0 4 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 7 7 4 7 7 0 0 0
0 0 0 4 7 4 0 0 0 0
0 0 4 0 7 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BBBA50>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

The task involves a grid of pixels, initially mostly black (0). There's a distinct shape formed by orange (7) and yellow (4) pixels in the input. The output shows a modified version of this shape. The most noticeable change is a rotation and some expansion of certain parts of the shape. Specifically, the yellow pixels appear to have "moved" outwards, and the orange pixels have shifted. It seems like a combination of a reflection over x and y axis, and a swap of "layers".

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - rows: 10
      - columns: 10
      - cells: pixels (integers 0-9, representing colors)
  - type: shape
    properties:
      - colors: [orange, yellow]
      - composition: connected pixels of colors 7 and 4
    actions:
      - rotate:  # Inferring rotation, see details below
          details: appears to be a combination of 90 degree rotations and/or reflections.
      - expand: #expanding the outside border
          details: yellow moves outward, creating a border around original central shape

relationships:
  - type: spatial
    details: The orange and yellow pixels form a contiguous shape in both input and output.
  - type: transformation
    details: The input shape is transformed into the output shape via rotation and expansion.
```


**Natural Language Program:**

1.  **Identify the Core Shape:** Locate the connected component of orange (7) and yellow (4) pixels in the input grid.
2.  **Swap the outer and inner layer:** Swap the position of the yellow and orange pixels.
3.  **Mirror/Reflect:** reflect the shape across both the horizontal and vertical center lines of the sub-grid.
4. **Recombine and Output:** Output the resulting grid.

In other words: The shape in the input is rotated by swapping the position of the colors and reflecting through x, y axis.

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
