# db3e9e38 • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x7778518FB250>

**output:**
```
8 7 8 7 8 7 8
0 7 8 7 8 7 0
0 0 8 7 8 0 0
0 0 0 7 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x7778518FB430>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a grid of numerical values (representing colors) into another grid of the same dimensions. The primary object is a vertical line of orange (7) pixels. The transformation seems to involve "detecting" this line and creating a patterned "cross" or "plus sign" around it, using azure (8) and the original orange (7). The background remains unchanged. The size and shape of the grid seem to be preserved.

**YAML Fact Block:**


```yaml
facts:
  - object: vertical_line
    color: orange (7)
    position: column 4 (index 3)
    length: 4
  - transformation: create_cross
    center_object: vertical_line
    horizontal_arm_color: azure (8)
    vertical_arm_color: orange (7)
    background: unchanged
  - grid:
      input_dimensions: 5x7
      output_dimensions: 5x7
```


**Natural Language Program:**

1.  **Identify the vertical line:** Find the contiguous vertical line of orange (7) pixels. Note its vertical extent and horizontal position.
2.  **Construct the vertical arm:** Maintain the original orange (7) line in the output grid.
3.  **Construct the horizontal arms:** For each row containing part of the original vertical orange line, place an azure (8) pixel to the immediate left and right of the orange pixel.
4. **extend horizontal arms:** Extend the arm to the border, alternating the colors of the pixels
5.  **Preserve the background:** All other pixels in the input grid that are not part of the constructed cross should retain their original values in the output grid.

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
