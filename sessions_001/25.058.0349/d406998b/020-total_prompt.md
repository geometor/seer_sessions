# d406998b • 020 • example_4 • investigate_coder

---

## Example 4

**input:**
```
0 0 5 0 0 5 0 5 0 5 0 5 0 0
5 0 0 0 5 0 0 0 5 0 5 0 0 5
0 5 0 5 0 0 5 0 0 0 0 0 5 0
```

<PIL.Image.Image image mode=RGB size=896x192 at 0x76911E9736B0>

**output:**
```
0 0 5 0 0 3 0 3 0 3 0 3 0 0
5 0 0 0 5 0 0 0 5 0 5 0 0 3
0 3 0 3 0 0 5 0 0 0 0 0 5 0
```

<PIL.Image.Image image mode=RGB size=896x192 at 0x76911E973930>
Okay, here's my analysis of the example input-output pair:

**Perception of Task Elements:**

The task involves a grid of pixels, each with a numerical value corresponding to a color. The primary colors observed are gray (5), white (0), and green (3). The input and output grids have the same dimensions (3x14). The transformation seems to involve selectively changing some gray (5) pixels to green (3) based on their position. There is a structure or pattern that is partially kept.

**YAML Block - Facts:**


```yaml
task: color_replacement
objects:
  - type: grid
    properties:
      dimensions: [3, 14]
      elements: pixels
      color_values: [0, 3, 5]
  - type: pixel
    properties:
      color:
        - white # 0
        - gray  # 5
        - green # 3
      position: [row, column]
actions:
  - name: change_color
    agent: transformation_rule
    input:
      - pixel
      - original_color
    output:
      - pixel
      - new_color
    conditions: specific_positions
relationships:
  - type: spatial
    description: Pixels are arranged in a 2D grid.
  - type: conditional
    description: color change depends on pixel position and maybe neighbor context
```


**Natural Language Program:**

1.  **Iterate** through each pixel of the input grid.
2.  **Identify** gray (5) pixels.
3. **Change** the color from grey(5) to green (3) at the following locations
    *   The pixel in the last column of the top row.
    *   The last pixel in the second row.
    *  The pixel on the bottom row at column index 2
    *   The pixel adjacent to the previously transformed pixel on the bottom row at the third column.

Essentially replacing a subset of gray pixels with green pixels, preserving all
other pixels.

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
