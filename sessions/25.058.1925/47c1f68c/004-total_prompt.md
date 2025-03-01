# 47c1f68c • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 2 0 0 0 0 0
0 1 0 0 0 2 0 0 0 0 0
1 1 0 0 0 2 0 0 0 0 0
0 1 1 0 0 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x704 at 0x78E5F214A3D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 0 0 0 2 0
2 2 0 0 0 0 0 0 2 2
0 2 2 0 0 0 0 2 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 2 2 0
2 2 0 0 0 0 0 0 2 2
0 2 0 0 0 0 0 0 2 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F214A450>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input and output are grids of digits, likely representing colors.
*   The input grid has a prominent vertical line of '2's (red) in the center, and a horizontal line of '2's across the middle. It forms a plus shape. There is a small cluster of blue "1" in the upper left corner.
*    The output appears have transformed the existing red objects and their locations, but blue is completely removed.
*   The output grid seems to maintain some, but not all, of the red ('2') pixels from the input, arranged around a blank space.

**YAML Block (Facts):**


```yaml
objects:
  - name: red_line_vertical
    type: line
    color: red (2)
    orientation: vertical
    position: center_column
    behavior: partially_remains

  - name: red_line_horizontal
    type: line
    color: red (2)
    orientation: horizontal
    position: center_row
    behavior: partially_remains

  - name: blue_cluster
    type: cluster
    color: blue (1)
    position: top_left
    behavior: disappears
    
  - name: background
    color: white (0)
    behavior: remains
```


**Natural Language Program:**

1.  **Remove Blue:** Eliminate all blue (1) pixels from the input grid.
2.  **Vertical Red Reduction**: On the original central vertical red line, keep only two pixels on either side of the middle horizontal line.
3. **Horizontal Red Reduction:** on the original central horizontal red line, keep only two pixels on either side of the middle vertical line.
4.  **Background Preservation:** The white (0) background pixels remain unchanged where there are no other colored pixels.

Essentially, the transformation removes the blue object, and reduces original central plus-shaped object.

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
