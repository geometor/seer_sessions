# 47c1f68c • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
2 0 0 4 0 0 0
0 2 2 4 0 0 0
0 2 0 4 0 0 0
4 4 4 4 4 4 4
0 0 0 4 0 0 0
0 0 0 4 0 0 0
0 0 0 4 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x78E5F21D2D50>

**output:**
```
4 0 0 0 0 4
0 4 4 4 4 0
0 4 0 0 4 0
0 4 0 0 4 0
0 4 4 4 4 0
4 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x78E5F21D3CD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a grid of colored pixels. The primary colors involved are red (2), yellow (4), and white (0). The input grid appears to have a cross-like shape made of yellow pixels, with some red pixels in the top-left corner. The output grid retains only the yellow pixels from the input, and it seems like the shape has been rotated or reflected.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    elements: pixels
    properties:
      - width: 7 (input), 6 (output)
      - height: 7 (input), 6 (output)
      - colors: [0, 2, 4] (input), [0, 4] (output)

  - name: pixel
    type: element
    properties:
      - color: integer (0-9)
      - position: (row, column)

  - name: yellow_cross
      type: object
      properties:
        - color: 4
        - shape: cross-like

actions:
  - name: filter_color
    description: Remove pixels of a specific color.
  - name: rotate_or_reflect
    description: I am not certain if the shape will be rotated or reflected. It almost looks like it is rotated 90 degrees clockwise

relationships:
  - yellow_cross: is_composed_of: pixels (color=4)
  - grid: contains: pixels
```


**Natural Language Program:**

1.  **Identify** the cross shape composed of yellow (4) pixels in the input grid.
2.  **Filter**: Remove all pixels that are not yellow (4).
3. **Rotate**: Rotate the pixels that make up the object by 90 degrees.


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
