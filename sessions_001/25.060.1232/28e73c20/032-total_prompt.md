# 28e73c20 • 032 • example_5 • investigate_coder

---

## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7CE41B8FFC50>

**output:**
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 3 0 3
3 0 3 3 3 3 0 3 0 3
3 0 3 0 3 3 0 3 0 3
3 0 3 0 0 0 0 3 0 3
3 0 3 3 3 3 3 3 0 3
3 0 0 0 0 0 0 0 0 3
3 3 3 3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7CE41B8FFDD0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

The input is a 10x10 grid filled entirely with zeros (white pixels). The output is also a 10x10 grid, but it contains a pattern of 3s (green pixels) and 0s (white pixels). The 3s appear to form a sort of filled, irregular, but symmetrical shape. The shape seems constructed using both solid blocks and lines with "thickness".

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    dimensions: 10x10
    elements:
      - type: pixel
        values: [0, 3]
        colors: [white, green]

properties:
  - grid_input:
      fill: all pixels are 0 (white)
  - grid_output:
      fill:  mixture of 0 (white) and 3 (green)
      pattern:
          type: filled, irregular, symmetrical along both horizontal and vertical center line.
          details:
              - green(3) pixels occupy all border cells.
              - green(3) pixels form a cross like feature in the central 6x6 sub grid.
relationships:
  - input_to_output: transformation changes pixel values from 0 to 3 based on an apparent pattern.
```


**Natural Language Program:**

1.  **Outline:** Create a 10x10 grid.
2.  **Border:** Fill the outermost border (top, bottom, left, and right edges) of the grid with green pixels (value 3).
3. **Central Cross:** in the central 6 x 6 grid (i.e., skip the first and last row and first and last column), make a cross with arm length 3 (including the center pixel, which will already be set to 3 from previous step):
    *   Fill the central vertical line and center horizontal line within the 6 x 6 grid with green(3) pixels except for the pixels at locations (3,1),(3,8) and (8,3),(8,8) where (0,0) is top left.
4.  **Background:** All other pixels remain white (value 0).

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
