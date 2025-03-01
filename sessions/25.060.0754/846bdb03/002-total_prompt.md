# 846bdb03 • 002 • example_4 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 1 0 0 0 0 0 0 0
0 0 0 2 0 1 1 1 0 0 0 0 0
0 0 0 2 2 1 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 0 0 4
0 0 0 0 0 2 0 0 0 0 0 0 1
0 0 0 0 0 2 0 0 0 0 0 0 1
0 0 0 0 0 2 0 0 0 0 0 0 1
0 0 0 0 0 2 0 0 0 0 0 0 1
0 0 0 0 0 4 0 0 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x7A174C679FD0>

**output:**
```
4 0 0 0 0 0 0 4
2 2 2 0 1 0 0 1
2 0 2 0 1 1 1 1
2 0 2 2 1 0 0 1
2 0 0 2 0 0 0 1
4 0 0 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=512x384 at 0x7A174C7005D0>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 8 0 8 0 0 0
0 0 0 0 3 3 3 8 8 8 0 0 0
0 0 0 0 0 3 0 8 0 8 0 0 0
0 0 0 0 0 3 3 8 8 8 0 0 0
0 0 0 0 0 0 0 8 0 8 0 0 0
0 4 0 0 0 0 0 0 4 0 0 0 0
0 8 0 0 0 0 0 0 3 0 0 0 0
0 8 0 0 0 0 0 0 3 0 0 0 0
0 8 0 0 0 0 0 0 3 0 0 0 0
0 8 0 0 0 0 0 0 3 0 0 0 0
0 8 0 0 0 0 0 0 3 0 0 0 0
0 4 0 0 0 0 0 0 4 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x7A174D298D50>

**output:**
```
4 0 0 0 0 0 0 4
8 8 0 8 0 3 0 3
8 8 8 8 3 3 3 3
8 8 0 8 0 3 0 3
8 8 8 8 3 3 0 3
8 8 0 8 0 0 0 3
4 0 0 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=512x448 at 0x7A17540FB950>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0 0 0 0 0
0 0 2 0 0 0 0 1 0 0 0 0 0
0 0 2 0 0 0 0 1 0 0 0 0 0
0 0 4 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 2 0 0 0 0 0 0 0
0 0 0 0 1 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x7A17540FB8D0>

**output:**
```
4 0 0 0 0 4
2 0 2 1 1 1
2 2 2 1 0 1
4 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=384x256 at 0x7A17540FB9D0>

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0 4 0 0
0 0 0 0 0 7 0 0 0 0 3 0 0
0 0 0 0 0 7 0 0 0 0 3 0 0
0 0 0 0 0 7 0 0 0 0 3 0 0
0 0 0 0 0 4 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 3 0 0 0 0
0 0 0 0 0 7 7 3 3 0 0 0 0
0 0 0 0 0 0 7 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=832x832 at 0x7A17540FB850>

**output:**
```
4 0 0 0 0 4
7 7 7 0 3 3
7 7 7 3 3 3
7 0 7 0 3 3
4 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=384x320 at 0x7A17540FBF50>
<PIL.Image.Image image mode=RGB size=3488x1360 at 0x7A1754064250>Okay, let's analyze the provided input-output pairs to understand the transformation rule.

**Perception of Elements:**

The task involves 2D grids containing single-digit integers (0-9), representing different colors. The transformation seems to involve a significant reduction in grid size and a rearrangement of the colored objects within the grid.  There appear to be vertical "stems" or "lines" of different colors that are being compressed or summarized in the output. The corners seem important, particularly the color yellow (4).

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: variable (changes between input and output)
      - cells: contain integer values (0-9) representing colors
  - type: stem
    properties:
      - color: varies (red, blue, green, azure, orange)
      - orientation: vertical
      - length: variable
      - connected: True #pixels are adjacent
  - type: corner
    properties:
      - color: yellow (4)
      - position: top-left, top-right, bottom-left, bottom-right
      - persistent: True # appears in both input and output

actions:
  - compress: reduces the dimensions of the grid
  - rearrange: positions objects within the new grid dimensions
  - summarize: captures the essence of vertical stems in a condensed form

relationships:
  - stems: adjacent to other stems of different colors
  - corners: mark boundaries of the output grid
  - input-output:  a mapping where the input grid is transformed to the output grid
```


**Natural Language Program:**

1. **Identify Corners:** Locate the yellow (4) pixels in the four corners of the *input* grid. These will define the corners of the smaller, *output* grid. If corner pixels of value 4 do not exist, ignore this rule.

2. **Determine Output Dimensions:** The output grid's dimensions are defined by drawing horizontal and vertical lines between opposite yellow corner pixels. If there are no yellow corners, the output size is the minimum rectangle enclosing all non-zero pixels.

3. **Summarize Vertical Stems:** For each non-zero, non-corner column in the input, identify contiguous vertical "stems" of the same color.  A "stem" is a vertical sequence of one or more pixels of the same color.

4. **Place Stems in Output:**  Represent each identified stem within the output grid's corresponding column.
    - The stem is represented by the same color.
    - Replicate that color in the *output* grid, filling a rectangle in the output column. The rectangle fills the whole column, except the top and bottom row if yellow pixels were present.

5. **Preserve corner elements**: replicate the yellow pixels in the corners to the output grid.

In essence, the transformation extracts a compressed representation of the vertical color stems, framed by the corner pixels. If corner pixels are missing, create the smallest bounding box for the stem elements.

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
