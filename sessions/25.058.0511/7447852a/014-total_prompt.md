# 7447852a • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x192 at 0x7B1DDE7AB850>

**output:**
```
2 0 0 0 2 4 4 4 2 0 0 0 2 0 0 0 2 4
4 2 0 2 0 2 4 2 0 2 0 2 4 2 0 2 0 2
4 4 2 0 0 0 2 0 0 0 2 4 4 4 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x192 at 0x7B1DDE42C2D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves 2D grids containing numerical values representing colors. The input grid contains the colors red (2) and white (0). The output grid introduces a new color, yellow (4), while retaining some reds and whites from the input. The positions of the red pixels seem to influence the placement of the yellow pixels. The shape and size of input and output grids are same.

**YAML Block (Facts):**


```yaml
facts:
  - observation: Input grid contains red (2) and white (0) pixels.
  - observation: Output grid contains red (2), white (0), and yellow (4) pixels.
  - observation: The dimensions of the input and output grids are identical (3x18).
  - relationship: Yellow pixels appear in the output grid in locations related to the positions of red pixels.
  - property: Red pixels adjacent to a white pixel horizontally (left or right) have a corresponding yellow pixel in that direction
```


**Natural Language Program:**

1.  **Iterate** through each cell of the input grid.
2.  **Identify** red (2) pixels.
3.  **For each red pixel**:
    *   **Check** its immediate horizontal neighbors (left and right).
    *  If any of the neighbors are white(0), **replace** that neighbor in the output grid with yellow(4).
4. **Copy all pixels without change, unless replaced in step 3**
    * all original red(2) pixels remain red(2).

In other words, any white pixel that is horizontally adjacent to a red pixel in the input becomes yellow in the output, while all other pixels remained unchanged.

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
