# aabf363d • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 0 0 0 0
0 2 2 2 0 0 0
0 0 2 0 0 0 0
0 2 2 2 2 0 0
0 0 2 2 2 0 0
0 0 0 2 0 0 0
4 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7BFC44390610>

**output:**
```
0 0 0 0 0 0 0
0 4 4 4 0 0 0
0 0 4 0 0 0 0
0 4 4 4 4 0 0
0 0 4 4 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7BFC44392F20>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid contains a shape made of red (value 2) pixels and a single yellow (value 4) pixel. The output grid appears to be a modified version of the input, where the red shape has been replaced with yellow pixels, and the original single yellow pixel is removed. The background (value 0) remains unchanged. The size and position of the red shape remain same after transformation, as does the overall grid size.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: Input and output are 2D grids of pixels.
  - type: object
    description: A contiguous shape of red (2) pixels exists in the input.
    properties:
      color: red (2)
      shape: irregular
      position: varies
  - type: object
    description: A single yellow (4) pixel exists in the input.
    properties:
      color: yellow (4)
      position: varies
  - type: transformation
    description: The red shape is replaced with yellow pixels.
  - type: transformation
    description: original yellow pixel is removed, replaced by background (0)
  - type: background
    description: background color remains unchanged
    properties:
        color: white(0)
```


**Natural Language Program:**

1.  **Identify** the contiguous shape composed of red (value 2) pixels in the input grid.
2.  **Identify** single yellow pixel (value 4).
3.  **Change** the color of all pixels within the identified red shape to yellow (value 4).
4.  **Change** the color of identified single yellow pixel to white (value 0)
5.  **Preserve** the white (value 0) background pixels.
6.  **Output** the modified grid.

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
