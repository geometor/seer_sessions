# 60b61512 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 4 4 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7F0A59D17890>

**output:**
```
0 0 0 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
7 4 4 0 0 0 0 0 0
4 4 4 0 0 0 0 0 0
0 0 0 0 0 4 4 4 0
0 0 0 0 0 7 4 7 0
0 0 0 0 0 7 4 7 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x576 at 0x7F0A5AEC1A90>
Okay, here's a breakdown of my observations and a proposed natural language program for the transformation:

**Perception of Elements:**

*   **Input:** A grid of pixels, mostly white (0) with some yellow (4) shapes.
*   **Output:** Same grid, but some of the yellow (4) pixels have been changed to orange (7).
*   The yellow shapes appear to come in two configurations:
    1.  A 3x2 or 2x3 rectangular block
    2. Isolated single pixels
*    It appears only some of the yellow becomes orange.

**YAML Documentation of Facts:**


```yaml
objects:
  - name: grid
    type: 2D array
    elements: pixels
    properties:
      - color:
          values: [0, 4, 7]
          mapping:
            0: white
            4: yellow
            7: orange

  - name: yellow_shape
    type: contiguous block
    properties:
        color: yellow
        possible_shapes:
            - rectangle: [3x2, 2x3]
            - isolated: 1x1

actions:
  - name: change_color
    agent: yellow_shape
    target: specific yellow pixels
    precondition:
      - pixel is part of shape
      - there is a yellow pixel directly below the top right yellow pixel and is either not boardered on the left or right by another yellow, or it is directly above another yellow that is part of a 3x2 group.

    result:
      - color changes from yellow(4) to orange(7)

relationships:
   - Adjacent: pixels share a side
```


**Natural Language Program:**

1.  **Identify** all yellow (4) pixels in the input grid.
2.  Locate any yellow pixels that are directly below the top-right most yellow pixel and is part of a cluster of at least one other yellow pixel, and is not boardered by yellow on both the left and right,
3. Or, locate any yellow pixel that is directly above another yellow that is part of a 3x2 yellow area.
4.  **Change** the color of the identified yellow pixels to orange (7).
5.  **Preserve** all other pixels (white and the remaining yellow) as they are in the input.

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
