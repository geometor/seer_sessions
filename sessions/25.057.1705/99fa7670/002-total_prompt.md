# 99fa7670 • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 0 0 0
0 0 2 0 0 0
0 0 0 0 0 0
0 3 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7778516A65D0>

**output:**
```
0 0 0 0 0 0
0 0 2 2 2 2
0 0 0 0 0 2
0 3 3 3 3 3
0 0 0 0 0 3
0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x777851443D90>
Okay, here's my analysis of the provided example, structured as a report:

**Perception of Task Elements:**

The task involves a grid of colored pixels, with most being white (0) and a few being non-white (red (2) and green (3)). The transformation seems to involve expanding the non-white pixels. The shapes of the colored regions in the output appear to be related to the positions of the colored pixels in the input, but extended.

**YAML Fact Block:**


```yaml
facts:
  - object: grid
    description: 2D array of pixels
    properties:
      - width: 6
      - height: 6
      - cells: integers representing colors (0-9)

  - object: red_pixel
    color: 2 (red)
    initial_position: (1, 2) [row, col]
    action: expand horizontally and vertically

  - object: green_pixel
    color: 3 (green)
    initial_position: (3, 1)
    action: expand horizontally and vertically

  - relation: expansion
    description: Non-white pixels extend to fill space to right and down,
     but cannot go past the edge of the grid or another expanding pixel
```


**Natural Language Program:**

1.  **Identify** all non-white pixels (pixels with a value other than 0) in the input grid.
2.  For each non-white pixel:
    *   **Expand Horizontally:** Change all white pixels to the right of the identified pixel on the same row to the color of the current non-white pixel, stopping if another non-white pixel, or the edge of the grid, is reached.
    *   **Expand Vertically:** Change all white pixels below, in the same column, the identified non-white pixel and the horizontal expansion, and change all white pixels in each cell to the color of the current non-white pixel. Stop when another non-white pixel, or the edge of the grid, is reached.

The expansion to right and down happens for all non-white pixels.


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
