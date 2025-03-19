# dc433765 • 034 • example_6 • investigate_coder

---

## train_6

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x704 at 0x7CE41B95CA50>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x704 at 0x7CE41B95DE50>
Okay, here's my analysis of the provided input-output pair:

**Perception of Elements:**

The task involves two grids (input and output) of the same dimensions (11x11).  The grids primarily contain '0' values (white pixels), with a few exceptions. The input grid has a green pixel (3) and a yellow pixel (4). The output grid appears to be a modified version of the input, where one row of all zeros has been removed, specifically, the row immediately above the green pixel.

**YAML Block - Facts:**


```yaml
facts:
  - observation: Input and output grids are 11x11.
  - observation: Most pixels are 0 (white).
  - observation: Input grid contains a green pixel (value 3) and a yellow pixel (value 4).
  - observation: The output grid contains the same green (3) and yellow (4) pixel, at the same X coordinates
  - observation: The y coordinates of the green and yellow pixels are the same in the input and output grids
  - observation: output grid is identical to the input grid, except the all-zero row above the green pixel has been deleted
  - relationship: the row directly above the green pixel in the input becomes the location for green in the output

```


**Natural Language Program:**

1.  Identify the green pixel (value 3) in the input grid.
2.  Identify the row directly above the green pixel
3.  check if the row directly above the green pixel has all values equal to zero
4.  If the identified row does have all zeros, copy the input grid to a new grid, removing the identified row.
5.  If the identified row does not have all zeros, copy entire grid without changes.
6. return the modified grid.


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
