# 00d62c1b • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 3 3 0 3 3 0 3 0 0
3 0 0 3 0 0 3 0 3 0
0 0 0 3 0 0 3 3 0 0
0 0 0 3 0 0 3 0 0 0
0 0 0 3 0 0 3 0 0 0
0 0 0 0 3 3 0 3 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC253D4EFD0>

**output:**
```
0 0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 3 3 0 3 3 0 3 0 0
3 0 0 3 4 4 3 4 3 0
0 0 0 3 4 4 3 3 0 0
0 0 0 3 4 4 3 0 0 0
0 0 0 3 4 4 3 0 0 0
0 0 0 0 3 3 0 3 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC253D4FBD0>
Okay, here's my analysis of the provided input-output example pair.

**Perception of Elements:**

The task involves a grid of pixels, each represented by a single digit integer (0-9). The input grid contains a shape formed by pixels of value 3 (green), surrounded by pixels of value 0 (white). The output grid seems to be a modified version of the input grid. The key difference is the appearance of pixels with value 4 (yellow) in the output. These yellow pixels appear within the boundaries of the original green shape, specifically in a contiguous block.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    elements: pixels
    properties:
      - width: 10
      - height: 10
  - name: green_shape
    type: object
    color: 3 (green)
    properties:
        - contiguous: true
  - name: yellow_shape
    type: object
    color: 4 (yellow)
    properties:
      - contiguous: true
      - location: inside green_shape

actions:
  - name: fill_inside
    agent: unknown
    target: green_shape
    instrument: yellow color (4)
    result: yellow_shape inside green_shape

relationships:
  - type: spatial
    subject: yellow_shape
    object: green_shape
    relation: contained_within

```


**Natural Language Program:**

1.  **Identify the green shape:** Locate the contiguous region of pixels with the value 3 (green) within the input grid.
2.  **Fill the interior:** Starting from the pixel at coordinates (4,4) on the green object and change the color of green pixels to yellow color (4), to its adjacent green pixels until the color is applied to green pixels that do not have another adjacent green pixel, where adjacent include the 8 nearby pixels.
3. **Output modified grid** Create a copy of the original image. Fill in the defined region by changing pixel values from green color to yellow.
4.  The rest of the grid remains unchanged.


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
