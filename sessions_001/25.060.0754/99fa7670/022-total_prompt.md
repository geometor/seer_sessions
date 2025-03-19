# 99fa7670 • 022 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0
0 0 8 0 0
0 0 0 0 0
0 7 0 0 0
0 0 0 0 0
0 0 6 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x448 at 0x7A1754163ED0>

**output:**
```
0 0 0 0 0
0 0 8 8 8
0 0 0 0 8
0 7 7 7 7
0 0 0 0 7
0 0 6 6 6
0 0 0 0 6
```

<PIL.Image.Image image mode=RGB size=320x448 at 0x7A1754162150>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid contains isolated non-zero pixels, while the output grid shows these non-zero pixels "expanding" to the right edge of the grid, but only on the row in which the original pixel exists. The background (0, or white) remains unchanged.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - width: 5
      - height: 7
      - cells: integers (0-9) representing colors
  - type: pixel
    properties:
      - color: integer (0-9)
      - position: (row, column)
  - type: non_zero_pixel
    inherits: pixel
    properties:
       - original_color: value before transformation
       - original_position: location before transformation

actions:
  - name: expand_right
    input: non_zero_pixel
    output: fills cells to right of the pixel and on the same row with pixel's color.

relationships:
  - type: spatial
    description: Pixels are arranged in a 2D grid.
  - type: transformation
    description: Non-zero pixels cause expansion of their color to the right edge of their row.

```


**Natural Language Program:**

1.  **Identify** all non-zero pixels in the input grid.
2.  For each non-zero pixel:
    *   Locate the pixel's row.
    *    Starting with the pixel's original column, replace pixel values to right and on the same row, with the non-zero pixel's color, until reaching the right edge of the grid.
3. All other pixels (with original value 0) remain unchanged.

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
