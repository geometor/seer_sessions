# 36fdfd69 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
1 0 0 0 0 1 1 0 0 0 0 0 0 1 0 0 0 1
1 1 2 1 1 1 1 1 1 0 0 1 0 1 1 1 0 0
1 1 1 2 1 2 2 2 2 0 1 1 1 0 0 1 1 0
1 0 2 1 2 2 2 2 2 0 1 0 0 0 1 1 1 1
0 1 1 1 0 0 1 1 1 0 0 0 1 0 1 1 0 0
1 0 1 0 0 1 1 0 0 0 1 1 1 1 0 0 0 0
1 0 1 0 0 0 1 0 1 0 0 0 0 0 1 1 0 1
0 0 0 1 0 0 1 0 0 0 1 0 0 0 1 2 1 0
0 1 0 1 1 0 0 0 0 1 0 0 0 0 2 2 1 1
0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 0 0
0 1 1 0 1 1 2 1 2 1 2 1 0 1 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 0 0 1 1 0 0 1
0 0 0 0 0 1 1 2 1 2 2 0 0 1 0 1 1 1
0 1 0 0 0 0 0 0 1 1 0 1 0 1 1 1 0 0
0 0 1 0 0 0 1 0 0 1 0 0 0 0 0 1 1 0
0 0 0 0 0 0 1 1 1 0 1 0 1 0 0 1 1 1
1 0 0 1 0 0 1 1 1 0 1 1 0 0 0 0 0 1
```

<PIL.Image.Image image mode=RGB size=1152x1088 at 0x78E5F21D2FD0>

**output:**
```
1 0 0 0 0 1 1 0 0 0 0 0 0 1 0 0 0 1
1 1 2 4 4 4 4 4 4 0 0 1 0 1 1 1 0 0
1 1 4 2 4 2 2 2 2 0 1 1 1 0 0 1 1 0
1 0 2 4 2 2 2 2 2 0 1 0 0 0 1 1 1 1
0 1 1 1 0 0 1 1 1 0 0 0 1 0 1 1 0 0
1 0 1 0 0 1 1 0 0 0 1 1 1 1 0 0 0 0
1 0 1 0 0 0 1 0 1 0 0 0 0 0 1 1 0 1
0 0 0 1 0 0 1 0 0 0 1 0 0 0 4 2 1 0
0 1 0 1 1 0 0 0 0 1 0 0 0 0 2 2 1 1
0 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 0 0
0 1 1 0 1 1 2 4 2 4 2 1 0 1 0 0 0 0
0 0 0 0 0 0 4 4 4 4 4 0 0 1 1 0 0 1
0 0 0 0 0 1 4 2 4 2 2 0 0 1 0 1 1 1
0 1 0 0 0 0 0 0 1 1 0 1 0 1 1 1 0 0
0 0 1 0 0 0 1 0 0 1 0 0 0 0 0 1 1 0
0 0 0 0 0 0 1 1 1 0 1 0 1 0 0 1 1 1
1 0 0 1 0 0 1 1 1 0 1 1 0 0 0 0 0 1
```

<PIL.Image.Image image mode=RGB size=1152x1088 at 0x78E5F21D3D50>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The input and output grids are identical except for some changes in pixel colors. Specifically, some pixels that are blue (1) in the input grid become yellow (4) in the output. It also seems like existing red(2) pixels dictate the change, specifically, blue(1) pixels that neighbor a red(2) pixel. There appears to be no other changes.

**YAML Block (Facts):**


```yaml
facts:
  - object: pixel
    properties:
      color:
        values: [0, 1, 2, 4]
        mapping: {0: white, 1: blue, 2: red, 4: yellow}
      position: (row, column)
    relationships:
      - type: neighbor
        description: Pixels sharing an edge are neighbors.
  - observation: color_change
    input_color: 1
    output_color: 4
    condition: "input pixel is a neighbor of a pixel with color 2"
```


**Natural Language Program:**

1.  **Iterate** through each pixel of the input grid.
2.  **Check** if the current pixel's color is blue (1).
3.  If the pixel is blue, **examine** its immediate neighbors (up, down, left, right).
4.  If *any* of the neighboring pixels is red (2), **change** the current pixel's color to yellow (4) in the output grid.
5.  If the pixel is not blue or none if its neighbors is red. **Keep** current pixel color in the output grid.
6.  All non-blue pixels retain their original color, and the overall grid structure stays the same.


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
