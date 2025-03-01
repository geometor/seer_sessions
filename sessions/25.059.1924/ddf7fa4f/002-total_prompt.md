# ddf7fa4f • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 2 0 0 6 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0
0 0 0 0 5 5 5 5 0 0
0 5 5 0 5 5 5 5 0 0
0 5 5 0 5 5 5 5 0 0
0 5 5 0 0 0 0 0 0 0
0 5 5 0 0 0 0 5 5 5
0 5 5 0 0 0 0 5 5 5
0 0 0 0 0 0 0 5 5 5
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x71663D535250>

**output:**
```
0 0 2 0 0 6 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 0 0
0 0 0 0 6 6 6 6 0 0
0 2 2 0 6 6 6 6 0 0
0 2 2 0 6 6 6 6 0 0
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 8 8 8
0 2 2 0 0 0 0 8 8 8
0 0 0 0 0 0 0 8 8 8
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C5C8D0>

## train_2

**input:**
```
0 1 0 0 0 4 0 0 7 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 0 0 0 5 5 5
5 5 5 5 0 0 0 5 5 5
5 5 5 5 0 0 0 5 5 5
5 5 5 5 0 0 0 5 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C5DD50>

**output:**
```
0 1 0 0 0 4 0 0 7 0
0 0 0 0 0 0 0 0 0 0
1 1 1 1 0 0 0 7 7 7
1 1 1 1 0 0 0 7 7 7
1 1 1 1 0 0 0 7 7 7
1 1 1 1 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0 0 0
0 0 0 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635CD8C50>

## train_3

**input:**
```
0 1 0 0 0 6 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0
0 5 5 0 0 0 0 5 5 5
0 5 5 0 0 0 0 5 5 5
0 0 0 5 5 5 0 0 0 0
0 0 0 5 5 5 0 0 0 0
0 0 0 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635CDB250>

**output:**
```
0 1 0 0 0 6 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0 0 0
0 1 1 0 0 0 0 7 7 7
0 1 1 0 0 0 0 7 7 7
0 0 0 6 6 6 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C4CE50>
<PIL.Image.Image image mode=RGB size=2048x1360 at 0x71663577D0D0>Okay, let's analyze the provided input-output pairs to discern the underlying transformation rule.

**Perception of Elements:**

*   **Grids:** The input and output are both 10x10 grids.
*   **Colors:** Each cell in the grid has a color, represented by an integer (0-9). We are given the mapping of integers to colors.
*   **Objects:** We can consider contiguous blocks of the same color as objects.
*   **Background:** The color 0 (white) appears to be the background.
*   **Transformation:** The transformation seems to involve replacing certain objects/colors with other colors based on the object and its surrounding. It maintains the background. The single color objects existing in the top row remains the same through the transformation.

**YAML Block - Facts:**


```yaml
objects:
  - description: Single-color regions in the top row.
    properties:
      color: Varies (1, 2, 4, 6, 7, 8).
      location: Top row of the grid.
      change: color stays the same.
  - description: Multi-color regions in rows other than the top row
    properties:
      color: grey (5)
      location: below the top row.
      change: changes to color of the signle-color object in same column.

background:
  color: 0 (white)
  change: none
```


**Natural Language Program:**

1.  Identify "single-color objects" in the top row of the input grid. These are single pixels.
2.  For the rest of the grid (rows below the top row), any object with colors other than the colors found in the top row are examined.
3. These object's colors are changed. The new color for the changed object is determined by looking up the single-color pixel on the top row that resides in the same column.
4.  The background (color 0) remains unchanged.
5. The single-color objects in the top row are unchanged.

In essence, the transformation "recolors" or "overlays" the existing objects below the top row. The colors of the objects in the top row dictates the colors of the other objects.

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
