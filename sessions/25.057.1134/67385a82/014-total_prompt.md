# 67385a82 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
3 3 0 3
3 3 0 0
3 0 0 3
0 0 3 3
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x74AF1CCD9550>

**output:**
```
8 8 0 3
8 8 0 0
8 0 0 8
0 0 8 8
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x74AF1C88FE50>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

*   The task involves a 4x4 grid in both the input and output.
*   The input grid contains two colors: green (3) and white (0).
*   The output grid contains three colors: azure (8), white (0), and green (3).
*   The white (0) pixels seem to remain unchanged.
*   The green (3) pixels seem to be changing to azure (8), except one in the top right corner.

**YAML Fact Documentation:**


```yaml
objects:
  - type: grid
    dimensions: 4x4
    elements: pixels
    properties:
      color:
        values: [0, 3]  # Input grid colors
        mapping:
          0: white
          3: green

  - type: grid
    dimensions: 4x4
    elements: pixels
    properties:
       color:
         values: [0,3,8]
         mapping:
           0: white
           3: green
           8: azure

actions:
  - type: color_change
    input_color: 3
    output_color: 8
    conditions:
       - "most green pixels change to azure"

relationships:
  - type: spatial
    description: "input and output grids have the same dimensions"
```


**Natural Language Program:**

1.  **Initialization:** Start with a 4x4 input grid containing pixels of colors white (0) and green (3).
2.  **Preservation:** All white (0) pixels in the input grid remain unchanged in the output grid.
3. **Color Transformation:** All of the green pixels, except the pixel in the top right corner, are changed to azure (8).
4. **Output**: top right green (3) pixel is unchaged.


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
