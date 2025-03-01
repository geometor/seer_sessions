# beb8660c • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
2 2 0
0 4 0
8 8 8
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7778516D14F0>

**output:**
```
0 0 4
0 2 2
8 8 8
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7778516D1450>
Okay, here's my analysis of the provided example, focusing on perception, object identification, and the transformation rule:

**Perception of Elements:**

The task involves a 3x3 grid of colored pixels. The colors are represented by single-digit integers.  The input and output grids have the same dimensions. The bottom row ( `8 8 8`) appears unchanged between input and output. The transformation seems to involve a 90 degree clockwise rotation of some, but maybe not all, elements.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    dimensions: 3x3
    elements: colored pixels
    element_type: integer (0-9)
  - object: bottom_row
    property: color, consistent
    value: 8 (azure)
    action: unchanged
  - object: top_left_pixel
    input_property: color, red(2)
    input_location: [0,0]
    output_property: color, white(0)
    output_location: [0,1]
  - object: top_middle_pixel
    input_property: color, red(2)
    input_location: [0,1]
    output_property: color, yellow(4)
    output_location: [0,2]
  - object: top_right_pixel
      input_property: color, white(0)
      input_location: [0,2]
      output_property: color, red(2)
      output_location: [1,2]
  - object: middle_left_pixel
      input_property: color, white(0)
      input_location: [1,0]
      output_property: color, white(0)
      output_location: [1,0]
  - object: middle_middle_pixel
      input_property: color, yellow(4)
      input_location: [1,1]
      output_property: color, red(2)
      output_location: [1,1]

  - transformation: rotation
    type: clockwise
    degrees: 90
    scope: "all pixels except bottom row"

```


**Natural Language Program:**

1.  **Identify the bottom row:** Observe the bottom row of the input grid. It remains unchanged in the output grid.
2.  **Rotate other elements:** Consider all other pixels *except* the bottom row. Rotate them 90 degrees clockwise.
3.  **Preserve Bottom Row:** Copy the bottom row from the input grid directly to the output grid without modification.

In essence, the transformation is a 90-degree clockwise rotation of the grid *excluding* the bottom row, which remains constant.

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
