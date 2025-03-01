# b94a9452 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0 0
0 0 0 2 4 4 2 0 0 0 0 0 0
0 0 0 2 4 4 2 0 0 0 0 0 0
0 0 0 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x768 at 0x7F4C1B703150>

**output:**
```
4 4 4 4
4 2 2 4
4 2 2 4
4 4 4 4
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7F4C1B67E450>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 1 3 1 0 0 0 0
0 0 0 0 1 1 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x768 at 0x7F4C1B703F50>

**output:**
```
3 3 3
3 1 3
3 3 3
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F4C1B67E050>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 4 4 6 4 4 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x768 at 0x7F4C1B67E150>

**output:**
```
6 6 6 6 6
6 6 6 6 6
6 6 4 6 6
6 6 6 6 6
6 6 6 6 6
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7F4C1B67E2D0>
<PIL.Image.Image image mode=RGB size=2496x1168 at 0x7F4C1A589B50>Okay, here's my analysis of the provided input-output examples, focusing on elements, a YAML-structured fact section, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves transforming a grid of colored pixels (represented by numbers 0-9) into a smaller grid. The input grids contain a prominent, usually centrally located, colored shape surrounded by a background of '0' (white).  The output grid seems to be a zoomed-in and inverted representation of this central shape. The inversion involves swapping the colors of the inner and surrounding pixels within the shape.

**YAML Block (Facts):**


```yaml
facts:
  - type: input
    description: A 2D grid of integers (colors).
    properties:
      - background_color: 0 (white)
      - shape: Usually centrally located, rectangular, composed of two colors.
      - inner_color:  A distinct color within the shape.
      - outer_color: A distinct color forming the border/surrounding of the inner color.

  - type: output
    description: A smaller 2D grid of integers, derived from the input.
    properties:
      - dimensions: Smaller than the input grid.
      - inverted_colors: Represents an inverted color mapping of the input shape.
      - relation_to_input:  Represents the "core" and one surrounding layer of pixels of a salient object

  - type: transformation
    description: Identification and inversion of a central shape.
    actions:
      - identify_shape: Locate the contiguous colored region in the input.
      - determine_inner_outer: Identify inner and outer colors of the shape.
      - invert_colors: Swap the inner and outer colors.
      - extract_subgrid: Create a smaller grid representing the inverted shape.

```


**Natural Language Program:**

1.  **Identify the Shape:** Locate the contiguous, non-white (non-zero) region within the input grid. This region represents the shape of interest.
2.  **Determine Inner and Outer Colors:** Within the identified shape, distinguish between the 'inner' color and the 'outer' color. The outer color forms the boundary of the shape, while the inner color fills the center.
3. **Extract relevant area**: Find the bounding box of the non-zero area, then enlarge it by one pixel on all sides (or as much as possible given boundary conditions.)
4.  **Invert Colors:** Swap the inner and outer color values to perform the inversion.
5.  **Create Output Grid:** Construct the output grid with dimensions encompassing the inverted colors representing core of the input shape and one layer of surronding pixels.

In essence, the program finds a shape, identifies its inner and outer colors, inverts those colors, and creates a new, smaller grid representing the core and border of that inverted shape.

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
