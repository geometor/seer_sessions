# cf98881b • 028 • example_5 • investigate_coder

---

## train_5

**input:**
```
4 0 4 0 2 0 0 0 0 2 0 0 0 1
4 4 4 4 2 0 0 0 9 2 1 1 0 0
0 4 4 4 2 0 9 9 0 2 1 1 0 1
0 4 4 0 2 0 0 9 0 2 0 1 0 1
```

<PIL.Image.Image image mode=RGB size=896x256 at 0x7CE41B8FFAD0>

**output:**
```
4 0 4 1
4 4 4 4
1 4 4 4
0 4 4 1
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7CE41B94FBD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a grid of colored pixels. The input grid is wider and contains more colors than the output grid. The output grid seems to be a simplified, smaller version of a section of the input grid. The primary color in both input and output is yellow (4). The output grid appears to retain spatial relationships from the input, but only of yellow and a few non-yellow pixels.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: [height, width]
      colors: [list of unique color values]
    instances:
      input_grid:
        dimensions: [4, 14]
        colors: [0, 1, 2, 4, 9]
      output_grid:
        dimensions: [4, 4]
        colors: [0, 1, 4]

  - type: pixel
    properties:
      color: integer (0-9)
      position: [row, column]

actions:
  - type: selection
    description: A sub-region of the input grid is selected.
    parameters:
      - top_left_corner: [row, column]
      - dimensions: [height, width]

  - type: filtering
    description: Pixels of certain colors are removed or replaced.

relationships:
  - spatial_containment: The output grid is a spatially consistent subset of the input grid.
```


**Natural Language Program:**

1.  **Identify a Region of Interest:** Locate a 4x4 region within the input grid.
2. **Focus on Yellow:** It seems that non-yellow pixels outside of the selected region are removed. The region must begin with yellow.
3.  **Copy:** The 4x4 output retains the spatial relationship of colors from the
    input.

In short, select a 4x4 subsection of input composed of yellow, blue and white pixels.

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
