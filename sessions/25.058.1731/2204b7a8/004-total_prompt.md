# 2204b7a8 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 3 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 3 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 3 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36044BF7D0>

**output:**
```
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 2 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 1 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 1 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
1 0 0 0 0 0 0 0 0 2
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36045038D0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input and output are 10x10 grids.
*   The grids contain single-digit integers, representing colors.
*   The input grid has vertical bars of blue (1) on the left and red (2) on the right. It has a few green (3) pixels.
*   The output grid maintains most of the structure of the input grid, but the green (3) pixels are replaced by blue (1).

**YAML Block (Facts):**


```yaml
objects:
  - name: grid
    type: 2D array
    properties:
      rows: 10
      columns: 10
      values: integers (0-9)

  - name: pixel
    type: element
    properties:
        color:
          0: white
          1: blue
          2: red
          3: green

actions:
    - name: replace_color
      input:
        - object: pixel
          property: color
          value: 3
      output:
        - object: pixel
          property: color
          value: 1
relationships:
  - type: spatial
    description: "Pixels are arranged in a 2D grid."
  - type: transformation
    description: "Input grid transforms to output grid by replacing specific colored pixels"

```


**Natural Language Program:**

The program takes a 10x10 grid as input. It iterates through each pixel of the grid. If a pixel's color is green (3), it changes the pixel's color to blue (1). All other pixels remain unchanged. The program outputs the modified grid.

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
