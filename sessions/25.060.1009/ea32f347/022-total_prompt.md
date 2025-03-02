# ea32f347 • 022 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 5 5 5 5 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 5 5 5 5 5 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC253D0C050>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 2 2 2 2 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 4 4 4 4 4 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC253D0F9D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, each with a numerical value representing a color. The input grid contains a shape formed by gray (5) pixels, while the output grid contains the same shape outline but with different colors: blue (1) for the vertical line, red (2) for the top horizontal segment, and yellow (4) for the bottom horizontal segment. The background is white (0) in both. The shape seems to be preserved, but the colors are changing based on the segment's position.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 10x10
      background_color: 0 (white)
  - type: shape
    properties:
      initial_color: 5 (gray)
      shape_type: "L" with a vertical and two attached horizontals
      segments:
        - type: vertical_line
          color: 1 (blue)
        - type: horizontal_line_top
          color: 2 (red)
        - type: horizontal_line_bottom
          color: 4 (yellow)

actions:
  - type: recolor_segments
    description: Change the color of shape segments based on their type.

relationships:
  - type: spatial
    description: The shape's segments are connected to form an "L" and additional attached horizontal. The output shape is isomorphic to the input shape.

```


**Natural Language Program:**

1.  **Identify the Shape:** Locate the contiguous shape formed by gray (5) pixels in the input grid.
2.  **Segment Identification:** Divide the shape into three segments:
    *   A vertical line segment.
    *   The horizontal segment attached to the *top* of the vertical segment.
    *   The horizontal segment attached to the *bottom* of the vertical segment.
3.  **Recolor Segments:**
    *   Change the color of the vertical line segment to blue (1).
    *   Change the color of the top horizontal line segment to red (2).
    *   Change the color of the bottom horizontal line segment to yellow (4).
4.  **Maintain Background:** Keep all other pixels as white (0).
5. **Output**: produce the new grid with the shape segments and background.

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
