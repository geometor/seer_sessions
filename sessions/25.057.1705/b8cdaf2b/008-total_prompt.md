# b8cdaf2b • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x777851601DB0>

**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7778516D1450>
Okay, here's my analysis of the example input-output pair, presented as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The colors present are white (0), azure (8), and green (3). The input grid transforms into the output grid, with some changes in the pixel colors and their positions. The most notable changes are focused on the top three rows, seemingly added. It is very difficult to simply the task as there doesn't seem to be a clear relationship between the added rows to the input. The bottom two rows don't change, these are assumed to be the "background".

**YAML Fact Documentation:**


```yaml
facts:
  - observation: |
      The input and output grids are 5x5.
  - objects:
      - name: background
        description: The bottom two rows of the input, which are unchanged in the output.
        properties:
          - row_4: "0 0 8 0 0"
          - row_5: "8 8 3 8 8"
      - name: insertion
        description: added rows at top
        properties:
            - row_1: "0 0 0 0 0"
            - row_2: "3 0 0 0 3"
            - row_3: "0 3 0 3 0"
  - actions:
      - name: add rows
        description: adds rows at the top of the output grid
        details: |
            The insertion seems to be based on combining a completely blank row
            with rows containing green at the ends, alternating with the
            middle.
  - relationships:
      - type: unchanged
        from: background input
        to: background output
      - type: added
        from: insertion
        to: top rows output
```


**Natural Language Program:**

1.  **Identify Background:** Locate the bottom two rows of the input grid. These will remain unchanged.
2.  **Maintain Background:** Copy the identified two bottom rows directly to the output grid.
3. **Construct rows to insert:**
    *   The first inserted row will be all 0.
    *   The second inserted row will be green (3) at opposite ends of the row, filling the remaining spaces with white (0).
    *   The third inserted row is the same at the second inserted row except the green elements (3) are adjacent to the end, filling the remaining spaces with white (0)
4.  **Combine:** insert the constructed rows at the top of the output.


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
