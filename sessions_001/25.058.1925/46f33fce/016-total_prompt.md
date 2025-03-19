# 46f33fce • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F99B4B50>

**output:**
```
3 3 3 3 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
3 3 3 3 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 4 4 4 4
1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 4 4 4 4
1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 4 4 4 4
1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 4 4 4 4
```

<PIL.Image.Image image mode=RGB size=1280x1280 at 0x78E5F99B47D0>
Okay, I'm ready to analyze this example. Here's my breakdown of the input-output pair, focusing on perception, facts, and a natural language program description.

**Perception:**

The input grid contains a few distinct colored pixels (green, red, blue, and yellow) scattered within a predominantly white (0) background. The output grid appears to create rectangular blocks of color, expanding from the locations of the initial colored pixels. The expansion seems to stop when different colored blocks meet, and the white background is largely preserved. The non-zero pixels seem to "claim" surrounding territory.

**YAML Fact Block:**


```yaml
facts:
  - description: "Identify non-zero pixels in the input grid."
    elements: [green (3), red (2), blue (1), yellow (4)]
  - description: "Each non-zero pixel initiates a region expansion."
    properties:
      - "Expansion occurs in orthogonal directions (up, down, left, right)."
      - "Expansion continues until another colored region or the edge of the grid is encountered."
  - description: "Expansion creates a rectangle around the original pixel"
    properties:
        - height: defined by other object or border
        - width: defined by other object or border
  - description: "White (0) pixels remain unchanged unless overtaken by an expanding colored region."
    properties:
      - "White is a passive background."
  - description: Each color expands to take up 1/4 of input
    properties:
      - height: 1/2 input height
      - width: 1/2 input width

```


**Natural Language Program:**

1.  **Locate:** Find all non-zero (colored) pixels in the input grid.
2.  **Expand:** For each non-zero pixel:
    *   Expand the pixel's color outward, creating a rectangle.
    *   Grow the rectangle equally in all orthogonal directions (up, down, left, and right).
    *   Stop expanding a side of the rectangle when it encounters:
        *   Another colored pixel's expanding region.
        *   The boundary of the input grid.
3.  **Preserve:** Leave all original white (0) pixels as white (0) unless they are within the expansion zone of a non-zero pixel.
4. **Equal Area:** The areas for each non-zero color expand to create areas of 1/4 of original input area. Each area is a rectangle of 1/2 input height and 1/2 input width.


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
