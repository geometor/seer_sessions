# 1f876c06 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 2 0 0 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360BFEBBD0>

**output:**
```
0 0 2 0 0 6 0 0 0 0
0 2 0 0 0 0 6 0 0 0
2 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 6
0 0 0 4 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 4 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360BFEB750>
Okay, here's my analysis of the provided input-output example pair, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The task involves a grid of colored pixels. The colors present in this specific example are white (0), red (2), magenta (6), and yellow (4).  The input and output grids have the same dimensions (10x10). The transformation seems to involve a vertical mirroring or reflection of the colored pixels, while the white pixels remain unchanged. The key colors (2, 4, and 6) appear to maintain their relative horizontal positions but are "flipped" vertically.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: [10, 10]
    elements: pixels
    properties:
      - color:
        values: [0, 2, 4, 6] # white, red, yellow, magenta
  - type: pixel
    properties:
      - color:
         mapping: {0: white, 2: red, 4: yellow, 6: magenta}
      - position: [row, column]

actions:
  - name: vertical_reflection
    description:  The colored pixels (non-zero) are reflected vertically across the horizontal midline of the grid.

relationships:
  - type: spatial
    description:  Pixels maintain their horizontal positions but change their vertical positions based on the reflection.
```


**Natural Language Program:**

1.  **Identify** all pixels with colors other than white (0) in the input grid.

2.  **Reflect** the positions of these non-white pixels vertically across the center line of the grid.
    *   Specifically, if a colored pixel is at position (row, col), its new position in the output grid will be (height - 1 - row, col), where 'height' is the number of rows in the grid.

3.  **Copy** all pixels over to the output grid
    *   All white pixels (0) remain in their original positions.
    *   All non-white pixels have their position reflected as in step 2

This can also be described as mirroring non-white pixel positions from top to
bottom, preserving horizontal position.

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
