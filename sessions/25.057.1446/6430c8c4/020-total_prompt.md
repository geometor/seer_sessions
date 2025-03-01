# 6430c8c4 • 020 • example_4 • investigate_coder

---

## Example 4

**input:**
```
7 0 7 0
0 0 7 7
7 0 7 7
7 7 0 0
4 4 4 4
0 0 2 2
0 0 0 0
2 0 0 2
0 2 0 2
```

<PIL.Image.Image image mode=RGB size=256x576 at 0x786C546CBC50>

**output:**
```
0 3 0 0
3 3 0 0
0 3 0 0
0 0 3 0
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x786C546CB450>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grid contains various colors (represented by digits 0-9), while the output grid seems to simplify this information, focusing on specific areas and changing the colors. There's a reduction in both dimensions and the number of distinct colors used. The output grid appears to highlight a specific pattern or feature extracted from the input, and replaces the highlighted color with green (3).

**YAML Fact Documentation:**


```yaml
facts:
  - observation: Input grid is 9x4 (rows x columns).
  - observation: Output grid is 4x4.
  - observation: Input grid contains colors 0, 2, 4, and 7.
  - observation: Output grid contains colors 0 and 3.
  - observation: The upper-left 4x4 subgrid of the Input relates to output.
  - object: Top-Left Object
    properties:
      - shape: "rectangle"
      - color: 7 (orange)
      - location: (0,0) to (3,3) with missing bottom right cell.
      - action: The shape made by color 7 is replaced by 3.
  - object: Bottom-Right Object
    properties:
      - shape: rectangle
      - location:
      - action: Bottom Right object in input is deleted.
```


**Natural Language Program:**

1.  **Focus Area:** Consider only the top-left 4x4 section of the input grid.
2.  **Identify primary shape:** In the area of interest, identify locations of color 7 (orange).
3. **Replace color:** Create an output grid 4x4 where identified locations are color 3, every other cell is 0.


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
