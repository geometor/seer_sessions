# 445eab21 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 4 4 4 4 4 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 2 2 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x76911EBFDE50>

**output:**
```
4 4
4 4
```

<PIL.Image.Image image mode=RGB size=128x128 at 0x76911EBFE030>
Okay, here's my analysis of the example input-output pair, structured as a report:

**Perception of Elements:**

The input grid contains two distinct objects:

1.  A large "C" shape composed of yellow (4) pixels.
2.  A smaller square/rectangle shape in the bottom-right corner composed of red (2) pixels.

The output grid contains only a 2x2 square of yellow (4) pixels. It appears the output extracts a sub-grid of the input related to the "C" object.

**YAML Fact Block:**


```yaml
objects:
  - id: C_shape
    color: yellow
    shape: C-like
    description: A larger structure resembling the letter C.
    bounding_box:
      top_left: [0, 1]
      bottom_right: [6, 6]

  - id: red_square
    color: red
    shape: square/rectangle
    description: smaller shape in bottom right
    bounding_box:
      top_left: [7, 7]
      bottom_right: [9, 9]

actions:
  - type: extract_subgrid
    target: C_shape
    description: Extracts a portion of the yellow C shape
    parameters:
        top_left_corner: [0,1] # relative to the overall input grid.
        subgrid_size: [2,2] # rows and columns.

relationships:
  - type: spatial
    description: The red square is spatially separated from the yellow C shape. The output only contains elements from C_shape.
```


**Natural Language Program:**

1.  Identify the bounding box of the yellow (4) "C" shape within the input grid. In this example, it is defined by the upper-left corner at row 0, column 1 and the lower right at row 6, column 6.

2.  Identify the upper-left corner of the c shape bounding box.

3. Extract a 2x2 subgrid from the input grid, starting at the yellow C shape's top-left corner.

4.  The extracted 2x2 subgrid is the output. Ignore all other parts of the input grid.

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
