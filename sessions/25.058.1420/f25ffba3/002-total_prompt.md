# f25ffba3 • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 9
0 0 3 9
0 0 3 9
2 0 3 9
2 4 3 9
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x7A608CFC2210>

**output:**
```
2 4 3 9
2 0 3 9
0 0 3 9
0 0 3 9
0 0 0 9
0 0 0 9
0 0 3 9
0 0 3 9
2 0 3 9
2 4 3 9
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x7A608CFC2170>

## train_2

**input:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 2
0 0 0 2
0 8 0 2
0 3 8 2
3 3 8 2
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x7A608CFC1B30>

**output:**
```
3 3 8 2
0 3 8 2
0 8 0 2
0 0 0 2
0 0 0 2
0 0 0 2
0 0 0 2
0 8 0 2
0 3 8 2
3 3 8 2
```

<PIL.Image.Image image mode=RGB size=256x640 at 0x7A608CFC1D10>
<PIL.Image.Image image mode=RGB size=572x1330 at 0x7A608C34AC10>Okay, here's my analysis of the provided example pair, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The task involves 2D grids of colored pixels. The primary colors involved seem to vary between the examples, but consistently include white (0) and other distinct colors. The input grids appear to have a "filled" rectangle at the bottom-right corner, which might be a key object of interest. The output grid seems to be a vertically mirrored, or flipped, version of some parts of the input grid. The "filled" area also is maintained.

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      - colors: integers (0-9) representing different colors
      - dimensions: 10x4 in the example (height x width)

  - name: filled_rectangle
    type: subgrid
    properties:
      - colors: a contiguous block of non-zero pixels at bottom-right
      - dimensions: variable, defined by contiguous non-zero pixels

actions:
  - name: vertical_flip
    type: transformation
    description: Mirrors a section of the grid vertically.
    parameters:
      - selection: The area to be flipped. In this instance it appears to be the entire height and width.

relationships:
  - type: part_of
    from: filled_rectangle
    to: grid
    description: The filled rectangle is a part of the overall grid.
  - type: transforms_to
    from: grid
    to: grid
    action: vertical_flip, potentially with some row or column selection or rearrangement.

```


**Natural Language Program:**

1.  **Identify the "filled rectangle"**: Locate the contiguous block of non-zero pixels in the bottom-right corner of the input grid.
2.  **Vertical Flip:** Mirror the entire input grid vertically. It will result in the "filled rectangle" appears at the top.
3. **Copy Bottom:** The last row of the input is equal to first row of the output. The first row of the input is equal to last row of output.

In essence the image is vertically flipped.


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
