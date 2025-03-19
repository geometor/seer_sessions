# ea32f347 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 5 5 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC252BC7D50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 2 2 2 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7FC252BC7750>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

The task involves a grid of pixels, initially with some areas colored gray (5). The transformation seems to recolor these gray areas based on their shape. It appears there are distinct horizontal and vertical gray components that are assigned different colors.

**YAML Block (Facts):**


```yaml
objects:
  - name: horizontal_gray_area
    type: contiguous_block
    color: gray (5)
    orientation: horizontal
  - name: vertical_gray_area
    type: contiguous_block
    color: gray (5)
    orientation: vertical
  - name: background
    type: grid_area
    color: white(0)

actions:
  - subject: horizontal_gray_area
    action: recolor
    new_color: blue (1) / red(2)
  - subject: vertical_gray_area
    action: recolor
    new_color: yellow (4)

relationships:
  - type: adjacency
    description: Gray areas are adjacent to white areas.
  - type: shape
    description: Gray areas form horizontal and vertical lines.
```


**Natural Language Program:**

1.  **Identify Contiguous Gray Areas:** Locate all contiguous blocks of gray (5) pixels.
2.  **Classify Orientation:** Determine if each gray block is primarily horizontal or vertical. A horizontal block is wider than it is tall; a vertical block will be taller than it is wide.
3.  **Recolor Horizontal Blocks:** Change the color of horizontal gray blocks to blue (1) if they are at the top and red(2) if not.
4.  **Recolor Vertical Blocks:** Change the color of vertical gray blocks to yellow (4).
5.  **Leave other areas unchanged.** White (0) areas are not to be modified.


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
