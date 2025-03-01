# beb8660c • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 1
0 0 0 0
2 2 2 0
0 0 0 0
0 3 3 0
0 0 0 0
8 8 8 8
```

<PIL.Image.Image image mode=RGB size=256x448 at 0x7778516016D0>

**output:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 1
0 0 3 3
0 2 2 2
8 8 8 8
```

<PIL.Image.Image image mode=RGB size=256x448 at 0x777851601DB0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The input and output grids have the same dimensions (7x4).  There are distinct horizontal lines of single colors (blue, red, green, azure) in the input. The output seems to reorder these lines, and some empty rows are inserted while other empty rows are deleted. The order of the colored lines appears to relate to the row index they initially occupy.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions: 7x4
      cells: integers (0-9) representing colors
  - type: line
    properties:
      orientation: horizontal
      color: single color per line (blue, red, green, or azure)
      length: varies (1 to 4 pixels)

actions:
  - type: reorder
    description: Lines are moved to different rows.
  - type: insert
    description: insert blank rows
  - type: delete
    description: delete blank rows

relationships:
  - input_grid: contains colored lines and empty rows
  - output_grid: contains the same colored lines as the input, reordered, and blank rows at the beginning
  - line_order: original row index of a colored line seems to influence its final position
```


**Natural Language Program:**

1.  **Identify Colored Lines:** Find all horizontal lines consisting of one or more contiguous pixels of the same non-zero color.
2.  **Determine New Order using Original index**: Add empty rows on the top. For the colored line, put them at the index that is equal to the number of rows from that row to the bottom.
3. **Reconstruct Grid:** fill the top lines with 0. Arrange the original line based on the new order.


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
