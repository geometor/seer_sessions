# 99fa7670 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0 0 0 0
0 8 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 5 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7778514437F0>

**output:**
```
0 0 0 0 0 0
0 8 8 8 8 8
0 0 0 0 0 8
0 0 0 0 0 8
0 0 0 5 5 5
0 0 0 0 0 5
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x777851443D90>
Okay, here's my analysis of the provided example:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid contains two distinct non-zero colored pixels (azure and gray) against a background of white pixels. The output grid shows that the non-zero colors have expanded. The azure color expands horizontally, filling the entire row it occupies, while also appearing at the far end of the row below and the far end of two rows below the original. The gray expands to fills its row.

**YAML Block - Facts:**


```yaml
facts:
  - type: grid
    description: Input and output are 2D grids of pixels.
    dimensions: 6x6
  - type: object
    description: Pixels with non-zero values are considered objects.
  - object_property: color
    values:
      - 0: white
      - 5: gray
      - 8: azure
  - object_action: expansion
    azure_description:  Expands horizontally to fill its entire row.
    gray_description: Expand horizontally to fill the entire row.
  - object_action: partial_duplication:
      azure_description: Replicated to the end of two rows below the original.
      gray_description: Replicated to the end of the row below the original.

```


**Natural Language Program:**

1.  **Identify Objects:** Find all pixels in the input grid that have a non-zero color value. These are the "active" objects.
2.  **Horizontal Expansion:** For each active object, replace all pixels in its row with the object's color.
3.    **Partial duplication**: For each active object, replicate it to the very end of the rows below the original.
4.  **Preserve Background:** All other pixels (with an initial value of 0) remain unchanged (white).


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
