# ea786f4a • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x716635C5FDD0>

**output:**
```
0 3 3 3 3 3 0
3 0 3 3 3 0 3
3 3 0 3 0 3 3
3 3 3 0 3 3 3
3 3 0 3 0 3 3
3 0 3 3 3 0 3
0 3 3 3 3 3 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x716635C5DE50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a 2D grid of pixels, where each pixel has a color value represented by an integer. The input grid appears to have a single "0" (white) pixel in the center, surrounded by "3" (green) pixels. The output grid transforms the input by creating a symmetrical cross or plus-shape pattern of "0" (white) pixels, extending from the center to the edges.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      - width: 7
      - height: 7
      - cells: pixels with integer values
  - name: pixel
    type: grid cell
    properties:
       - color: integer (0 or 3)

actions:
 - name: find_center
   description: locate the pixel at the center of the grid
 - name: extend_color
   description: change color of the pixels along horizontal, and vertical from center
  
relations:
  - subject: center pixel
    relation: surrounded by
    object:  pixels of color 3
  - subject: output grid
    relation: symmetrical
    object: about center
```


**Natural Language Program:**

1.  **Find the Center:** Locate the center pixel of the input grid. In this 7x7 grid, the center is at coordinates (3, 3) (zero-indexed).
2.  **Propagate the Center Color:** Change the color of every pixel that lies on either the same row, or the same column of the central pixel to the color of the central pixel.
3. All other pixels remain unchanged.

In essence, the transformation takes the color of the central pixel and extends it outwards in horizontal and vertical lines to create a cross shape.

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
