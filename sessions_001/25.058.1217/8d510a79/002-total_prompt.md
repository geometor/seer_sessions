# 8d510a79 • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 2 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 2 0 0 1 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x741F72B8FF70>

**output:**
```
0 0 1 0 0 0 1 0 0 0
0 0 0 0 0 0 1 0 0 0
0 2 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0 2
0 2 0 0 0 0 0 0 0 2
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 2 0 0 0 0
0 1 0 0 0 2 0 0 1 0
0 1 0 0 0 0 0 0 1 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x741F72B8FBB0>

## train_2

**input:**
```
0 2 0 1 0 0 0 0 0 0
0 0 0 0 0 2 0 1 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 2
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 2 0 1 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x741F72B1B7F0>

**output:**
```
0 2 0 1 0 0 0 1 0 0
0 2 0 0 0 2 0 1 0 0
0 2 0 0 0 2 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 2 0 0 0 0 2 0 0 2
0 2 0 0 0 0 2 0 0 2
0 0 0 0 1 0 2 0 0 0
0 0 0 0 1 0 2 0 0 0
0 0 1 0 1 0 2 0 1 0
0 0 1 0 1 0 0 0 1 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x741F72B1A850>
<PIL.Image.Image image mode=RGB size=1340x1330 at 0x741F733F5C70>Okay, here's my analysis of the provided input-output pairs, structured as requested:

**Perception of Elements:**

The task involves 2D grids containing pixels of different colors (represented by digits 0-9).  The most prominent colors are white (0), blue (1), red (2), and gray (5).  The gray row appears to be a static, dividing line. The transformation seems to involve a vertical mirroring or reflection of the colored pixels (blue and red) above and below the gray line, but with some nuanced behavior. Specifically, isolated colored pixels are mirrored, but strings of colored pixels, those which are adjacent, seem to replicate but maintaining the original colors (blue and red in our examples).

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: 2D array of pixels
    elements:
      - color: white
        value: 0
      - color: blue
        value: 1
      - color: red
        value: 2
      - color: gray
        value: 5
    properties:
      - width: 10
      - height: 10
  - type: object
    description: contiguous block of single colored pixel
  - type: object
    description: contiguous block of multiple colored pixels
  - type: static_element
    description: horizontal gray line
    row_index: 5 # Row index where the gray line is consistently located
  - type: transformation
    description: vertical mirroring of isolated colored pixels
  - type: transformation
    description: vertical replication of multiple, adjacent, colored pixels
  - type: constraint
      description: The gray row remains unchanged.

```


**Natural Language Program:**

1.  **Identify the static gray row:** Locate the row filled with gray (5) pixels. This row acts as a mirror/replication line.

2.  **Iterate through the other rows:** For each row *above* the gray row, examine each pixel.

3.  **Mirror isolated colored pixels:**
    *   If a pixel is blue (1) or red (2), and its adjacent vertical pixels, *within the same region* (above the gray line or below), are white (0), check the corresponding position in its "reflection row" determined by the position's distance from the gray row.
    *   The "reflection row" for row `r` above the static gray row at `s` is `s + (s - r)`. The "reflection row" for row `r` below the static gray row at `s` is `s - (r - s)`.
    *   If that corresponding pixel in the mirrored row is white (0) in the input, change it to the same color (1 or 2, correspondingly) as the source pixel.

4.  **Replicate strings of colored pixels**:
    * If a pixel is blue(1) or red(2) and is adjacent, vertically, to another pixel of the *same color*, copy that entire vertical string of pixels to the region determined by its distance from the gray row.
    *   The "reflection row" for the string of pixels is calculated using the start and end point of the string using the formula in point 3 above.

5.  **Gray Row Preservation:** The gray row remains unchanged during the transformation.

Essentially the input grid is mirrored vertically around the gray row with a special rule, that the strings of adjacent colored pixels do not change, and are copied from one area of the grey row to another.

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
