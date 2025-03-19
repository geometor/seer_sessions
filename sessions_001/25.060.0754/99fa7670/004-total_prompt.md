# 99fa7670 • 004 • example_1 • investigate_coder

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

<PIL.Image.Image image mode=RGB size=384x384 at 0x7A174C702C50>

**output:**
```
0 0 0 0 0 0
0 0 2 2 2 2
0 0 0 0 0 2
0 3 3 3 3 3
0 0 0 0 0 3
0 0 0 0 0 3
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7A174C702ED0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves two 6x6 grids. The input grid contains two distinct colored pixels (red=2 and green=3) against a background of white (0). The output grid shows that the colored pixels have expanded to fill their respective rows and then extend downwards, filling the remaining rows below them. The expansion seems to occur in both directions from the original colored pixel.

**YAML Block (Facts):**


```yaml
objects:
  - id: red_pixel
    color: red (2)
    initial_position: (1, 2) # (row, col)
    shape: single pixel
  - id: green_pixel
    color: green (3)
    initial_position: (3, 1)
    shape: single pixel
  - id: background
    color: white (0)
    shape: 6x6 grid

actions:
  - type: expansion
    target: red_pixel
    description: Expands horizontally to fill the row, then vertically downwards.
  - type: expansion
    target: green_pixel
    description: Expands horizontally to fill the row, then vertically downwards

relationships:
   - red_pixel and green_pixel do not overlap during expansion.
   - expansion occurs within the bounds of the background grid.
```


**Natural Language Program:**

1.  **Identify colored pixels:** Locate all pixels in the input grid that are not white (0).
2.  **Horizontal Expansion:** For each colored pixel, expand it horizontally to the left and right edges of the grid, changing all pixels in that row to the color of the original pixel.
3.  **Vertical Expansion:** after the row expansion, expand each colored pixel downwards until each column is occupied.

In other words. For the row that a colored object is in, replace the entire row
with the color. Then take each column and fill downwards until you hit the
bottom of the grid.

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
