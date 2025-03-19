# 253bf280 • 022 • example_4 • investigate_coder

---

## train_4

**input:**
```
0 0 0 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x576 at 0x7CE423308BD0>

**output:**
```
0 0 0 0 0 0
0 0 8 0 0 0
0 0 3 0 0 0
0 0 3 0 0 0
0 0 3 0 0 0
0 0 3 0 0 0
0 0 3 0 0 0
0 0 8 0 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x576 at 0x7CE423308450>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of pixels, most of which are white (value 0). There are two key colors/values present: azure (8) and green (3). The azure pixels appear to define "anchor points", and the green pixels form a vertical line between them. The output grid retains the azure pixels in their original positions.

**YAML Block - Facts:**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - white (0)
        - azure (8)
        - green (3)
      position: [row, column]
  - type: grid
    properties:
      dimensions: [height, width]

actions:
  - name: identify_anchors
    description: Locate azure (8) pixels.
  - name: draw_line
    description: Create a vertical line of green (3) pixels between the azure anchors.

relationships:
  - type: spatial
    description: Azure pixels act as boundaries for the green line.
```


**Natural Language Program:**

1.  **Identify Anchors:** Find all pixels with the value 8 (azure) in the input grid.
2.  **Maintain Anchors:** Keep the locations and the value of azure pixels in the result.
3.  **Draw Vertical Line:** For each *pair* of vertically aligned pixels, if found, between their row positions, change the value to 3.

In simpler terms: Find the azure pixels. Keep the azure pixels in the output. Draw a green vertical line between vertically aligned azure pixels.

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
