# d406998b • 020 • example_4 • investigate_coder

---

## Example 4

**input:**
```
0 0 5 0 0 5 0 5 0 5 0 5 0 0
5 0 0 0 5 0 0 0 5 0 5 0 0 5
0 5 0 5 0 0 5 0 0 0 0 0 5 0
```

<PIL.Image.Image image mode=RGB size=896x192 at 0x7B1DDE486550>

**output:**
```
0 0 5 0 0 3 0 3 0 3 0 3 0 0
5 0 0 0 5 0 0 0 5 0 5 0 0 3
0 3 0 3 0 0 5 0 0 0 0 0 5 0
```

<PIL.Image.Image image mode=RGB size=896x192 at 0x7B1DDE487150>
Okay, here's my analysis of the example input-output pair, formatted as a report:

**Perception of Elements:**

The task involves a grid of pixels, each with a numerical value representing a color. The primary colors observed are gray (5), white (0), and green (3). The input and output grids have the same dimensions (3x14). The transformation appears to involve changing some of the gray (5) pixels to green (3), and it seems the pattern is related to their position.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      dimensions: [3, 14]
      pixels: [integers, range 0-9]
  - type: pixel
    properties:
      color: [gray, white, green]
      value: [0, 3, 5]
      position: [row, column]

actions:
  - type: change_color
    description: Change the color of a pixel from gray to green.
    conditions:
      - Based on x,y position of gray colored pixel

relationships:
  - spatial: Pixels are arranged in a grid.
  - conditional: Color change depends on the pixel's position, specifically alternating.
```


**Natural Language Program:**

1.  **Iterate** through each pixel of the input grid.
2.  **Identify** gray (5) pixels.
3.  Starting at the right side of the image, for every gray pixel change the first, skip the next two, and repeat this three step cycle.
4.  **Change** the identified gray pixels into green (3) pixels.
5.  **Preserve** all other pixels (non-gray) as they are.
6.   All other pixels retain original color and position.

Essentially, the transformation selectively changes every third gray pixel to green, starting from the right, while leaving all other pixels unchanged.

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
