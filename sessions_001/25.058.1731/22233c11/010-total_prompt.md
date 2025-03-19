# 22233c11 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360455CC50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36044BF2D0>
Okay, let's analyze this input-output example.

**Perception of Elements:**

*   The input and output are 10x10 grids.
*   The input grid contains two 2x2 squares of green (3) pixels.
*   The output grid is identical to the input grid except for:
    *   Two azure (8) pixels in the top-left corner.
    *   Two azure (8) pixels in the bottom-right.

**YAML Block (Facts):**


```yaml
objects:
  - id: square1
    type: square
    color: green
    size: 2x2
    position: (3,3)  # Top-left corner coordinates
  - id: square2
    type: square
    color: green
    size: 2x2
    position: (1,5) # Top left corner coordinates
  - id: azure_pixels1
    type: object
    color: azure
    size: 2x1
    position: (0,1)
  - id: azure_pixels2
    type: object
    color: azure
    size: 2x1
    position: (5,7)

actions:
  - type: add
    object: azure_pixels1
    to: output_grid
  - type: add
    object: azure_pixels2
    to: output_grid
    
relationships:
   - squares are diagonally opposed
   - azure pixels are placed at opposite corners of the grids.

```


**Natural Language Program:**

1.  Copy the input grid to the output grid.
2.  Add two azure (8) pixels to the top left corner of the output, at row 1 column 0 and at row 2 column 0.
3.  Add a two azure pixels at row 7, column 5 and at row 8, column 5 and in the bottom right corner of the grid.

Essentially, the transformation preserves the original green squares and adds azure pixels in the corners.

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
