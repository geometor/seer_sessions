# 8e1813be • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 4 4 4 4 4 4 4
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 5 5 5 5 5 5 0 8 8 8 8 8 8 8
0 5 5 5 5 5 5 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
6 6 6 6 6 6 6 6 6 6 6 6 6 6 6
```

<PIL.Image.Image image mode=RGB size=960x1152 at 0x7F2DF795C750>

**output:**
```
2 2 2 2 2 2
1 1 1 1 1 1
3 3 3 3 3 3
4 4 4 4 4 4
8 8 8 8 8 8
6 6 6 6 6 6
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7F2DF78BCBD0>
Okay, here's my analysis of the provided example, focusing on perception, documented facts, and a natural language program describing the transformation.

**Perception of Elements:**

The input is a larger grid, and the output is a much smaller grid. The output grid seems to be composed of select, complete horizontal lines from the input grid. The colors in the output grid are present in the input grid. The lines selected are not all adjacent, lines have been skipped or culled. Lines of all zeros are not present in the output. The selected lines appear to be ones of a uniform single color.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    description: 2D array of color values (integers 0-9)
    properties:
      - height: number of rows
      - width: number of columns
      - rows: list of rows, each row is a list of color values

  - type: color_line
    description: A horizontal line (row) in the grid with all pixels having the same color value.
    properties:
    - color: integer value representing the color
    - length: number of pixels (should match width of its parent grid)

actions:
  - select: Choose specific color_lines from the input grid.
  - construct: Build a new grid from the selected color_lines.

relationships:
  - input_grid: Contains multiple color_lines.
  - output_grid: Composed of a subset of color_lines selected from the input_grid.

```


**Natural Language Program:**

1.  **Identify** all horizontal lines (rows) in the input grid that consist of a single, uniform color. We can refer to these as "solid color lines".
2.  **Exclude** any solid color lines where the color is 0 (white/background).
3. **Select:** select the solid colored lines.
4.  **Construct** the output grid by vertically stacking the selected solid color lines, in the order that they appeared in the input grid.

Essentially, the transformation filters the input grid, keeping only the non-zero, solid-colored horizontal lines and stacking them to create the output grid.

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
