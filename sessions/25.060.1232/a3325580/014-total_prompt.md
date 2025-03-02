# a3325580 • 014 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 4
0 9 0 0 0 6 0 0 4 4
0 9 9 0 0 6 0 0 0 4
9 9 0 0 6 6 6 0 0 0
0 9 0 0 0 0 6 0 0 0
0 9 9 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7CE41B8C38D0>

**output:**
```
9 4
9 4
9 4
9 4
9 4
9 4
9 4
9 4
9 4
```

<PIL.Image.Image image mode=RGB size=128x576 at 0x7CE41B9E74D0>
Okay, here's my analysis of the provided input-output pair:

**Perception of Elements:**

The task involves transforming a grid of colored pixels into a smaller grid. The input grid contains three distinct colored objects: maroon (9), magenta (6), and yellow (4). The output grid only contains maroon and yellow pixels, arranged in two columns. It seems that there is a selection and compaction to only two colors and the height is preserved, and width collapses.

**YAML Block (Facts):**


```yaml
facts:
  - input_grid_size: 10x10
  - output_grid_size: 9x2
  - input_colors:
    - maroon (9)
    - magenta (6)
    - yellow (4)
    - white(0)
  - output_colors:
    - maroon (9)
    - yellow (4)
  - input_object_maroon:
      shape: irregular
      position: left side, dispersed
  - input_object_magenta:
      shape: irregular
      position: middle, dispersed
  - input_object_yellow:
      shape: irregular, mostly top right corner
      position: right edge, dispersed
  - output_arrangement:
    - column_1: all maroon
    - column_2: all yellow
  - height_relationship: output height equals input height
```


**Natural Language Program:**

1.  **Identify Target Colors:** Identify the leftmost non-background (non-zero) color and rightmost non-background color in the input grid. These will be used to create output. In this case, first non-zero from left is 9 and last non-zero from right is 4.

2. **Preserve Height**: the output will have the height of original grid, less one because last line is all zeros.

3.  **Create Output Columns:** Create two output columns.

4.  **Populate Columns:** The first output column is filled entirely with the leftmost target color (maroon/9). The second output column is filled entirely with the rightmost target color (yellow/4).

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
