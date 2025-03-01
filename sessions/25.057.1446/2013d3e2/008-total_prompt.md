# 2013d3e2 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 1 0 0 0
0 0 3 6 5 3 0 0 0 0
0 0 5 2 2 6 0 0 0 0
0 0 6 2 2 5 0 0 0 0
0 0 3 5 6 3 0 0 0 0
0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x786C5486E5D0>

**output:**
```
1 0 0
0 3 6
0 5 2
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x786C54816950>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The input is a 10x10 grid, and the output is a 3x3 grid. The input grid contains a central cluster of non-zero pixels surrounded by zeros. The output grid seems to be a cropped and condensed version of the central non-zero region of the input, with the surrounding zeros removed. The colors and their relative positions are maintained in the output. The two blue pixels in the input disappear.

**YAML Block (Facts):**


```yaml
facts:
  - object: input_grid
    type: grid
    dimensions: 10x10
    elements: pixels
    properties:
      - color: [0-9] # Representing different colors
  - object: output_grid
    type: grid
    dimensions: 3x3
    elements: pixels
    properties:
      - color: [0-9]
  - relationship: output_grid_is_cropped_input_grid
    subject: output_grid
    predicate: is a cropped version of
    object: input_grid
  - action: cropping
    agent: unknown
    target: input_grid
    result: output_grid
  - objects_removed:
    - blue_pixels at locations (1,1) and (6,1) (input)
  - observation:
    description: "All non-zero pixels, other than the blue, in the central region are preserved."
```


**Natural Language Program:**

1.  **Identify the Target:** Locate the smallest rectangular region within the input grid that contains all the non-zero pixels, ignoring the blue color.
2.  **Crop:** Extract this rectangular region.
3.  **Output:** The extracted region is the output grid.

Essentially, the transformation identifies and extracts the smallest rectangle
containing the colored cluster at the input grid's center, excluding the blue
pixels (color 1).

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
