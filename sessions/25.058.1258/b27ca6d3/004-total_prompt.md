# b27ca6d3 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=1152x960 at 0x7E120E2F5F90>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 3 2 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 2 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=1152x960 at 0x7E120E2F6350>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, initially mostly white (0) with some red (2) pixels scattered seemingly randomly. The transformation seems to involve adding green (3) pixels around some of the red (2) pixels. The positioning of the green pixels appears to be directly adjacent to the red pixels, forming a sort of "halo" or "border" in certain locations. It is important to see how consistent the placement rule is.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - red (2)
        - green (3)
      position: [row, column]
actions:
  - name: surround
    agent: red pixel
    target: adjacent pixels
    result: change adjacent pixel color to green
relationships:
  - type: adjacency
    between: [red pixel, green pixel]
```


**Natural Language Program:**

1.  **Identify** all red (2) pixels in the input grid.
2.  **For each** red (2) pixel:
    *   **Check** the directly adjacent pixels (up, down, left, and right - not diagonal).
    * Specifically find the group of 3 pixels: the top, middle, and bottom of the row, or the left, middle, and right of the column.
    * If a horizontal or vertical group of three such cells all exist, **change** the color of adjacent white (0) pixels to green (3) *within that set of 3*.
3.  **Leave** all other pixels unchanged.
4. Green pixels are only added on the first and third cells in the existing group, that is, it looks like an adjacent 'frame' must exist for green to be filled.

Essentially, a three element frame must exist around red pixels, where there is an adjacent cell on *both* sides, before the border of green pixels are added. The core idea appears to be the creation of a partial green border, but only where the local shape of the border allows it.

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
