# a699fb00 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
1 0 1 0 0
0 0 0 0 0
0 0 0 0 0
0 1 0 1 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7F4C1B75C750>

**output:**
```
1 2 1 0 0
0 0 0 0 0
0 0 0 0 0
0 1 2 1 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7F4C1B703450>

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

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B7011D0>

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

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B700050>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 1 0
0 1 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 0 1 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B75E0D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 2 1 0
0 1 2 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 1 2 1 2 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 2 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 2 1 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B6BFD50>
<PIL.Image.Image image mode=RGB size=1728x1360 at 0x7F4C231A8950>Okay, here's my analysis of the provided input-output examples:

**Perception of Elements:**

The task involves 2D grids containing pixels of different colors. The primary colors observed are blue (1) and white (0) in the input grids, and blue (1), red (2), and white (0) in the output grids. The transformation seems to involve changing some of the blue pixels to red based on their neighbors. The consistent elements seem to be groups of blue pixels, and transformation only impacts those.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      - width: variable
      - height: variable
      - cells: contain integer values representing colors

  - name: pixel
    type: cell
    properties:
      - color: integer (0, 1, or 2)
      - position: (row, column)

  - name: blue_pixel
    type: pixel
    properties:
      - color: 1

  - name: red_pixel
    type: pixel
    properties:
      - color: 2

actions:
  - name: change_color
    description: Changes the color of a pixel.
    parameters:
      - target: pixel
      - new_color: integer

relationships:
   - name: adjacency
     description: two blue pixels that are horizontally adjacent

```


**Natural Language Program:**

1.  **Identify Blue Pixels:** Locate all pixels in the input grid with a value of 1 (blue).
2.  **Check for Horizontal Adjacency:** For each blue pixel, check if it has a horizontally adjacent blue pixel (immediately to the left or right).
3.  **Transform to Red:** If a blue pixel has a horizontally adjacent blue pixel, change that blue pixel to a value of 2 (red) in the output grid, otherwise, leave them the same.
4. All non-blue pixels keep their original values.

In essence, the rule changes blue pixels to red *only* if they are part of a horizontal pair or sequence of blue pixels. Isolated blue pixels remain blue.

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
