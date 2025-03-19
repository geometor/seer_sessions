# 6150a2bd • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
5 5 2
1 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7359640699C0>

**output:**
```
0 0 0
0 0 1
2 5 5
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x735964068130>
Okay, here's my analysis of the provided example, structured as a report:

**Perception of Elements:**

The task involves a transformation of a 3x3 grid of colored pixels. Each pixel is represented by a single digit integer (0-9), corresponding to a specific color. The input grid appears to be rotated and possibly inverted to produce the output grid. The colors themselves are also maintained during the transformation, with the positions being re-arranged.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: 3x3 matrix of pixels
    elements: integers (0-9) representing colors
  - object: pixel
    properties:
      color: represented by an integer (0-9)
      position: row and column index in the grid
  - transformation: rotation
    type: spatial
    details:  The grid is rotated 90 degrees counter-clockwise. Or 270 clockwise
  - transformation: positional_inversion
    type: logical
    details: the x,y coordinates are swapped from the first to second
```


**Natural Language Program:**

1.  **Input:** A 3x3 grid of colored pixels.
2.  **Transformation**:
    *   Rotate input grid by 90 degrees counter-clockwise (or 270 clockwise).
    *   Swap the x and y values. In other words a cell in the input data at \[x][y] will map to \[y][x] in the output data.
3.  **Output:** The transformed 3x3 grid.

Essentially the input matrix is rotated and the coordinates inverted.

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
