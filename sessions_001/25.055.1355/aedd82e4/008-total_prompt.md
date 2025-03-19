# aedd82e4 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
2 2 2 0
0 2 0 0
0 0 0 2
0 2 0 0
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7DCBFC2B4E80>

**output:**
```
2 2 2 0
0 2 0 0
0 0 0 1
0 1 0 0
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7DCBFC2B4F70>
Okay, here's my analysis of the provided example, focusing on perception, structured observations, and a natural language program describing the transformation.

**Perception of Task Elements:**

*   The input and output are grids of the same dimensions (4x4 in this case).
*   The grids contain single-digit integers, which represent colors.
*   The input grid contains only colors 0 (white) and 2 (red).
*   The output grid contains colors 0 (white), 1(blue) and 2 (red).
*   The red color (2) pixels in input remain same in the output grid.
*    Two of the white pixels in the input are changing to blue (1) in output. These two pixels appear to be related, they are the last of color 0 in the respective row/column, and each are adjacent to a color 2.

**YAML Fact Documentation:**


```yaml
facts:
  - observation: |
      Input and output grids are 4x4.
  - observation: |
      Input grid contains colors 0 (white) and 2 (red).
  - observation: |
      Output grid contains colors 0 (white), 1(blue) and 2 (red).
  - observation: |
    The color red (2) pixels locations are unchanged from input to output.
  - observation: |
      Some white (0) pixels in the input grid change to blue (1) in the output grid.
  - object: |
      Grid: A 2D array of pixels, representing colors.
  - property: |
      Color: An integer value (0-9) representing a specific color.
  - action: |
      ChangeColor: Modifying the color of a pixel from white (0) to blue(1).
  - relationship: |
    Input and Output have same size, red pixels unchanged, some white changed to blue.

```


**Natural Language Program:**

1.  **Preserve Reds:** Copy the input grid to the output grid, leaving all pixels with the color red (2) unchanged.
2.  **Identify Blue Candidates:** The pixels that were white in the input and in the bottom-right most location of contiguous white pixels in a row or column, adjacent to a red pixel, are candidates to become blue.
3. **Change to Blue:** The identified candidate pixels will change from color white(0) to color blue(1).


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
