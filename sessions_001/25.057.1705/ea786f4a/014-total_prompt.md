# ea786f4a • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x777851601D10>

**output:**
```
0 3 3 3 3 3 0
3 0 3 3 3 0 3
3 3 0 3 0 3 3
3 3 3 0 3 3 3
3 3 0 3 0 3 3
3 0 3 3 3 0 3
0 3 3 3 3 3 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x777851399BD0>
Okay, here's my analysis of the provided example, focusing on perception, documented facts, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves a grid of pixels, initially mostly green (value 3) with a single white (value 0) pixel in the center. The transformation seems to "expand" or "propagate" the white pixel, replacing green pixels in a cross or plus-sign (+) shape centered on the original white pixel. The green pixels at the corners remain untouched.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      rows: 7
      columns: 7
      cells:
        values: [0, 3]  # white, green
    features:
      - name: center_pixel
        initial_value: 0 # white
        location: [3,3] # zero based row, col

actions:
  - name: expand_center
    type: propagation
    origin: center_pixel
    directions: [up, down, left, right]
    replacement_value: 0

relationships:
  - type: adjacency
    description:  The white pixel expands to adjacent green pixels in cardinal directions.
  - type: boundary_condition
    description: Expansion stops at the edges of the grid, corners remain.
```


**Natural Language Program:**

1.  **Identify the Center:** Locate the single white pixel (value 0) in the input grid. This pixel is the origin.
2.  **Expand Vertically:** Change all green (3) pixels directly above and below the origin pixel to white (0) until reaching the grid's edge.
3.  **Expand Horizontally:** Change all green (3) pixels directly to the left and right of the origin pixel to white (0) until reaching the grid's edge.
4. The output grid corners are green.

Essentially, the transformation takes a single point and projects it into a cross. The origin defines the cross' center. The dimensions of the grid limit the extent.

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
