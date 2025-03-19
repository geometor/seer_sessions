# 8e1813be • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 4 4 4 4 4 4 4
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 8 8 8 8 8 8 8
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```

<PIL.Image.Image image mode=RGB size=960x1152 at 0x7F2DF795FCD0>

**output:**
```
2 2 2 2 2 2
1 1 1 1 1 1
3 3 3 3 3 3
4 4 4 4 4 4
8 8 8 8 8 8
6 6 6 6 6 6
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7F2DF795E0D0>

## train_2

**input:**
```
0 0 0 0 0 2 0 0 4 0
0 5 5 5 0 2 0 0 4 0
0 5 5 5 0 2 0 0 4 0
0 5 5 5 0 2 0 0 4 0
0 0 0 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
0 0 1 0 0 2 0 0 4 0
```

<PIL.Image.Image image mode=RGB size=640x768 at 0x7F2DF795DCD0>

**output:**
```
1 2 4
1 2 4
1 2 4
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F2DFF3FBCD0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 0 5 5 5 5 0 2
0 0 0 0 0 0 5 5 5 5 0 0
0 0 0 0 0 0 5 5 5 5 0 0
8 8 8 8 8 0 5 5 5 5 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7F2DF79E0B50>

**output:**
```
2 2 2 2
8 8 8 8
4 4 4 4
1 1 1 1
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7F2DFF3FBF50>
<PIL.Image.Image image mode=RGB size=2496x1616 at 0x7F2DFF3FA6D0>Okay, here's my analysis of the provided examples, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The task involves transforming grids of colored pixels. The input grids are generally larger and more complex than the output grids. The output grids seem to be a simplified or extracted version of the input grids, retaining only certain colors and often reducing the overall size. The background is always white (0). There are distinct colored regions or "objects."

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: variable
      - cells: colored pixels (0-9)
  - type: colored_region
    properties:
      - color: integer (0-9)
      - shape: contiguous block

actions:
  - select:
    description: Identify specific colored regions.
    criteria:
      - color: not 0 (background)
      - uniqueness: appears only once in each input
      - complete row: occupies a full horizontal line on the grid, might only be part of a row.
  - extract:
      description: Copy the selected colored regions
  - compose:
    description: Arrange the extracted regions into a new grid.

relationships:
  - input_grid_contains: colored_regions
  - output_grid_composed_of: extracted_colored_regions
```


**Natural Language Program:**

1.  **Identify Target Colors:** Examine the input grid and identify the colors that *completely fill one or more rows, and where the remaining pixels on that row are all 0*. Also the colors should be unique. For example, if color 2 appears twice as complete rows, ignore them.
2.  **Extract Rows:** For each target color identified, extract *one* full row of that color from the input grid. The width of the extracted row should be the same as the number of non-zero pixels in the original row.
3.  **Compose Output:** Stack the extracted rows vertically, in the order they appear top-to-bottom in the input, to create the output grid.

In summary, the process finds rows that are solid blocks of the *same* color (not background) and are unique within the input grid, extracts one instance of those rows, removes background, and combines.

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
