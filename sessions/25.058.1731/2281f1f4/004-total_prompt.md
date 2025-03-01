# 2281f1f4 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
5 0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36044BF2D0>

**output:**
```
5 0 0 5 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 2 0 0 0 2 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 2 0 0 0 2 0 5
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36044BF1D0>
Okay, here's my analysis of the provided input-output example pair, formatted as a report:

**Perception of Elements:**

The task involves a 10x10 grid. The primary colors involved appear to be gray (5), white (0), and red (2). The input grid contains a scattering of gray pixels, primarily along the top and right edges, with the rest being white. The output grid maintains the gray pixels in their original positions but introduces red pixels in a specific pattern. The red pixels replace some but not all of the white pixels on rows with some grey pixels.

**YAML Fact Documentation:**


```yaml
facts:
  - object: grid
    type: 2D array
    dimensions: 10x10
    elements: pixels
    colors: [gray, white, red]

  - object: gray_pixel
    color: gray (5)
    property: static (position unchanged)

  - object: white_pixel
    color: white (0)
    property: can_change (to red)

  - object: red_pixel
    color: red (2)
    property: replaces_white (under_certain_conditions)
    condition_for_replacement:
        - on_row_with_grey: true
        - column_index_where_grey_is_present: true

  - action: replacement
    subject: white_pixel
    object: red_pixel
    rule: "If a white pixel is in same row and same column where gray pixels present, change it to red"
```


**Natural Language Program:**

1.  **Identify Static Elements:** Locate all gray (5) pixels in the input grid. Their positions will remain unchanged in the output grid.

2.  **Identify Target Rows:** Find the rows that contain at least one gray pixel.

3.  **Identify Target Columns:** Find the columns containing at least one gray pixel.

4. **Conditional Replacement:** For rows and columns identified, change those white pixels to red.

5.  **Preserve Unchanged:** All other pixels (white pixels in rows and columns not containing grey) remain unchanged (white, 0).

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
