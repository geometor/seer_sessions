# 834ec97d • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 2 0
0 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7D67CBDADAD0>

**output:**
```
0 4 0
0 2 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7D67CBDAC3D0>

## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7D67CBDAC850>

**output:**
```
4 0 4 0 4
4 0 4 0 4
4 0 4 0 4
0 0 6 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7D67CBDAD1D0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7D67CBDAE8D0>

**output:**
```
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
4 0 4 0 4 0 4 0 4
0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7D67CBDAD9D0>
<PIL.Image.Image image mode=RGB size=1216x1232 at 0x7D67CBDADED0>Okay, here's my analysis of the provided examples, structured as requested:

**Perception of Elements:**

The task involves 2D grids where each cell contains a single digit representing a color. The primary element is a single colored pixel (non-white, value > 0) within a grid of otherwise white (0) pixels. The transformation seems to involve adding yellow (4) pixels in a specific pattern related to the position of the initial colored pixel. The size of the grid appears to expand in at least one case.

**YAML Fact Block:**


```yaml
facts:
  - object: grid
    properties:
      - type: 2D array
      - values: integers (0-9) representing colors
      - size: variable
  - object: colored_pixel
    properties:
      - color: non-white (value > 0)
      - location: row and column index within the grid
    actions:
      - identified: single instance per grid
  - object: yellow_pixels
    properties:
       - color: yellow (value = 4)
    actions:
      - added: to the output grid based on colored_pixel location
    relationships:
       -  pattern:  yellow fills the entire first row and columns of index equal to "colored_pixel column index".
```


**Natural Language Program:**

1.  **Identify** the single non-white pixel (the "colored pixel") in the input grid and note its row and column indices.
2.  **Create** an output grid. It has the dimensions as the number of columns of the input, applied both as rows and columns.
3.  **Copy** the colored pixel from the input grid to its original location in the output grid.
4.  **Fill** all cells in the first row of output grid with the value 4 (yellow).
5. **Fill** cells in the columns with index equal to the "colored\_pixel column index" with the value 4 (yellow).


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
