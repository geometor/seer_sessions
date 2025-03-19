# 48d8fb45 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 4 4 0 0
0 0 4 0 0 0 0 0 4 0
0 4 0 4 0 0 0 4 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B1DDE4F8FD0>

**output:**
```
4 4 0
0 0 4
0 4 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7B1DDE4F9550>
Okay, here's my analysis of the provided input-output example, formatted as a report:

**Perception of Elements:**

The task involves a transformation of a 2D grid of colored pixels (represented by numbers) into a smaller 2D grid. The primary colors involved seem to be white (0), yellow (4), and grey (5). The output grid appears to be a condensed version of the input grid, focusing on the yellow pixels and their relative positions. The grey pixel seems to disappear during processing and has no direct impact on the output.

**YAML Fact Block:**


```yaml
facts:
  - object: grid
    properties:
      - type: 2D array
      - values: integers (0-9 representing colors)
    observations:
      - input_shape: 10x10
      - output_shape: 3x3
  - object: pixel
    properties:
      - color:
        - white: 0
        - yellow: 4
        - grey: 5
    observations:
      - grey_pixel_disappears: true
  - action: transformation
    description: Condenses the input grid into a smaller output grid.
    details:
      - Focuses on yellow pixels.
      - Preserves relative positions of yellow pixels.
      - output grid shows only part of original, cropped around yellow pixels
```


**Natural Language Program:**

1.  **Identify Target Pixels:** Locate all yellow (4) pixels within the input grid.
2.  **Determine Bounding Box:** find the minimum bounding rectangle, this means finding the top-most, left-most, bottom-most and right most yellow pixels.
3.  **Extract Sub-grid:** Extract the region defined by top-most, left-most, bottom-most and right-most rows and columns.
4. return the cropped grid


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
