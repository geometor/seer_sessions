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

<PIL.Image.Image image mode=RGB size=448x448 at 0x76911E9AE170>

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

<PIL.Image.Image image mode=RGB size=448x448 at 0x76911E9AEB70>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of pixels, initially all green (value 3) except for a single white (value 0) pixel in the center. The transformation seems to involve an expansion or propagation of the white pixel, creating a cross or plus-shaped pattern of white pixels centered on the original white pixel. The green pixels at the corners of the grid remain, but the green pixels adjacent to the expanding white area change into white pixels.  The final output has a symmetric cross of white cells on a field of green.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 7x7
      elements: pixels
      default_value: 3 (green)
  - type: pixel
    properties:
      values: [0 (white), 3 (green)]
      initial_state:
        white_pixel:
          location: (3,3) # (row, col), 0-indexed
          value: 0
        green_pixels:
          location: all other locations
          value: 3
actions:
  - type: change_color
    description: Change pixel color from green to white.
    conditions:
      - Adjacent to a white pixel (horizontally or vertically).
relationships:
  - adjacency: Determines which pixels are affected by the color change.
  - symmetry: The final pattern is symmetrical around the initial white pixel.
```


**Natural Language Program:**

1.  **Identify the Center:** Locate the single white pixel (value 0) in the input grid. This is the center of the transformation.
2.  **Expand Horizontally and Vertically:** Change all green (value 3) pixels to white (value 0) along the row and column that pass through the initial white pixel.
3. Keep green pixels that are on the borders on each corner

In simple terms: find the single white, then make its whole row and column white.

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
