# 56ff96f3 • 024 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x384 at 0x7B4BFE14CA50>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 7 7 7 7 0 0 0
0 7 7 7 7 7 7 7 0 0 0
0 7 7 7 7 7 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x384 at 0x7B4BFE14F950>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid (2D array) of pixels, where each pixel has a color value represented by an integer (0-9). The primary colors observed are white (0) and orange (7). The input grid contains isolated orange pixels, while the output grid shows a filled rectangular area of orange pixels. The transformation seems to involve identifying the locations of the orange pixels and filling the area between, encompassing any gaps to form a solid rectangle, or perhaps finding the orange pixel bounds and creating a new shape.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: [6, 11] # Height, Width
      - cell_values: integers (0-9)
  - type: pixel
    properties:
      - color:
          - white (0)
          - orange (7)
      - location: [row, column]
  - type: rectangle #inferred
    properties:
        - top_left: [row, col]
        - bottom_right: [row, col]
        - color: orange (7)

actions:
  - name: identify_orange_pixels
    description: Locate all pixels with a value of 7.
  - name: create_bounding_rectangle
    description:  Determine minimum and maximum row and col of orange pixels, form a rectangle defined by opposite corners.
  - name: fill_rectangle
    description: Set all pixel values within the bounding rectangle to 7.

relationships:
  - input_grid: Contains scattered orange pixels.
  - output_grid: Contains a filled orange rectangle encompassing the original orange pixels.
```


**Natural Language Program:**

1.  **Identify:** Find all orange pixels (value 7) in the input grid.
2.  **Bound:** Determine the minimum and maximum row and column indices among the identified orange pixels. This defines the top-left and bottom-right corners of a rectangle.
3.  **Fill:** In the output grid, set all pixels within the boundaries of the rectangle (inclusive) to orange (value 7). Pixels outside this rectangle remain unchanged (white/0). The input grid dimensions are maintained.

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
