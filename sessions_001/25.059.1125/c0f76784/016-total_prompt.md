# c0f76784 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0
0 5 0 0 0 5 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7F4C1B67E8D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 5 8 8 8 5 0 0 0 0 0 0
0 5 8 8 8 5 0 0 0 0 0 0
0 5 8 8 8 5 0 0 0 0 0 0
0 5 5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 5 7 7 5 0 0 0 0
0 0 0 0 5 7 7 5 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7F4C1B703250>
Okay, here's my analysis of the provided input-output example, formatted as requested:

**Perception of Elements:**

The task involves two 12x12 grids. The input grid contains two distinct shapes made of grey (5) pixels, surrounded by white (0) pixels. The output grid seems to modify the interior of these shapes with new colors while retaining the outline and the overall shape, as well as all white pixels. The top grey shape is filled with azure (8), the bottom one with orange (7).

**YAML Block (Facts):**


```yaml
objects:
  - id: shape_1
    type: contiguous_region
    color: grey (5)
    initial_location: top_left
    outline: yes
  - id: shape_2
    type: contiguous_region
    color: grey (5)
    initial_location: bottom_right
    outline: yes
  - id: background
    type: background
    color: white (0)

actions:
  - type: fill_interior
    target: shape_1
    new_color: azure (8)
  - type: fill_interior
    target: shape_2
    new_color: orange (7)

relationships:
  - shape_1: above:shape_2
  - shape_1: contains: azure_region
  - shape_2: contains: orange_region
  - background: surrounds: [shape_1, shape_2]

```


**Natural Language Program:**

1.  Identify all contiguous regions (shapes) of grey (5) pixels.
2.  For the top-most grey shape, fill its interior pixels (all non-outline grey pixels) with azure (8).
3.  For the bottom-most grey shape, fill its interior pixels (all non-outline grey pixels) with orange (7).
4.  Leave all white (0) background pixels unchanged.

Essentially, we find the distinct gray shapes, then for each of them change their inner pixels to other determined colors, based on top/down position.

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
