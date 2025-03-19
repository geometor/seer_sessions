# 3ac3eb23 • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 2 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x384 at 0x7778516016D0>

**output:**
```
0 2 0 0 0 8 0 0 0 0
2 0 2 0 8 0 8 0 0 0
0 2 0 0 0 8 0 0 0 0
2 0 2 0 8 0 8 0 0 0
0 2 0 0 0 8 0 0 0 0
2 0 2 0 8 0 8 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x384 at 0x7778518FB430>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves a grid of numerical values, each representing a color. The input grid appears to be transformed into an output grid of the same dimensions. The primary change seems to be the replication of certain colored pixels (represented by non-zero numbers) in a specific pattern. Specifically, the red (2) and azure (8) pixels are duplicated, creating a vertical line below each original instance of these colored pixel. The white pixels (0) are unchanged.

**YAML Fact Block:**


```yaml
facts:
  - type: grid
    description: Input and output are grids of the same dimensions.
  - type: cell_values
    description: Cell values represent colors (0-9).
  - type: colors
    description:
      0: white
      2: red
      8: azure
  - type: observation
    description: Non-zero pixels (2 and 8) are the focus of the transformation.
  - type: transformation
    description:  Replication of specific colored pixels.
  - type: pattern
    description: Red (2) and Azure (8) are replicated vertically downwards one line.
  - type: object_persistence
    description: White pixels (0) remain unchanged.
```


**Natural Language Program:**

1.  **Iterate** through each cell of the input grid.
2.  **Identify** cells with the values 2 (red) or 8 (azure).
3.  For each identified cell:
    *   **Copy** the value of the colored pixel to the cell immediately below it in the next row.
4.  **Preserve** all other cells (value 0 (white)) as they are.
5. The final output is the modified version of the grid.


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
