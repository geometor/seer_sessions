# 56ff96f3 • 006 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B4BFE15C9D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0
0 1 1 1 1 1 1 0 0 0
0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B4BFDB42A50>
Okay, let's analyze this input-output example pair to discern the transformation rule.

**Perception of Elements:**

*   The input and output are both 10x10 grids.
*   The input grid contains single pixels of color blue (1) and red (2) on a background of white (0).
*    The output grid shows rectangular blocks of blue (1) and red (2) replacing the single input pixels, all on white background.
*    The blue and red blocks appear to be centered on the original pixel locations.
*   The blue and red blocks are three pixels high, and the width stretches from the colored pixel in the input to to the left edge (exclusive)

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    background_color: white (0)

  - type: pixel
    properties:
      color:
        - blue (1)
        - red (2)
      location:
        - row: [1,3,5,7]
          col: [6,1,3,7]

  - type: block
    properties:
      color:
        - blue (1)
        - red (2)
      shape: rectangle
      dimensions: height varies. width varies
      anchor:  # the relationship of the input pixel location and output shape
          row: same as corresponding input pixel.
          col: centered on the original input, extends to the left.

actions:
- type: transform_pixel
  input:  single pixel
  output: rectangle of pixels
  transformation_rule: extends the single color into a rectangle shape, centered on initial position, height fixed and length is to column 0.

relationships:
  - object1: input pixel
    object2: output block
    relation: one-to-one correspondence in color
    spatial_relation: output block is centered on the input pixel's original location.

```


**Natural Language Program:**

1.  **Identify** all non-white pixels (blue and red) in the input grid.
2.  For each identified pixel:
    *   Create a rectangle of the same color.
    *    Make height = 3
    *   Determine the column index of the original pixel.
    *   Extend the rectangle from column 0 of the input (exclusive) to the initial column, keeping the color constant.
3.  Replace the background with white (0) where there are no colored rectangles.
4. Return the grid.


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
