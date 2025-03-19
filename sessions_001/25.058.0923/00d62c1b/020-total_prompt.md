# 00d62c1b • 020 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 0 0 3 0 0 0 0
0 0 3 0 0 3 0 3 0 0
0 0 3 3 3 3 3 3 3 0
0 0 0 3 0 0 0 0 3 0
0 0 0 3 0 0 0 3 3 0
0 0 0 3 3 0 0 3 0 3
0 0 0 3 0 3 0 0 3 0
0 0 0 0 3 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B3DDB382550>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0
0 0 3 4 4 3 0 0 0 0
0 0 3 4 4 3 0 3 0 0
0 0 3 3 3 3 3 3 3 0
0 0 0 3 0 0 0 0 3 0
0 0 0 3 0 0 0 3 3 0
0 0 0 3 3 0 0 3 4 3
0 0 0 3 4 3 0 0 3 0
0 0 0 0 3 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B3DDA974D50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, primarily consisting of white (0) and green (3) pixels. The transformation seems to involve identifying specific green pixels and changing their color to yellow (4). The placement of these yellow pixels seems to be related to the shape formed by the green pixels.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 10x10
      cell_values: [0, 3, 4]
  - type: pixel
    properties:
      color:
        white: 0
        green: 3
        yellow: 4
      position: (row, column)
  - type: shape
    properties:
        color: green
        contiguous: true # assumption that the shape consists of touching pixels

actions:
  - name: identify_interior_pixels
    description: Locates green pixels enclosed within a certain region of other green pixels.
  - name: change_color
    description: Modifies the color of a pixel.
    parameters:
      target_color: yellow

relationships:
  - type: encloses
    description: A set of green pixels encloses other green pixels if they are inside the approximate center of the contiguous region.
```


**Natural Language Program:**

1.  **Identify the green shape:** Find all pixels with a value of 3 (green).
2.  **Locate interior green pixels:** Within the green shape, find green pixels that are directly adjacent to each other horizontally forming a 2x2 block.
3.  **Change color:** Change the color of these identified interior pixels to 4 (yellow).
4. **Preserve Other Pixels:** Leave all the remaining pixels as they are.

In summary. The transformation changes some green pixels to yellow, these pixels are found inside of a 2x2 block of only green pixels.

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
