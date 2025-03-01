# 6430c8c4 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 7 7
0 0 7 7
0 7 7 0
7 7 0 0
4 4 4 4
2 0 2 0
0 2 0 2
0 2 2 0
0 0 2 0
```

<PIL.Image.Image image mode=RGB size=256x576 at 0x786C548818D0>

**output:**
```
0 3 0 0
3 0 0 0
3 0 0 3
0 0 0 3
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x786C54883450>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a larger, multi-colored grid (input) into a smaller, single-color grid (output). The input grid contains several distinct colored regions, while the output grid appears to represent a simplified, abstracted version of the input. The colors in the input do not directly translate to the color in the output; instead the relative color positions in the input determine locations in the output.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: input grid
    properties:
      - dimensions: 9x4 (height x width)
      - colors: [0, 7, 4, 2]
      - color_regions:
        - color: 7
          shape: rectangle
          location: top-left corner, extends to 2nd row and occupies top half
        - color: 4
          shape: rectangle
          location: 5th row, full width
        - color: 2
          shape: complex, "L" and mirrored "L" shapes, and single cell
          location: bottom rows, arranged in a pattern

  - type: grid
    description: output grid
    properties:
      - dimensions: 4x4
      - color: [0, 3]
      - color_regions:
          shape: rectangle
          color: 3
          location: occupies corners

  - transformation:
      type: abstraction/simplification
      details: input grid features are reduced to corner representations in output grid.
      input_to_output_mapping: |
        The output grid appears to be the same height, but maybe coincidental.
        The top two corner colors in the input grid are 7 (orange).
        The color 3 (green) in the output is placed where the color 7 would be.
        There is no color 3 in the input grid.

```


**Natural Language Program:**

1.  **Identify Input Corners:** Examine the input grid and identify the colors present in the four corners of the largest contiguous rectangles (in the 4 directions).

2.  **Map Top-Left Color:**
    *   Find the first instance of non-zero color moving from the top left, across the row and then down.
    *   Locate the color in the input grid that's occupying the "top-left" position of the input.

3.  **Create Output Grid:** Create a new grid that has the dimensions of the largest square, where the first instance of a non-zero color has been replaced with green (3). The other cells are white (0).

4.  **Populate Corners:** Using only the top section of the input image, find the color that fills the corners of that section and use its location for placing the color green in the output, or if that section has all corners equal to color 0, then skip.

In summary, the transformation constructs an output grid where cells in the four corners are colored based on the non-zero color from the input. The other cells will be filled with white (0).

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
