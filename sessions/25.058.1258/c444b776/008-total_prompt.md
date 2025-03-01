# c444b776 • 008 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1216x1216 at 0x7E120E2F6030>

**output:**
```
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 7 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 2 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 8 7 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 8 0 0 3 0
0 7 0 0 0 0 0 0 0 4 0 7 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 4 0 0 0 0 0 7 0 0 0
0 0 0 2 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 2 0 0 0 0 0 0 4 0 0 2 0 0 0 0 0 0
0 3 0 0 0 3 0 0 0 4 0 3 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 8 7 0 0 0 0 4 0 0 0 8 7 0 0 0 0
0 0 0 0 8 0 0 3 0 4 0 0 0 0 8 0 0 3 0
0 7 0 0 0 0 0 0 0 4 0 7 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1216x1216 at 0x7E120E2F6350>
Okay, here's my analysis of the provided input-output example pair:

**Perception of Elements:**

The task involves a grid of colored pixels. The most prominent feature is a vertical line of yellow (4) pixels extending from the top to the bottom of the input grid. There's also a horizontal line of yellow pixels across the middle row. The output grid appears to maintain the central yellow line and reflect other colored pixels across this line, but not the line itself. The input image contains a combination of single, isolated, colored pixels and the solid line.

**YAML Block - Facts:**


```yaml
objects:
  - type: pixel
    properties:
      color: [white, blue, red, green, yellow, gray, magenta, orange, azure, maroon]
      position: [row, column]
  - type: line
    properties:
      color: yellow
      orientation: [vertical, horizontal]
      position:
        vertical: center_column
        horizontal: center_row

actions:
  - type: reflection
    properties:
      axis: vertical_yellow_line
      scope: all pixels except yellow line pixels

relationships:
  - type: spatial
    description: Pixels are arranged in a 2D grid.
  - type: symmetry
    description: Output grid shows reflection symmetry across the vertical yellow line.
```


**Natural Language Program:**

1.  **Identify the Axis:** Locate the vertical line of yellow (4) pixels that runs down the center of the grid. This is the reflection axis and its position and color do not change. The horizontal yellow line does change.
2.  **Reflect Other Pixels:** For every non-yellow pixel in the input grid to the left or right of the central yellow line, find its corresponding position on the *opposite* side of the vertical axis (the vertical yellow line). If the non-yellow input pixel is N pixels away for the central line, then copy this pixel to N pixels away on the other side.
3. The output of the process maintains the original central line.


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
