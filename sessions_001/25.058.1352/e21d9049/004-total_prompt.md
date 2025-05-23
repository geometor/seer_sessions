# e21d9049 • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
8 3 2 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x768 at 0x7ACD21382E90>

**output:**
```
0 0 3 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
8 3 2 8 3 2 8 3 2 8 3
0 0 8 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x768 at 0x7ACD21382AD0>
Okay, here's my analysis of the provided input-output example pair, formatted as a report:

**Perception of Elements:**

The task involves 2D grids of colored pixels. The input grid contains a cluster of non-zero pixels (8, 3, and 2 - azure, green, and red, respectively) in the top-left quadrant, surrounded by zeros (white). The output grid retains the original cluster but also extends it. Specifically, the fifth row of the input, containing `8 3 2`, appears to be replicated horizontally to fill the rest of that row. Moreover, a vertical mirrored expansion is observed, where the non-zero section of the first three rows ( `8`, `3` and a column containing `3`, `2` on rows 2,3 and 8 on rows 1 ) are mirrored downwards along column 3.

**YAML Fact Documentation:**


```yaml
facts:
  - object: input_grid
    type: 2D_array
    properties:
      dimensions: 12x11
      elements: integers (0-9) representing colors
      non_zero_cluster:
        location: top-left
        colors: [8, 3, 2]
        shape: irregular

  - object: output_grid
    type: 2D_array
    properties:
      dimensions: 12x11
      elements: integers (0-9)
      pattern: partial horizontal and vertical replication of input_cluster

  - actions:
    - name: horizontal_replication
      description: The sequence '8 3 2' on row 5 in input is extended across the row.
    - name: vertical_mirroring
      description: Columns are replicated below row 3.
```


**Natural Language Program:**

1.  **Identify the Core:** Locate the contiguous non-zero cluster of pixels in the input grid. In this example it is pixels with values 8,3,2 near the top left.

2.  **Horizontal Expansion:** Identify row 5 of the input grid. Replicate the non-zero pixel sequence ('8 3 2') across the entire width of the output grid on the corresponding row (row 5).

3. **Vertical mirroring**. Take the column of pixels in the core (column 3). Mirror these below the core downwards.

4.  **Preserve and fill**: The original core is kept in the output. Fill every other value with 0.

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
