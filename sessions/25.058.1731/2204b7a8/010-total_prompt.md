# 2204b7a8 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 7 7 7
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36045021D0>

**output:**
```
4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 4 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 7 7 7
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C3604502ED0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a 10x10 grid. The input grid contains pixels of colors yellow (4), white (0), green (3), and orange (7). The output grid appears to maintain the structure of yellow, white, and orange pixels but changes green pixels to yellow, and some yellow pixels in the sixth line from the top become orange. The core concept appears to involve a color substitution, specifically of green pixels, and selective changes to the 6th horizontal line.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    properties:
      color:
        values: [0, 3, 4, 7]

  - type: pixel
    properties:
      color:
        values: [0,3,4,7]
      position:
        values: [row, col]

actions:
  - type: color_substitution
    input_color: 3
    output_color: 4
    scope: all

  - type: color_substitution
        input_color: 4
        output_color: 7
        scope: limited
        conditions:
           - row == 6

relationships:
 - type: spatial
   description: pixels are arranged in a 2D grid.
```


**Natural Language Program:**

1.  **Iterate** through each pixel in the input grid.
2.  **If** a pixel's color is green (3), **change** its color to yellow (4).
3. **If** a pixel's color is yellow (4) and it is located on the 6th row from the top, **change** the yellow (4) pixel to orange (7).
4.  **Otherwise**, keep the pixel's original color.
5.  **Output** the modified grid.

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
