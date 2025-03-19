# 6150a2bd • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
5 5 2
1 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x799A661079D0>

**output:**
```
0 0 0
0 0 1
2 5 5
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x799A66106F80>
Okay, here's my analysis of the provided input-output example, formatted as a report:

**Perception of Elements:**

The task involves a transformation of a 3x3 grid of colored pixels. The colors are represented by single digits (0-9). The input and output grids have the same dimensions. It appears there's a rotation and a color inversion or mirroring involved. The positions of specific colors seem to be key to the transformation.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    dimensions: 3x3
    elements: pixels
    properties:
      - color: represented by digits 0-9

actions:
  - rotation: clockwise or counterclockwise
  - color_inversion:  colors are possibly swapped or mirrored based on position

relationships:
  - spatial:  pixels have relative positions (row, column) within the grid
  - color_based: transformation may depend on the initial color of the pixel
```


**Natural Language Program:**

1.  **Rotate the grid:** Rotate the entire input grid 90 degrees clockwise.
2.  **Invert Colors on the main diagonal:** The colors on the main diagonal are flipped. The top left, the center and the bottom right corner change places, the content of the bottom left corner becomes the top left corner.

This is a high-level program. The detailed color change operation needs further refinement, but this rotation and color changes is the main idea.

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
