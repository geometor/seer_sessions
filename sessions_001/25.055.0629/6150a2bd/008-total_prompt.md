# 6150a2bd • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
5 5 2
1 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x79ABAF5737F0>

**output:**
```
0 0 0
0 0 1
2 5 5
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x79ABAF572320>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a transformation of a 3x3 grid of colored pixels. The colors are represented by single digits (0-9). The transformation seems to involve a rotation and a color swap. The input and output grids have the same dimensions.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 3x3
    elements: pixels
    properties:
      - color: represented by digits 0-9

actions:
  - type: rotation
    details: 180 degrees clockwise
  - type: color_swap
    details: specific color pairs are exchanged

relationships:
  - input_grid: initial state of the grid
  - output_grid: transformed state of the grid
```


**Natural Language Program:**

1.  **Rotate the Grid:** Rotate the entire input grid by 180 degrees clockwise.  This means the top-left element becomes the bottom-right, the top-right becomes the bottom-left, etc.

2.  **Color Swap:** Perform the following color substitutions based on the rotated grid:
    *   If a pixel is '1' (blue), change it to '5'(grey).
    *   If a pixel is '2' (red), change it to '1' (blue).
    *  If a pixel is '5'(grey), change it to '2'(red).
    All other colors remain unchanged.

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
