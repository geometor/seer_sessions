# dc1df850 • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
2 0 0 0 0
0 0 0 2 0
0 0 0 0 0
0 6 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7B1DDE739B50>

**output:**
```
2 1 1 1 1
1 1 1 2 1
0 0 1 1 1
0 6 0 0 0
0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7B1DDE699FD0>
Okay, I will analyze the provided input-output example and deliver my observations.

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid contains a few pixels of red (2) and magenta (6), with the rest being white (0). The output grid introduces blue (1) pixels in the top three rows, replacing some of the white pixels. The red pixels remain in the same positions, and the magenta pixel also stays the same. It seems like a flood fill operation might be occurring, starting from some white pixels and stopping when it hits a non-white pixel.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      rows: 5
      columns: 5
      cell_values: [0-9]  # Representing colors
  - type: pixel
    properties:
      color:
        - white (0)
        - red (2)
        - magenta (6)
        - blue (1)
      position: [row, column]

actions:
  - name: flood_fill
    parameters:
      start_position: [row, column]
      fill_color: color_value
    constraints:
      - Stops at non-white pixels

relationships:
  - type: adjacency
    description: Pixels are adjacent horizontally and vertically.
  - type: containment
    description: The grid contains pixels.
```


**Natural Language Program:**

1.  **Identify** all red (2) and magenta (6) pixels in the input grid. Their positions and colors are preserved in the output.
2.  **Flood Fill**: for the top 3 project rows and all columns, perform the steps:
    1. change all white (0) pixels to blue (1).
    2. If a pixel is red, it will retain the color red.

In essence, the top three rows are being flood-filled with blue, with the constraint is that red pixels won't be changed to blue, and the red and magenta pixels are unchanged.

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
