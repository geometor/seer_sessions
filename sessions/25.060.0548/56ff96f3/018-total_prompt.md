# 56ff96f3 • 018 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B4C05B57C50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B4BFDB43A50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a transformation of a 2D grid of pixels. The primary color involved is yellow (represented by the digit '4'). The background is white (represented by '0'). The transformation seems to involve expanding a yellow region.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 10x10
      elements: pixels
      colors: [white, yellow]

  - type: yellow_pixel
    properties:
      color: yellow
      initial_positions: [(2,1), (6,5)]

  - type: yellow_region
    properties:
      shape: rectangle
      initial_seed: yellow_pixels
      final_shape: 6x5 rectangle

actions:
  - type: expansion
    target: yellow_region
    description: Expands from isolated yellow pixels to form a filled rectangle.

relationships:
  - type: contains
    from: grid
    to: yellow_region
```


**Natural Language Program:**

1.  **Identify** all isolated yellow pixels in the input grid.
2.  **Determine** the bounding box by identifying minimal and maximal row and minimal and maximal columns occupied by the yellow pixels.
3.  **Fill** the bounding box defined by yellow pixels with yellow, creating the output grid. In the example, there were 2 seed points (2, 1) and (6, 5). Minimal row: 2, Maximal Row: 6. Maximal Column: 5, minimal column: 1.
4.  **Resulting** Rectangle should span these rows and columns inclusive.

In essence, the transformation takes isolated yellow pixels and uses their locations to construct the minimal and maximal extent of a rectangle of yellow pixels.

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
