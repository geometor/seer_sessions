# 2204b7a8 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 3 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 3 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 3 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360454C5D0>

**output:**
```
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 2 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 1 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 1 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360455DCD0>

## train_2

**input:**
```
4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 7 7 7
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360455FCD0>

**output:**
```
4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 4 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 0 0 0
7 7 7 7 7 7 7 7 7 7
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C3604579850>

## train_3

**input:**
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 3 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9 9 9
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360457ACD0>

**output:**
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 9 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9 9 9
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360BFEB3D0>
<PIL.Image.Image image mode=RGB size=2000x1330 at 0x7C360BFEB850>Okay, here's my analysis of the provided input-output examples, structured as requested:

**Perception of Elements:**

The task involves 2D grids (matrices) of single-digit integers, where each integer represents a color. The input grids appear to have specific colored borders (top and bottom rows) and scattered single-colored pixels within the grid. The output grids maintain the border colors and transform the scattered interior pixels. The transformation seems to involve changing the color of the scattered interior pixels to match the color of the top border if above the main diagonal, and to the color of the bottom border if below the main diagonal.

**YAML Block - Facts:**


```yaml
objects:
  - grid:
      type: 2D array
      properties:
        rows: integer
        columns: integer
        cells: integer (representing colors)
        top_border_color: integer
        bottom_border_color: integer
        interior_pixels: list of (row, column, color) tuples

actions:
  - color_change:
      input: grid
      parameters:
          pixel: (row, column)
          new_color: integer
      description: Changes the color of a specified pixel.

relationships:
  - spatial:
    - above_main_diagonal:
        description: A pixel is above the main diagonal if its row index is less than its column index.
    - below_main_diagonal:
        description: A pixel is below the main diagonal if its row index is greater than its column index.
    - on_main_diagonal:
        description: A pixel is on the main diagonal if its row index is equal to its column index.

```


**Natural Language Program:**

1.  **Identify Borders:** Determine the colors of the top and bottom rows of the input grid. These are the "target colors."
2.  **Iterate Interior Pixels:** For each pixel in the input grid that is *not* in the top or bottom row:
3.  **Check Diagonal Relationship:**
    *   If the pixel's row index is less than its column index (above the main diagonal), change its color to the top border color.
    *   If the pixel's row index is greater than its column index (below the main diagonal), change its color to the bottom border color.
    *    If on the main diagonal, leave its original color.
4. **Preserve Borders:** The top and bottom rows of the grid remain unchanged.

In essence, the rule uses the main diagonal of the grid as a dividing line. Scattered pixels above the diagonal adopt the top border's color, and those below adopt the bottom border's color. The border colors themselves are copied without modification. Pixels which lay exactly on the main diagonal will also not be changed.

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
