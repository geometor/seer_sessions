# 7447852a • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x192 at 0x76911EB26490>

**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0 0 2 4
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0 2 0 2
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x192 at 0x76911EB263F0>
Okay, here's my analysis of the provided input-output example, formatted as requested:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors observed are red (2), white (0), and yellow (4). The input grid transforms into an output grid of the same dimensions. The transformation seems to involve a selective replacement of white (0) pixels with yellow (4) pixels, based on the positions of red (2) pixels. It's a local operation as values change due to adjacent pixels, and the transformation appears to be row-independent, meaning the same operation is performed at the same row index of each grid, and on each row of the grids.

**YAML Fact Block:**


```yaml
facts:
  - object: grid
    properties:
      - dimensions: 3x18 (rows x columns)
      - elements: pixels
      - colors: [red, white, yellow]
    relationships:
      - input_grid: same dimensions as output_grid

  - object: pixel
    properties:
      - color_value: integer (0, 2, 4)
      - color_name: [white, red, yellow]
      - position: (row, column)
    actions:
      - change_color: white (0) can change to yellow (4)
    relationships:
      - adjacent_to: other pixels in the grid

  - object: transformation_rule
    properties:
      - type: conditional color change
    conditions:
      - if: a white pixel is adjacent to a red pixel on specific sides.
      - then: change the white pixel to yellow.
```


**Natural Language Program:**

1.  **Iterate** through each cell of the input grid.
2.  **Identify** red (2) pixels.
3.  **Examine** the white (0) pixels to the right and below any red pixels, if there is one.
4.  **If** a white pixel is found to the right of red pixel, then change that pixel in the corresponding location of the output to yellow (4).
5.  **If** a white pixel is found below a red pixel, then change that pixel in the corresponding location of the output grid to yellow (4).
6. **If** a pixel in the input grid is red (2), then the pixel will be (2) in the output grid, i.e. no change.
7. **If** a pixel in the input grid is yellow(4), then the pixel will be (4) in the output grid, i.e. no change.
8. Any white pixels not adjacent to a red square on its right or bottom side remains white (0).

In short, the color change rule can be expressed as: *Change a white pixel to yellow if it is immediately to the right or immediately below a red pixel, otherwise keep their original color*.

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
