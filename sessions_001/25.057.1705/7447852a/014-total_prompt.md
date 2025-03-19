# 7447852a • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x192 at 0x77785139ACB0>

**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0 0 2 4
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0 2 0 2
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x192 at 0x77785139A7B0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors involved seem to be red (2), white (0), and yellow (4). The transformation seems to involve some kind of interaction or replacement of colors based on their adjacency. The input grid has a discernible pattern, and it seems that the yellow color is introduced in the output grid based on the context defined in the input grid.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      rows: 3
      columns: 18
      colors: [red, white, yellow]
  - type: pixel
    properties:
      color:
        red: 2
        white: 0
        yellow: 4
      position: [row, column]

actions:
  - type: replace_color
    description: Replaces a white pixel with a yellow pixel based on context.
    conditions:
      - condition: adjacent_colors
        description:  Checks colors of adjacent pixels.

relationships:
 - type: adjacency
   description: Determines which pixels are next to each other (horizontally and vertically).
```


**Natural Language Program:**

1.  **Iterate** through each pixel of the input grid.
2.  For each pixel, check if it is white (0).
3. If a pixel is white, check its immediate horizontal neighbors (left and right).
4.  If a white pixel is horizontally adjacent to a red pixel *on the left*, then change that white pixel to a yellow one.
5.  If a white pixel is horizontally adjacent to a red pixel *on the right*, then change that white pixel to a yellow one.
6. If a white pixel has *red neighbours on both its left and right*, and a yellow pixel is on the edge of the block of the size three whites that contain that white pixel, and on the *same* side as the neighbor red, substitute this white with a yellow.
7.  Copy all red pixels from the input to the output grid, in their original positions, without changing their color.

Essentially, white pixels touching red pixels horizontally can become yellow.

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
