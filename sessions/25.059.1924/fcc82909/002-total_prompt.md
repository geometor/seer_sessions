# fcc82909 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 4 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C4F650>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 9 9 0 0 0 0 0 0 0
0 6 6 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 3 3 0 0 8 4 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 3 3 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BE8250>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 8 0 0 0 0 0 0
0 0 9 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 1 0 0
0 0 0 0 0 0 1 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635CD8C50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 8 0 0 0 0 0 0
0 0 9 4 0 0 0 0 0 0
0 0 3 3 0 0 0 0 0 0
0 0 3 3 0 0 2 1 0 0
0 0 3 3 0 0 1 2 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 3 3 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BE8450>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 2 4 0 0 9 8 0 0
0 0 6 7 0 0 8 9 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 6 0 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BEAF50>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 2 4 0 0 9 8 0 0
0 0 6 7 0 0 8 9 0 0
0 0 3 3 0 0 3 3 0 0
0 0 3 3 0 0 3 3 0 0
0 0 3 3 7 6 0 0 0 0
0 0 3 3 6 6 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BEB9D0>
<PIL.Image.Image image mode=RGB size=2048x1360 at 0x71663D5B3050>Okay, here's my analysis of the provided examples, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The task involves 2D grids (matrices) containing single-digit integers (0-9) representing different colors.  The input grids are transformed into output grids.  The transformation appears to involve both a change in color and potentially the addition of new colored regions. The key seems to be identifying clusters of non-zero pixels and applying a consistent color change, possibly alongside growing a new region with color 3.

**YAML Fact Documentation:**


```yaml
facts:
  - type: grid
    description: Input and output are 2D grids of integers.
  - type: color_coding
    description: Integers 0-9 represent different colors. 0 is consistently background (white).
  - type: object
    description: Non-zero pixels form contiguous objects/clusters.
  - type: transformation_type
    description: Color replacement and addition of a fixed new color.
  - type: color_addition
    property: green (3)
    description: The new cluster is extended downward.
  - type: action:
    description: The transformation rule seems to expand and fill a fixed size rectangular with green color (3).
```


**Natural Language Program:**

1.  **Identify Objects:** Locate all contiguous regions (objects) of non-zero pixels in the input grid.
2.  **Color Replacement Area:** Locate all 2x2 clusters.
3.  **Green Expansion:** Create the target area. Add green (value 3) pixels:
    *   Below each original 2x2 cluster of non-zero pixels, fill up empty space.
    *   Below each original non-zero pixels that don't contain in 2x2 cluster, fill with two rows of green pixels.
    *   If any 2x2 cluster adjacent at row, fill with one row of green color, and put this row in between these objects.


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
