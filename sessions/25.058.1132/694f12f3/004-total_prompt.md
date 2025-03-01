# 694f12f3 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 0
0 0 0 4 4 4 4 4 4 0
0 0 0 4 4 4 4 4 4 0
0 0 0 4 4 4 4 4 4 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F0A59D16490>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 1 1 4 0 0 0 0 0
0 4 1 1 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 4 0
0 0 0 4 2 2 2 2 4 0
0 0 0 4 2 2 2 2 4 0
0 0 0 4 4 4 4 4 4 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F0A59D16530>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves two grids of digits, where each digit represents a color. The input grid contains two distinct rectangular regions of color '4' (yellow) against a background of color '0' (white). The output grid shows modifications within these yellow regions. Specifically, the inner parts of these regions are changed to color '1' (blue) in the top rectangle and to color '2' (red) in the bottom rectangle. The outlines of the original yellow rectangles remain unchanged.

**YAML Block (Facts):**


```yaml
objects:
  - id: background
    color: 0
    description: The background color of the entire grid.
  - id: rectangle_1
    color: 4
    shape: rectangle
    location: top-left
    action: inner_fill
    fill_color: 1
  - id: rectangle_2
    color: 4
    shape: rectangle
    location: bottom-right
    action: inner_fill
    fill_color: 2
relationships:
  - rectangle_1 and rectangle_2 are separated by background.
  - The filled area of rectangle_1 and rectangle_2 does not include the outline.
```


**Natural Language Program:**

1.  **Identify Rectangles:** Locate all rectangular regions of color '4' (yellow) on the input grid.
2.  **Separate Rectangles:** Distinguish the rectangles based on location (top and bottom).
3.  **Inner Fill (Top Rectangle):** For the top-most rectangle, change the color of the inner pixels (excluding the outline) to '1' (blue).
4.  **Inner Fill (Bottom Rectangle):** For the bottom-most rectangle, change the color of the inner pixels (excluding the outline) to '2' (red).
5. **Preserve Outline:** Do not modify the original outline of the rectangles. Maintain pixels of original rectangle color.
6. **Output:** The output grid should reflect these changes, preserving background.

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
