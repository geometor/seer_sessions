# 6b9890af • 008 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1344x1152 at 0x7A43F5EB38D0>

**output:**
```
2 2 2 2 2 2 2 2
2 0 0 8 8 0 0 2
2 0 0 8 8 0 0 2
2 8 8 8 8 8 8 2
2 8 8 8 8 8 8 2
2 0 0 8 8 0 0 2
2 0 0 8 8 0 0 2
2 2 2 2 2 2 2 2
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x7A43F5EEF8D0>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

*   The input is a larger grid (21x18) containing two distinct shapes: a small azure (8) shape at the top and a larger red (2) hollow square-like shape in the middle.
*   The output is a smaller grid (8x8) that seems to combine elements of both shapes from the input.
*   The output grid's border is entirely red (2).
*   The output grid has two 3x2 azure (8) rectangles inside, placed symmetrically, surrounded by 0, except the outside border.
*	  It seems that the output grid is a zoomed and cropped part of the input grid.

**YAML Block (Facts):**


```yaml
objects:
  - id: shape_1
    type: rectangle
    color: azure (8)
    properties:
      - width: variable
      - height: variable
      - position: top-center

  - id: shape_2
    type: hollow_rectangle
    color: red (2)
    properties:
      - width: variable
      - height: variable
      - position: center

  - id: output_grid
    type: grid
    color: mixed
    properties:
     - width: 8
     - height: 8
     - border_color: red(2)

actions:
  - type: crop_and_zoom
    input: input_grid
    output: output_grid
    parameters:
      - focus: shape_1 and shape_2
      - maintain relative position and border.

relationships:
  - type: contains
    from: input_grid
    to: [shape_1, shape_2]

  - type: combined.
    from: [shape_1,shape_2]
    to: output_grid.
```


**Natural Language Program:**

1.  **Identify Objects:** Locate the azure (8) rectangle and the red (2) hollow rectangle within the input grid.
2.  **Define Output Size:** Create an 8x8 output grid.
3.  **Create Border**: Make the external border of output with red(2).
4.  **Crop and Zoom:** Extract a section from input focused on the azure rectangle.
5. **Combine:** Incorporate the azure rectangle, with the relative position inside the border in output grid.
6. **Fill**:  Fill 0 between the azure rectangle and the border.

In simpler terms: The transformation extracts a region around the azure and red shapes in the input, creates a smaller 8x8 grid with a red border, and positions a transformed/resized versions of azure shapes within this new grid, keeping some relative positioning and filling with white color.

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
