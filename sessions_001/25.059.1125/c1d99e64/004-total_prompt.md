# c1d99e64 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
1 0 0 0 1 1 1 1 0 1 1 0 1 0 1 0 1 1 1
1 0 1 0 1 1 1 1 0 0 1 1 1 1 1 1 0 1 1
1 1 1 1 0 0 1 1 0 1 0 0 0 1 0 1 0 1 0
1 0 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1
1 0 1 1 0 1 1 1 0 1 1 1 1 1 1 1 1 1 1
1 1 0 1 0 1 1 0 0 0 0 1 0 1 1 0 0 0 1
1 0 0 1 1 0 1 0 0 1 1 1 1 1 1 1 0 1 0
1 1 0 0 1 1 1 1 0 1 0 1 1 1 0 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 0 0 1 1 1 0 1 0 0 1 1 1 1 1 1 1
1 1 0 0 1 1 0 0 0 1 1 0 0 0 1 0 1 0 1
1 0 1 0 1 0 0 1 0 1 1 1 1 0 0 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=1216x768 at 0x7F4C1B77AFD0>

**output:**
```
1 0 0 0 1 1 1 1 2 1 1 0 1 0 1 0 1 1 1
1 0 1 0 1 1 1 1 2 0 1 1 1 1 1 1 0 1 1
1 1 1 1 0 0 1 1 2 1 0 0 0 1 0 1 0 1 0
1 0 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1
1 0 1 1 0 1 1 1 2 1 1 1 1 1 1 1 1 1 1
1 1 0 1 0 1 1 0 2 0 0 1 0 1 1 0 0 0 1
1 0 0 1 1 0 1 0 2 1 1 1 1 1 1 1 0 1 0
1 1 0 0 1 1 1 1 2 1 0 1 1 1 0 1 1 1 1
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
1 1 1 0 0 1 1 1 2 1 0 0 1 1 1 1 1 1 1
1 1 0 0 1 1 0 0 2 1 1 0 0 0 1 0 1 0 1
1 0 1 0 1 0 0 1 2 1 1 1 1 0 0 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=1216x768 at 0x7F4C1B74CA50>
Okay, here's a breakdown of my observations and a proposed natural language program for the transformation:

**Perception of Task Elements:**

*   The input and output are grids of the same dimensions.
*   The grids contain single-digit integers (0, 1, and 2).
*   The color mapping associates 0 with white, 1 with blue, and 2 with red.
*   The primary change appears to be the introduction of the color red (2) in the output grid.
*    All of the 2s form a cross.
*   The red cross is centered in the output grid.
*   All 0s are preserved in the input

**YAML Documentation of Facts:**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - dimensions: 12 x 19
      - values: [0, 1]
  - name: output_grid
    type: grid
    properties:
      - dimensions: 12 x 19
      - values: [0, 1, 2]
  - name: red_cross
    type: shape
    properties:
     - color: red (2)
     - location: center
     - description: vertical and horizontal lines intersecting at the center

actions:
  - name: preserve_zeros
    description: all 0 values in the input are present in the output, in the same location.
  - name: add_cross
    description: draw a red (value 2) cross, centered, in the output grid.

relationships:
  - input_grid and output_grid have same dimensions.
  - All 0-value pixels in input_grid are in the same locations in output_grid
  - The value 2 in the output forms a cross centered on the grid.
```


**Natural Language Program:**

1.  Copy the input grid to the output grid, preserving all 0 values.
2.  Calculate the center row and center column of the output grid.
3.  Change the value of every cell in the center row to 2.
4. Change the value of every cell in the center column to 2.


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
