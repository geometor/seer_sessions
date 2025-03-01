# 72322fa7 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 8 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x832 at 0x7A43F5E763D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 8 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 8 4
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
4 8 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 8 4 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x832 at 0x7A43F5F4FA50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels (represented by numbers 0-9). The primary colors present are yellow (4), azure (8), and white (0). There are distinct groups of connected pixels of the same color, forming "objects". The transformation seems to involve some form of replication or mirroring of these objects, specifically the yellow and azure ones, across both the horizontal and vertical axes. The white pixels act as background.

**YAML Block (Facts):**


```yaml
objects:
  - id: yellow_group_1
    color: yellow (4)
    shape: line
    position:
      start: [3, 1]
      end: [3, 3]
  - id: azure_group_1
    color: azure (8)
    shape: single pixel
    position: [4, 10]
  - id: yellow_group_2
      color: yellow(4)
      shape: line
      position:
        start: [9,0]
        end: [9,2]
  - id: azure_group_2
      color: azure(8)
      shape: single pixel
      position: [ 10, 7]

transformations:
  - type: replication
    axis: both horizontal and vertical
    affected_objects: [yellow_group_1, azure_group_1, yellow_group_2, azure_group_2]

```


**Natural Language Program:**

1.  **Identify Objects:** Locate all contiguous groups of non-white pixels. In this case, these groups are colored yellow (4) and azure (8). There are two distinct "lines" (horizontal contiguous blocks) of yellow, and two isolated azure pixels.

2.  **Horizontal and Vertical Replication:** Replicate non-white pixel groups. The existing objects appear replicated on the other half of the horizontal and vertical axis. If an object exists on the left half it gets replicated at an equivalent position in the right half. If an object exists in the top half it gets replicated in a similar location at the bottom half.

In simpler, more step by step form:

1. Scan first half of rows (0 to 6, since height = 13), from left to right and top to bottom.
2. When a non-white pixel is located, check for adjacent pixels in horizontal directions, forming horizontal lines. Record the color, and x-y locations.
3. After checking the first half, scan the bottom half (7-13).
4.  For each detected object, check the corresponding x-y coordinates in the other halves of both axis.
5. Copy each found object in the original coordinates to the output grid.
6. Copy each object to it's mirror position on the other horizontal half, and other vertical half.


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
