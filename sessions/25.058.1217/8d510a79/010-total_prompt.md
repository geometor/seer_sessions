# 8d510a79 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 2 0 1 0 0 0 0 0 0
0 0 0 0 0 2 0 1 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 2
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 2 0 1 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x741F72B1A3F0>

**output:**
```
0 2 0 1 0 0 0 1 0 0
0 2 0 0 0 2 0 1 0 0
0 2 0 0 0 2 0 0 0 0
5 5 5 5 5 5 5 5 5 5
0 2 0 0 0 0 2 0 0 2
0 2 0 0 0 0 2 0 0 2
0 0 0 0 1 0 2 0 0 0
0 0 0 0 1 0 2 0 0 0
0 0 1 0 1 0 2 0 1 0
0 0 1 0 1 0 0 0 1 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x741F72B1B250>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (10x10).
*   The grids contain single-digit integers representing colors.
*   The most prominent feature is a horizontal line of '5's (gray) across the middle.
*   Above and below this line are scattered instances of '1' (blue), '2' (red), and '0' (white).
*   The transformation seems to involve some kind of duplication or mirroring of elements, potentially around the gray line. There is an increase of the number of colored object of the same color and shape.

**YAML Fact Block:**


```yaml
facts:
  - object: grid
    properties:
      dimensions: 10x10
      elements: integers (0-9)
      colors:
        0: white
        1: blue
        2: red
        5: gray
  - object: horizontal_line
    properties:
      color: gray (5)
      position: row 4 (index 3)
      length: 10
  - object: colored_pixels
    properties:
        colors: blue (1), red (2)
    observations:
      - location: scattered above and below the horizontal line
      - change: number of instances appear to increase in output

  - action: duplication
    description:  Colored pixels above the gray line are duplicated below it, and vice-versa. The position within each vertical line relative to the grey line matters.
```


**Natural Language Program:**

1.  **Identify the central gray line:** Locate the horizontal line of gray (5) pixels at row 4 (index 3).
2.  **Iterate the columns.** Iterate through each of the columns.
3.  **Duplicate above and below.** For each colored pixel, going from the grey line to the edges of the grid, duplicate the current color to the output grid. For example, looking at the first column, from the grey line to the top: white, white, red, white -> write to the ouput, starting at the grey line: white, red, white, white. Then repeat for the other side of the grey line.

Essentially, colored pixels above the grey lines are copied to the equivalent spot below and vice-versa. The grey lines are unchanged.

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
