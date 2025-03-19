# 8a004b2b • 008 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 1 1 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1088x1088 at 0x7F2DF78BF7D0>

**output:**
```
4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 2 2 0 0 0
0 3 3 0 0 0 0 0 0 2 2 0 0 0
0 1 1 1 1 0 0 1 1 1 1 0 0 0
0 1 1 1 1 0 0 1 1 1 1 0 0 0
0 0 0 1 1 1 1 1 1 0 0 0 0 0
0 0 0 1 1 1 1 1 1 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=896x576 at 0x7F2DF787AF50>
Okay, here's my analysis of the provided input-output pair:

**Perception of Elements:**

The task involves manipulating colored squares on a grid. The input grid is larger than the output grid. The output grid seems to be a cropped and, in some areas, condensed version of the input grid. The colors present are white (0), blue (1), red (2), green (3), and yellow (4). The most striking feature is the consolidation of blue (1) squares.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: variable
      cells: contain color values (0-9)
  - type: square
    properties:
      color: integer (0-9)
      size: variable (single cell or contiguous block)

actions:
  - name: crop
    description: Reduce the overall dimensions of the grid.
  - name: condense
    description: Combine adjacent squares of the same color into a single, larger square or a line.
    conditions:
      colors: must be identical
      adjacency: must be directly touching (horizontal or vertical)

relationships:
  - type: adjacency
    description: Squares of the same color touching each other.
  - type: containment
    description: The output grid is a subset of the input grid (after cropping and condensing).

```


**Natural Language Program:**

1.  **Crop:** Remove the outer rows and columns of the input grid that consist entirely of white (0) pixels, stopping when a non-white pixel in any row or column is met.
2.  **Condense Blue:** Within the cropped region, locate all blue (1) squares. If multiple blue squares are adjacent horizontally or vertically, condense or connect those. Horizontal blue blocks attempt to connect by filling a line between the blocks if all colors inbetween are white. Vertical condensation simply merges contiguous vertically aligned blocks. Diagonal and isolated squares do not get condensed.
3. **Preserve other colors:** Other colored squares (red, green, yellow) are preserved from the cropped input to the output without modification to position or dimension, in the same absolute positions relative to each other.


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
