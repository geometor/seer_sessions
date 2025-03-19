# ed36ccf7 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 9
0 0 9
9 9 9
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7FC253C82750>

**output:**
```
9 9 9
0 0 9
0 0 9
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7FC25B62D3D0>
Okay, I'm ready to analyze this input-output pair and provide my observations.

**Perception of Elements:**

*   The input and output are 3x3 grids.
*   The grids contain two colors, represented by the digits 0 (white) and 9 (maroon).
*   The position of the colors changes between the input and output. It seems to be some sort of rotation or reflection.

**YAML Block (Facts):**


```yaml
facts:
  - type: grid
    dimensions: 3x3
    colors: [0, 9] # white, maroon
    input_state: "0 0 9; 0 0 9; 9 9 9"
    output_state: "9 9 9; 0 0 9; 0 0 9"
  - observation: The grid appears to be rotated or reflected.
  - input_object:
      color: maroon
      shape: L-shape
      position: bottom right
  - output_object:
      color: maroon
      shape: L-shape
      position: top-left, rotated 180.
  - action: The maroon L-shape has been rotated 180 degrees.
```


**Natural Language Program:**

The transformation rule is a 180-degree rotation of the grid. The L-Shaped object made out of marron (9) pixels is being rotated.

1.  Take the Input Grid
2.  Rotate the entire contents of the grid by 180 degrees.
3.  Present the rotated grid.

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
