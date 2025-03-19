# 496994bd • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```

<PIL.Image.Image image mode=RGB size=192x640 at 0x786C54881150>

**output:**
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
3 3 3
2 2 2
2 2 2
```

<PIL.Image.Image image mode=RGB size=192x640 at 0x786C547D3C50>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid appears to be transformed into a modified output grid. The primary colors involved are red (2), green (3), and white (0). The transformation seems to involve some form of rearrangement or duplication of rows. The output appears to preserve some structures and also invert some structures from the bottom.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      rows: 10
      columns: 3
      colors: [0, 2, 3]
  - type: row
    properties:
      pixels: [color values]
  - type: pixel
     properties:
        color: int #between 0-9

actions:
    - name: copy_rows
    - name: reverse_rows
    - name: mirror_rows
    - name: append_rows

relationships:
  - type: row_contains_pixels
  - type: grid_contains_rows
```


**Natural Language Program:**

1.  **Identify Key Regions:** Divide the input grid conceptually into two regions:
    *   The top three rows (colored region).
    *   The remaining seven rows (white region).
2.  **Copy and Preserve:** Copy the top three rows (the colored region) to the output grid, maintaining their original order and position.
3. Copy the white region (next 4 rows) to the output
4. **Mirror the top:** Reverse rows from the top of the input and copy it to the bottom of the output.

In summary, the top part of the grid containing colors is preserved, the next part is preserved and the bottom part of the grid contains a reflection of the upper colored part, in reverse order.

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
