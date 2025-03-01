# 54d82841 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 6 6 6 0 0 0 0
0 6 0 6 0 0 0 0
0 0 0 0 0 6 6 6
0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x744068E010D0>

**output:**
```
0 6 6 6 0 0 0 0
0 6 0 6 0 0 0 0
0 0 0 0 0 6 6 6
0 0 0 0 0 6 0 6
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 4 0 0 0 4 0
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x744068E008D0>

## train_2

**input:**
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x744068E01250>

**output:**
```
0 3 3 3 0
0 3 0 3 0
0 0 0 0 0
0 0 0 0 0
0 0 4 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x744068E45AD0>

## train_3

**input:**
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
0 8 0 8 6 6 6
0 0 0 0 6 0 6
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x744068E47850>

**output:**
```
0 0 0 0 0 0 0
0 8 8 8 0 0 0
0 8 0 8 6 6 6
0 0 0 0 6 0 6
0 0 4 0 0 4 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x744068E63DD0>
<PIL.Image.Image image mode=RGB size=1360x1074 at 0x7440707377D0>Okay, here's my analysis of the provided input-output examples:

**Perception of Elements:**

The task involves 2D grids where each cell contains a single digit representing a color. The input grids appear to have certain colored regions, and the output grids seem to mostly retain the input structure, but with the addition of a yellow (color 4) object at the bottom. The position of the new yellow object seems related to objects of other colours in the upper rows.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: variable (rows x columns)
      - cells: contain single-digit integers (0-9) representing colors

  - type: colored_region
    properties:
      - color:  integer (0-9) except 4
      - shape: contiguous block of same-colored cells
      location: variable

  - type: yellow_object
     properties:
        color: 4
        shape: single cell or two horizontally adjacent cells
        location: bottom row
actions:
  - description: add a yellow object
    details:  A new object with a color 4 (yellow) is placed on the last row.  Its position is related to the existence and position of other non-white, non-yellow objects in the grid

relationships:
  - input_grid: contains colored_regions
  - output_grid: contains original colored_regions and yellow object in the final row

```


**Natural Language Program:**

1.  **Identify colored regions:** Examine the input grid. Identify contiguous blocks of cells with the same color (excluding white/0).
2. **Determine number of coloured objects:** Count the objects in the input grid, if an object extends to the grid edge, that counts as an object
3.  **Create the output grid:** Copy the input grid to the output grid.
4. **Add yellow object to the bottom row.:** If there is only 1 object, place a single yellow pixel in the center of the last row, if the grid width is odd, if even offset by one to the left. If there are two or more objects, place two yellow pixels in last row below each object, matching their x position


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
