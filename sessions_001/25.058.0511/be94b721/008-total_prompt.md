# be94b721 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 0 0 0 0 6 6 0
0 3 0 0 4 4 0 0 6 0
3 3 3 0 4 4 0 0 0 0
0 3 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x320 at 0x7B1DDEC182D0>

**output:**
```
4 4
4 4
4 4
```

<PIL.Image.Image image mode=RGB size=128x192 at 0x7B1DDE7AB850>
Okay, here's my analysis of the example input-output pair, structured as requested:

**Perception of Elements:**

The input is a grid of colored pixels (represented by numbers 0-9). The output is a smaller grid, seemingly extracted from the input. The colors in the input are: white (0), green (3), yellow (4), and magenta (6). The output grid consists entirely of yellow (4) pixels. The yellow pixels in the input form a 2x2 contiguous block. The magenta pixels are only on the edge. The position of the yellow block in input is in the middle.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      name: input_grid
      dimensions: [5, 10]
      colors: [0, 3, 4, 6]  # white, green, yellow, magenta
    elements:
      - type: contiguous_block
        color: 4  # yellow
        shape: rectangle
        dimensions: [2, 2]
        position: (1,3)
      - type: contiguous_block
        color: 3
        shape: rectangle
        dimensions: [3,1]
        position: (1,0)

  - type: grid
    properties:
      name: output_grid
      dimensions: [3, 2]
      colors: [4]  # yellow
    elements:
      - type: contiguous_block
        color: 4  # yellow
        shape: rectangle
        dimensions: [3, 2]

actions:
  - type: extract
    object: input_grid
    target: output_grid
    parameters:
      color: 4  # yellow
```


**Natural Language Program:**

1.  **Identify** the largest contiguous block of yellow (4) pixels within the input grid.
2.  **Extract** a rectangle that includes all instances of the largest contiguous block. In this case, this is a 2x2 square.
3.   **Create** a filled rectangle from the shape extracted.
4.  **Output** the resulting 3x2 grid filled with yellow.


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
