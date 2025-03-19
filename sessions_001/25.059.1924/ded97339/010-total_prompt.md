# ded97339 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635B76650>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 8 8 8 8 8
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635B75FD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, most of which are white (0).  The key element is the presence of azure (8) pixels. The transformation seems to involve manipulating these azure pixels based on their initial positions. Specifically, a vertical line and a horizontal line are created/modified.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    color: white (0)
    property: background
  - type: pixel
    color: azure (8)
    property: foreground
  - type: grid
    property: input
  - type: grid
    property: output

actions:
  - type: propagation
    object: azure pixel
    direction: vertical
    condition: from original positions
  - type: propagation
      object: azure pixel
      direction: horizontal
      condition: from an original y position

relationships:
  - type: spatial
    description: azure pixels are distributed within the grid.
  - type: transformation
    description:  Input grid's azure pixels determine the output grid's azure pattern.

```


**Natural Language Program:**

1.  **Identify:** Locate all azure (8) pixels in the input grid.
2.  **Vertical Propagation:** For each azure pixel in the input, draw a vertical line of azure pixels downwards, taking the original position of each pixel as the x coordinate of the new pixels.
3.  **Horizontal propagation;** From the original y position with an azure pixel, draw a horizontal line using the value of the azure pixels.


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
