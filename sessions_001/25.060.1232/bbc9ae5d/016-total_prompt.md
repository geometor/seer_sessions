# bbc9ae5d • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
5 5 5 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x64 at 0x7CE41B94FF50>

**output:**
```
5 5 5 0 0 0 0 0 0 0
5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0
5 5 5 5 5 5 5 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x320 at 0x7CE41B856AD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a transformation of a single-row grid (input) into a multi-row grid (output). The input grid contains two distinct colors: gray (5) and white (0). The output grid expands the gray region vertically while maintaining the same number of white pixels. The left side seems to be a gray area expanding downwards and right side is all white area.

**YAML Block (Facts):**


```yaml
objects:
  - id: gray_region
    type: contiguous_block
    color: gray (5)
    initial_position: left_side
    shape: variable
  - id: white_region
    type: contiguous_block
    color: white (0)
    initial_position: right_side
    shape: variable

actions:
  - type: expansion
    object: gray_region
    direction: vertical
    constraints:
         - maintain_horizontal_length
         - stops_at_row_5

  - type: fill,
    object: white_region
    constraints:
        - maintain_original_width
        - stops_at_row_5

relationships:
  - type: adjacent
    objects: [gray_region, white_region]
    direction: horizontal
```


**Natural Language Program:**

1.  **Identify** the contiguous block of gray (5) pixels on the left side of the input grid and the white area (0) on the right.
2.  **Expand** the gray region vertically downwards. The height of gray region becomes 5.
3.  **Maintain** the original width of input. Fill rest of output grid with white.
4.  **Stop** when the number of rows is reach 5.

In essence, the transformation takes the input row and replicates it downwards to create the output. The replication of a row continues until there is 5 rows filled with values from original row.

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
