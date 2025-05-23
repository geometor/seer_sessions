# 3bdb4ada • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1920x512 at 0x7DBFF232FA70>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0 4 0
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1920x512 at 0x7DBFF232F570>
Okay, let's analyze this input-output example.

**Perception of Elements:**

The task involves two grids: an input grid and an output grid. Both grids contain numerical values representing colors. The primary colors observed are yellow (4), azure (8), and white (0). The input grid contains three distinct horizontal rectangular blocks of color. The output seems to modify only some areas, by "poking" a hole into the colored blocks.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - name: input_grid
      - dimensions: 8x30
      - colors: [0, 4, 8]
  - type: grid
    properties:
      - name: output_grid
      - dimensions: 8x30
      - colors: [0, 4, 8]
  - type: rectangle
    properties:
      - color: yellow (4)
      - location: rows 1-3, columns 0-28
      - modification: alternating 0s in row 2
  - type: rectangle
    properties:
      - color: azure (8)
      - location: rows 5-7, columns 12-26
      - modification: alternating 0s in row 6
  - type: rectangle
    properties:
        - color: white (0)
        - location: all other cells
actions:
    - type: poke_holes
      description: introduce alternating white pixels, making checkerboard in the middle row of colored rectangles

```


**Natural Language Program:**

1.  **Identify Rectangles:** Locate horizontal rectangular blocks of uniform color within the input grid.
2.  **Target Middle Row:** For each identified rectangle, focus on its middle row.
3.  **Poke Checkerboard:** Within the middle row of each rectangle, alternate the existing color with white (0), starting with the original color and then 0, until the end of the block on that row.
4. **Keep the rest** Keep all pixels outside the colored rectangles, and any part of a color other than the middle line, as is.

Essentially, the transformation "pokes" an alternating pattern of white pixels (0) into the middle row of each colored rectangular block, creating a checkerboard effect within that row, while leaving the rest of the grid unchanged.

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
