# 99fa7670 • 002 • example_4 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0
0 0 2 0 0 0
0 0 0 0 0 0
0 3 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7A174C75CED0>

**output:**
```
0 0 0 0 0 0
0 0 2 2 2 2
0 0 0 0 0 2
0 3 3 3 3 3
0 0 0 0 0 3
0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7A174C74FF50>

## train_2

**input:**
```
0 0 0
0 6 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7A174C74C5D0>

**output:**
```
0 0 0
0 6 6
0 0 6
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7A17540FB9D0>

## train_3

**input:**
```
0 0 0 0 0 0
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 5 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7A17540FBDD0>

**output:**
```
0 0 0 0 0 0
0 8 8 8 8 8
0 0 0 0 0 8
0 0 0 0 0 8
0 0 0 5 5 5
0 0 0 0 0 5
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7A17540FB950>

## train_4

**input:**
```
0 0 0 0 0
0 0 8 0 0
0 0 0 0 0
0 7 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x448 at 0x7A17540FBC50>

**output:**
```
0 0 0 0 0
0 0 8 8 8
0 0 0 0 8
0 7 7 7 7
0 0 0 0 7
0 0 6 6 6
0 0 0 0 6
```

<PIL.Image.Image image mode=RGB size=320x448 at 0x7A17540FBCD0>
<PIL.Image.Image image mode=RGB size=1440x976 at 0x7A174C75D550>Okay, here's my analysis of the provided examples, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The task involves 2D grids where each cell contains a single digit representing a color. The input grids contain a few colored cells, with the majority being '0' (white). The transformation seems to involve expanding the non-zero colored cells. The shape of the input grid is identical to its output grid.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: rows x columns (variable)
      - cells: contain integer values (0-9) representing colors

  - type: colored_cell
    properties:
      - color: integer value (1-9)
      - location: row, column index within the grid

actions:
  - type: expand
    properties:
      - direction: horizontal and vertical
      - extent: to the right and down

relationships:
  - colored_cells are contained within the grid
  - expansion of colored_cells modifies the grid
```


**Natural Language Program:**

1.  **Identify** all non-zero colored cells within the input grid.
2.  For each identified colored cell:
    *   **Extend** the cell's color horizontally to the right edge of the grid.
    *   **Extend** the color of all cells in this extended row, downwards to fill the input grid shape.

Essentially, each non-zero cell's color is propagated rightward and then downward, overwriting any existing colors. The key is the order: right, then fill down from the extended row.

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
