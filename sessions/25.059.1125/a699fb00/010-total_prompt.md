# a699fb00 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A588450>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 2 1 2 1 2 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 2 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 2 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1A58A750>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The task involves a grid of pixels, where each pixel has a color value (represented by integers 0-9). The input grid seems to have a pattern of blue (1) pixels against a background of white (0) pixels. The output grid introduces red (2) pixels adjacent to the blue pixels. The overall grid dimensions remain the same.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 10x10
      cells: pixels
      colors: [0, 1, 2]  # white, blue, red
  - type: pixel
    properties:
      color: integer (0-9)
      position: (row, column)

actions:
  - name: identify_blue_pixels
    description: Locate all pixels with color value 1.
  - name: change_color
    description: Change the color of a pixel.
  - name: check_adjacency
    description: Determine the adjacent position

relationships:
  - adjacency: Pixels can be horizontally or vertically adjacent.
```


**Natural Language Program:**

1.  **Identify Blue Pixels:** Scan the input grid and find all pixels with a value of 1 (blue).
2.  **Check to the Right:** For each blue pixel, check if to the right of the position exist and if the exist and it contains 0, change the color from 0 to 2.


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
