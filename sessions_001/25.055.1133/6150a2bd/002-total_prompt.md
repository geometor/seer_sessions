# 6150a2bd • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
3 3 8
3 7 0
5 0 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x78FDACE64490>

**output:**
```
0 0 5
0 7 3
8 3 3
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x78FDACE659C0>
Okay, here's my analysis of the example input-output pair, structured as requested:

**Perception of Elements:**

The task involves a 3x3 grid of single-digit integers, each representing a color. The transformation appears to rearrange the grid elements without changing the set of unique digits present. The overall structure (3x3 grid) is preserved. The central element (7, orange) remains in the center. The other numbers seem to have been mirrored, across both vertical and horizontal axes.

**YAML Fact Documentation:**


```yaml
facts:
  - type: grid
    dimensions: 3x3
    elements: single_digit integers (0-9)
    element_type: color_code
  - observation: input_grid_structure is preserved in output_grid
  - observation: unique_elements in input == unique_elements in output
  - observation: central element (index [1][1]) remains unchanged
  - transformation: mirroring
    axis: both vertical and horizontal
    details: each element moves to its opposite position relative to the center
```


**Natural Language Program:**

1.  **Preserve Structure:** Maintain the 3x3 grid structure.
2.  **Center Lock:** Keep the central element (at row 1, column 1) in its original position.
3.  **Mirror Elements:** For all other elements, swap their position across both the horizontal and vertical axes. Specifically, an element at position (row, col) will move to position (2-row, 2-col). This can also be looked upon as rotation of the matrix by 180 degrees.


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
