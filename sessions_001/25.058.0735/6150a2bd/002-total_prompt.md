# 6150a2bd • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
3 3 8
3 7 0
5 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7A80FECD25D0>

**output:**
```
0 0 5
0 7 3
8 3 3
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7A80FECD2CB0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a 3x3 grid of single-digit integers, representing colored pixels. The transformation appears to involve a rotation of the grid's contents. The colors/values themselves remain unchanged; only their positions within the grid are altered. It seems like a 180-degree rotation.

**YAML Fact Documentation:**


```yaml
facts:
  - type: grid
    dimensions: 3x3
    elements: integers (0-9) representing colors
    transformation: rotation
    rotation_angle: 180 degrees
    properties_preserved:
      - color/value of each cell
    properties_changed:
      - position of each cell within the grid
```


**Natural Language Program:**

1.  **Input:** A 3x3 grid of integers.
2.  **Rotate:** Rotate the entire grid by 180 degrees clockwise (or counter-clockwise, the result is the same).
3.  **Output:** The rotated 3x3 grid.

In simpler terms, imagine picking up the input grid, flipping it upside down like a pancake, and placing it back down. The values in the top-left corner end up in the bottom-right, and so on.

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
