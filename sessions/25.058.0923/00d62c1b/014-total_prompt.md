# 00d62c1b • 014 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 3 3 0 3 3 0 3 0 0
3 0 0 3 0 0 3 0 3 0
0 0 0 3 0 0 3 3 0 0
0 0 0 3 0 0 3 0 0 0
0 0 0 3 0 0 3 0 0 0
0 0 0 0 3 3 0 3 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B3DDB30FCD0>

**output:**
```
0 0 0 0 0 3 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 3 3 0 3 3 0 3 0 0
3 0 0 3 4 4 3 4 3 0
0 0 0 3 4 4 3 3 0 0
0 0 0 3 4 4 3 0 0 0
0 0 0 3 4 4 3 0 0 0
0 0 0 0 3 3 0 3 0 0
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B3DDB30C650>
Okay, here's my analysis of the provided input-output example pair, focusing on perception, facts, and a natural language program description.

**Perception of Elements:**

The task involves a grid of pixels, where each pixel has a color represented by a digit (0-9). The primary color observed is green (3) and white (0). The transformation seems to involve identifying a specific region within the green (3) pixels and changing the color of some of those pixels to yellow (4). The shape formed by green pixels appears to be an irregular shape. The overall grid size is 10x10.

**YAML Block (Facts):**


```yaml
objects:
  - id: grid
    type: 2D array
    dimensions: [10, 10]
    elements: pixels
  - id: green_shape
    type: irregular shape
    color: 3 # Green
    property: contiguous
  - id: yellow_shape
      type: rectangle
      color: 4
      property: within_green_shape

actions:
  - type: identify_region
    agent: unknown
    target: green_shape
    criteria: central, contiguous, rectangular subsection
  - type: change_color
    agent: unknown
    target: identified_region
    from_color: 3 # Green
    to_color: 4 # Yellow

relationships:
  - type: spatial
    relation: contains
    subject: green_shape
    object: yellow_shape
  - type: adjacency
      relation: determines extent of green object
      subject: grid
      object: green shape

```


**Natural Language Program:**

1.  **Identify the Green Shape:** Locate the contiguous region of pixels with the value '3' (green) within the input grid. This forms the 'green_shape'.
2.  **Find the Central Rectangular Region:** Within the 'green_shape', identify a rectangular sub-region. It is a rectangle within the central area of the green shape, that includes all rows and all columns of green cells that form a continuous section.
3.  **Change Color:** Change the color of the pixels within this rectangular region from '3' (green) to '4' (yellow).
4.  **Output:** The output grid is the same as the input grid, except for the pixels within the identified rectangular region, which are now yellow.

In summary, the transformation isolates the green object and replaces the largest fully contained rectangle, from the "center outward" with yellow.

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
