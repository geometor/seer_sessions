# 694f12f3 • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 0
0 0 0 4 4 4 4 4 4 0
0 0 0 4 4 4 4 4 4 0
0 0 0 4 4 4 4 4 4 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F0A59D631B0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 1 1 4 0 0 0 0 0
0 4 1 1 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 0
0 0 0 4 2 2 2 2 4 0
0 0 0 4 2 2 2 2 4 0
0 0 0 4 4 4 4 4 4 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F0A59D63110>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 4 4 4 4 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F0A59D627B0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 4 2 2 2 4 0 0 0 0
0 4 2 2 2 4 0 0 0 0
0 4 2 2 2 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 4 4 0
0 0 0 0 0 4 1 1 4 0
0 0 0 0 0 4 4 4 4 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F0A59D61F90>
<PIL.Image.Image image mode=RGB size=1340x1330 at 0x7F0A5AEC2170>Okay, here's my analysis of the provided input-output examples, formatted as a report:

**Perception of Elements:**

The task involves 2D grids containing colored pixels. The primary colors observed are yellow (4), blue (1), and red (2). The background is consistently white (0). The transformation seems to involve identifying rectangular shapes of uniform color (yellow in the examples) and altering the inner pixels of those shapes to a different color. The alteration pattern appears dependent on the shape's position within the grid.

**YAML Fact Block:**


```yaml
facts:
  - object: rectangle
    properties:
      - color: yellow (4)
      - shape: rectangular
      - contents: uniform
    actions:
      - fill_interior:
          conditions:
            - position: top-left
            - color: blue(1)
            - rows: 2
            - cols: 2
            - type: square
            - position: top-left
            - position: bottom-right
            - color: blue (1)
            - rows: 2
            - type: square
            - cols: 2
          conditions:
            - color: red (2)
            - type: rectangle
            - position: bottom-right
            - position: top-left
            - rows: 2

  - grid:
      properties:
        - background_color: white (0)
```


**Natural Language Program:**

1.  **Identify Rectangles:** Locate all rectangular regions of uniform color (yellow/4) within the input grid.
2.  **Conditional Interior Fill:** For each identified rectangle, apply the following logic:

    *   If the rectangle is in the top-left part of the grid, and it is composed of at least 2 rows, fill the inner 2x2 center of the rectangle with blue (1).
    *   If the rectangle is in the bottom-right part of the grid, and it is composed of at least two rows, fill the inner area that is 2 rows high rectangle with red (2).

The definition of the top-left/bottom-right "part" will be refined. It is apparent from the examples that the program should check for yellow rectangles and based on where those yellow rectangles are located within the grid, replace the inner contents with blue or red.

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
