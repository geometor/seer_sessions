# 7447852a • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x7B1DDE7AB850>

**output:**
```
2 0 0 0 2 4 4 4 2 0
4 2 0 2 0 2 4 2 0 2
4 4 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x7B1DDE42D1D0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels, represented by numbers. The primary colors observed are red (2) and white (0). The transformation seems to involve the introduction of yellow (4) pixels. The spatial arrangement and patterns of the red pixels appear to be crucial to the transformation.

**YAML Block - Facts:**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - red (2)
        - yellow (4)
      position: [row, column]
  - type: grid
    properties:
      dimensions: [height, width]
      cells: list of pixels

actions:
  - type: color_change
    conditions:
      - spatial_pattern:  "red (2) pixels surrounded by, or adjacent to other red pixels"
    result:
      - change to yellow(4)
      
relationships:
    - adjacency: "pixels can be horizontally, vertically, adjacent"
```


**Natural Language Program:**

1.  **Identify Target Pixels:** Examine the input grid. The red (2) pixels are the focus.
2.  **Horizontal/Vertical Check, :** If a red pixel is immediately adjacent to a red pixel, it might turn to yellow (4), either horizontally or vertically.
3. **Color change:** If a red pixel has a direct horizontal or vertical neighbor, that is also red, under the following condition:
    - if a red pixel is on the edge, it will have at maximum, 2 vertical or 2 horizontal neighbours
    - if a red pixel is in the middle, it will have at maximum, 1 horizontal or 1 vertical neighbours.
    - if a red pixel satisfy any of these condition, it is converted to yellow (4).
4.  **Apply Transformation:** Create the output grid by copying the input grid, changing some red (2) to yellow(4), according to previous rules. All other pixels remain unchanged.

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
