# 6cdd2623 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 2 2 0 0 0 0 3 0 0 0 0 0 2 0 0 0 0
2 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 2 0 5 2 0 5 0 0 0 0 0 2 0 0 0
0 0 0 0 5 5 0 0 0 0 0 0 0 0 2 0 0 0 0 0 2 0
5 0 0 2 0 2 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 2 0 0 0 2 0 0 2 0 0 0 0 0 0 0 2 0 5 0
0 0 2 0 0 0 0 0 0 5 5 0 0 5 0 0 0 0 0 2 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0
3 0 0 5 5 0 2 5 0 0 0 0 0 0 0 0 0 0 0 0 2 3
0 0 0 0 0 0 0 0 0 2 0 2 5 0 5 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 5 0 0 3 0 0 0 0 0 5 0 5 0 0
```

<PIL.Image.Image image mode=RGB size=1408x704 at 0x7A43FD927850>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1408x704 at 0x7A43FD927A50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid contains various colors (represented by numbers 0-9), while the output grid seems to simplify the input significantly, retaining only one color (green/3) in a specific pattern. The most prominent change is the replacement of all non-green pixels with background color and the formation of a green vertical line, and a green horizontal line through the original green pixels.

**YAML Fact Documentation:**


```yaml
facts:
  - type: grid
    description: Input and output are 2D grids of pixels.
  - type: colors
    description: Pixels have colors represented by integers 0-9.
  - type: observation
    description: Output grid predominantly uses color 0 (background).
  - type: observation
    description: Output grid highlights color 3 (green).
  - type: object
    color: 3
    description: Green pixels in the input grid.
  - type: action
    description: all other colors change to white (0).
  - type: pattern
    description: Green pixels form a vertical and horizontal intersecting line.
  - type: location
    description: The horizontal line appears to be located on row 8 of input grid (the row with multiple green pixels in it).
  - type: location
    description: Vertical line of green appears to occupy column 11 in both input and output.
```


**Natural Language Program:**

1.  **Identify Green:** Locate all pixels in the input grid with the color value 3 (green).
2.  **Background:** Change all the non-green pixels in the input grid to color 0 (white, the background).
3.  **Vertical Line**: Draw a vertical line of green (3) color through all rows, on the column of input grid that has multiple green pixels present in it.
4.  **Horizontal Line:**  Draw a horizontal line using color 3 (green) through all columns, across the row that has multiple green colors in it.

Essentially, the transformation isolates and emphasizes the location of existing green pixels by creating lines, vertical and horizontal using their original location and changing other colors to the background.

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
