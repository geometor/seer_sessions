# d406998b • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
5 0 5 0 0 5 0 0 0 5
0 5 0 0 5 0 0 5 0 0
0 0 0 5 0 0 5 0 5 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x7FC253D0F850>

**output:**
```
5 0 5 0 0 3 0 0 0 3
0 3 0 0 5 0 0 3 0 0
0 0 0 3 0 0 5 0 5 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x7FC253D0F650>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels (represented by numbers). The primary colors involved seem to be gray (5) and white (0). The transformation seems to involve selectively changing some gray (5) pixels to green (3), based on their spatial relationship with other gray pixels.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - gray (5)
        - green (3)
      position: [row, column]
actions:
  - type: color_change
    agent: unknown
    target: pixel
    from_color: gray (5)
    to_color: green (3)
    conditions:
      - spatial_relationship
relationships:
  - type: adjacency
    between: pixels
```


**Natural Language Program:**

1.  **Identify Target Pixels:** Examine each gray (5) pixel in the input grid.
2.  **Check Adjacency Condition:**
    * Change those to green if gray is adjacent to one white and two gray pixels.
3.  **Apply Transformation:** If all the conditions for a pixel is met, change its color from gray (5) to green (3). If not, leave the pixel's color unchanged.

Essentially, certain gray pixels become green based on adjacent pixel.

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
