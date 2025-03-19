# e8593010 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 5 5 0 5 5 5 0 5
5 5 0 0 5 5 5 5 0 5
5 0 5 0 5 0 5 5 0 5
5 0 5 5 0 5 5 5 5 5
5 5 5 0 0 5 5 0 5 0
5 5 0 5 5 5 5 0 5 0
5 5 0 5 5 0 5 5 5 5
5 5 5 0 5 5 5 5 5 5
5 0 5 5 5 0 5 0 5 5
5 5 0 5 5 5 5 5 5 5
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635BBB650>

**output:**
```
2 2 5 5 3 5 5 5 1 5
5 5 1 1 5 5 5 5 1 5
5 2 5 1 5 3 5 5 1 5
5 2 5 5 1 5 5 5 5 5
5 5 5 1 1 5 5 2 5 2
5 5 2 5 5 5 5 2 5 2
5 5 2 5 5 3 5 5 5 5
5 5 5 3 5 5 5 5 5 5
5 3 5 5 5 3 5 3 5 5
5 5 3 5 5 5 5 5 5 5
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x716635C7AAD0>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (10x10).
*   The input grid primarily consists of two colors: gray (5) and white (0).
*   The output grid introduces three new colors, while gray(5) remains: red (2), green (3), and blue (1).
* It appears the white(0) pixels have been replaced with the new colors.
* There's a clear spatial relationship: The positions of the new coloured pixels in the output corresponds to the positions of the white pixels in the input.

**YAML Fact Block:**


```yaml
facts:
  - observation: Input and output grids have identical dimensions.
  - observation: Input grid contains only gray (5) and white (0) pixels.
  - observation: Output grid retains gray (5) pixels.
  - observation: White (0) pixels in the input are replaced by red (2), green (3), or blue (1) in the output.
  - relationship:  Spatial positions of gray pixels are consistent between input and output.
  - relationship: Spatial positions of new colors in the output correspond to white pixels in the input.
  - object_input:
      type: grid
      dimensions: 10x10
      colors: [gray, white]
  - object_output:
      type: grid
      dimensions: 10x10
      colors: [gray, red, green, blue]
```


**Natural Language Program:**

1.  **Preserve Gray:** Copy all gray (5) pixels from the input grid to the same positions in the output grid.
2.  **Transform White:** For each white (0) pixel in the input grid:
    *   If the white cell is at an even row and an even column, replace with red(2)
    *   If the white cell is at an odd row and an odd column, replace with green(3)
    *   If the white cell is at an odd row and an even column, OR an even row and an odd column, replace with blue(1)

Essentially the white pixels are replaced by a new color based on it's row, column parity, with:
* even, even -> red
* odd, odd -> green
* even, odd or odd, even -> blue

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
