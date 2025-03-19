# cdecee7f • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 3
0 0 5 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 1 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B6BFDD0>

**output:**
```
2 4 5
1 9 3
5 1 3
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7F4C1B6BF550>
Okay, I'm ready to analyze this input-output pair and try to discern the transformation rule. Here's my report:

**Perception of Elements:**

*   The input is a 10x10 grid of single-digit integers (0-9), representing colors. Most of the grid is filled with 0 (white), with a few scattered non-zero colored pixels.
*   The output is a 3x3 grid, also of single-digit integers. It seems to contain only the non-zero digits from the input grid, but rearranged.
*   The colors are maintained in transfer, so numbers have the same color
    meaning.

**Facts (YAML):**


```yaml
facts:
  - type: grid
    description: Input grid is 10x10, Output grid is 3x3.
    elements: Integers 0-9, representing colors.
  - object: non_zero_pixels
    description: Pixels in the input grid with values other than 0.
    properties:
      - color: Represented by their integer value.
      - position: Original (x, y) coordinates in the input grid.
  - action: extraction
    description: Non-zero pixels are extracted from the input grid.
  - action: rearrangement
    description: The order of extracted pixels appears changed in a structured
      way.
  - relationship: input_to_output
    description: Non-zero pixels from input, maintaining color, compose the
      output arranged into a 3x3 matrix.

```


**Natural Language Program:**

1.  **Identify:** Find all non-zero pixels within the 10x10 input grid.
2.  **Extract:** Collect these non-zero pixel values, preserving their original color (value).
3.  **Order:** Take the non-zero digits and place in reading order into the cells
    of the 3 x 3 output.
4.  Specifically, reading top to bottom, left to right.
5.  **Output**: construct new 3x3 grid with the digits.

Essentially the program extracts all of the colored numbers and places them in
order into a new, smaller, grid.

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
