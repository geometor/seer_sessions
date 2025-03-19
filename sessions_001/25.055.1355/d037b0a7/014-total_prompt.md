# d037b0a7 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
4 0 0
0 2 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7DCBFF5DB6D0>

**output:**
```
4 0 0
4 2 0
4 2 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7DCBFF5DA6E0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a 3x3 grid of colored pixels. The input grid contains yellow (4), red (2), and white (0) pixels. The output grid seems to be a modified version of the input grid, with some pixels retaining their original colors and positions, while others change. The most notable change is the replication of colored pixels downwards.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    dimensions: 3x3
    elements: pixels
    properties:
      - color:
          values: [0, 2, 4] #white, red, yellow

  - type: pixel
    properties:
      - color:
          values: [0, 2, 4]
      - position:
          row: [0, 1, 2]
          col: [0, 1, 2]

actions:
  - name: replicate_color_downward
    description: The color from the top of non-white colors is copied downwards.
    parameters:
      - color: original color of the pixel

relationships:
- type: spatial
  description: Pixels are arranged in a 2D grid.
- type: color_replication
  description: >-
    Non-white colors in the top row initiate a downward propagation of their
    color.
```


**Natural Language Program:**

1.  **Identify Key Pixels:** Locate non-white pixels in the input grid.
2.  **Propagate Colors Downward:** For each non-white pixel in the top row (row 0), its color is copied to all the rows in that column that are below it. If other color appears in column below the current color it copies down until that point.

In other words the yellow in the top left, is replicated downwards through the whole first column, and red in the center is copied downwards to fill the column beneath it.

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
