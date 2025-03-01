# 2204b7a8 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 3 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 3 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9 9 9
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360BFEBED0>

**output:**
```
8 8 8 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 0 0 0 0 9 0 0 0
0 0 0 9 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
9 9 9 9 9 9 9 9 9 9
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360BFEB8D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a 10x10 grid. The input grid contains pixels of azure (8), white (0), green (3), and maroon (9). The output grid seems to retain some of the input colors (azure and maroon) but replaces green (3) with the color of the pixels in the top and bottom rows depending upon the green pixel position.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements: pixels
    properties:
      color: [0, 3, 8, 9]  # White, Green, Azure, Maroon

actions:
  - type: replace_color
    target: 3  # Green
    condition: "position of original 3 pixel"
    replacement_top: 8
    replacement_bottom: 9

relationships:
  - type: spatial
    description: "Green pixels are replaced by the color of the top or bottom row pixels, dependent upon row"
```


**Natural Language Program:**

1.  **Identify:** Find all green (3) pixels within the input grid.
2. ** Check Row:**
    *  If any green color pixel are present in row index less than 5 (top half), change the color to azure (8)
    *   If any green color pixel are present in row index greater or equal to 5 (bottom half), change the color to maroon (9).
3.  **Preserve:** All other pixels (azure, white, and maroon) remain unchanged.
4.  **Output:** The modified grid is the output.

Essentially, the green pixels are replaced conditional to location: azure if green is in the top half, else maroon.

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
