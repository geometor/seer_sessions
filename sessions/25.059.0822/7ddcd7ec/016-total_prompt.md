# 7ddcd7ec • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x70A2EC7935D0>

**output:**
```
0 0 0 0 0 0 0 0 7 0
0 0 0 0 0 0 0 7 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 7 0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x70A2EC74DE50>
Okay, let's analyze this input-output example.

**Perception of Elements:**

*   The input and output are grids of digits, representing colored pixels.
*   The primary color present is orange (7) against a background of white (0).
*   The orange pixels in the input form a somewhat connected shape, while in the output, the shape is expanded and rotated.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      rows: 10
      columns: 10
      background_color: 0  # White
  - type: shape
    properties:
      color: 7  # Orange
      initial_position:
        row_min: 2
        row_max: 5
        col_min: 3
        col_max: 6
    actions:
      - type: expand
        details: "Expands around the core 2x2 square of orange."
      - type: rotate
        details: "Rotates 90 degrees counter-clockwise."
```


**Natural Language Program:**

1.  **Identify the Core:** Locate the contiguous orange (7) pixels in the input grid. There appears to be an identifiable 2x2 square of '7's.
2.  **Expand:** If there is an isolated orange region, a copy is translated.
3. **Rotate:** The copied orange region rotates by 90 degrees counter-clockwise relative to the 2x2 orange block.


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
