# dc1df850 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
2 0 0 0 0
0 0 0 2 0
0 0 0 0 0
0 6 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x716635BBBE50>

**output:**
```
2 1 1 1 1
1 1 1 2 1
0 0 1 1 1
0 6 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x716635C4F8D0>

## train_2

**input:**
```
0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x716635C4EFD0>

**output:**
```
0 0 0 0 0 0 1 2
0 0 0 0 0 0 1 1
0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0
0 1 1 1 0 0 0 0
0 1 2 1 0 0 0 0
0 1 1 1 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x716635C5DD50>

## train_3

**input:**
```
0 0 0 0 0
0 2 0 0 0
0 0 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x256 at 0x716635C5CD50>

**output:**
```
1 1 1 0 0
1 2 1 0 0
1 1 1 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x256 at 0x71663577C250>
<PIL.Image.Image image mode=RGB size=1280x1104 at 0x71663577D450>Okay, here's my analysis of the provided examples, focusing on perception, factual documentation, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves 2D grids where each cell contains a single digit integer (0-9), representing different colors. The core transformation seems to involve identifying non-zero colored pixels in the input and creating a "halo" of blue (value 1) pixels around them in the output. The original non-zero pixels seem to be preserved.  Zero-valued (white) pixels remain unchanged, unless influenced by the halo.

**YAML Documentation of Facts:**


```yaml
facts:
  - object: grid
    description: 2D array of integer values representing colored pixels.
    properties:
      - height: variable, based on input
      - width: variable, based on input
      - cells: individual elements within the grid, each with a color value.

  - object: pixel
    description: An individual cell within the grid.
    properties:
      - color: integer value (0-9) representing the color.
      - row:  row index within the grid.
      - column: column index within the grid.
    actions:
      - change_color:  Modify the color value of the pixel.

  - relation: adjacency
    description:  Pixels are considered adjacent if they share a side (not diagonal).
    properties:
      - neighbors:  A pixel can have up to 4 neighbors (up, down, left, right).

  - action: halo_creation
    description:  Surrounding non-zero pixels with a halo of blue (1) pixels.
    properties:
      - color_source: The original non-zero pixel.
      - halo_color:  Blue (1).
      - halo_extent: One pixel in all adjacent directions (up, down, left, right).

```


**Natural Language Program:**

1. **Iterate** through each pixel in the input grid.
2. **Identify** non-zero pixels. Skip any pixel with value of 0.
3. **Preserve** the original non-zero colored pixels in the output grid by copying it's value.
4. **For each** non-zero pixel, **examine** its four immediate neighbors (up, down, left, and right).
5. **If a neighbor** is within the grid boundaries (exists) and has a value of 0 in the input grid, **change** its value to 1 (blue) in the output grid.
6. **If a neighbor** is not within grid boundaries or is not a zero, leave it as is in output.
7. **Pixels** that have not been affected by a non-zero cell remain unchanged in the output - if a pixel's color is 0 in input, the pixel's color is 0 in output.

This program describes a process where each non-zero pixel "casts" a blue halo onto its adjacent, previously zero-valued neighbors, while non-zero colored cells and other halo cells maintain their original values.

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
