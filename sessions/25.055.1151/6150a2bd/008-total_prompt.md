# 6150a2bd • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
5 5 2
1 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x72AB78A69990>

**output:**
```
0 0 0
0 0 1
2 5 5
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x72AB78A68100>
Okay, here's my analysis of the provided example, presented as a report:

**Perception of Task Elements:**

The task involves a transformation of a 3x3 grid of colored pixels. Each pixel is represented by a single digit integer (0-9), corresponding to a specific color. The transformation appears to involve a rotation and a color inversion or mirroring of the grid's contents.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: 3x3 grid of pixels
    input:
      dimensions: [3, 3]
      elements: [5, 5, 2, 1, 0, 0, 0, 0, 0]
      element_type: integer
      element_range: [0, 9]
    output:
      dimensions: [3, 3]
      elements: [0, 0, 0, 0, 0, 1, 2, 5, 5]
      element_type: integer
      element_range: [0, 9]
  - type: transformation
    description: Rotation and color mirroring/inversion
    details: >
      The input grid is rotated 180 degrees.
      The values within the grid is also mirrored from top left and bottom right.

```


**Natural Language Program:**

1.  **Rotate:** Rotate the entire input grid by 180 degrees.
2. **Mirror values**: Mirror the values in the rotated grid. Imagine an axis runing from the original top left and bottom right. The value at a particular index is replaced by its "mirror" index across the imaginary axis.

In summary, the transformation is a 180 degree rotation combined with color mirroring.

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
