# d8c310e9 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0 0 0 0 0 0
3 3 2 1 3 3 2 1 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x320 at 0x716635BBB250>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2
0 0 2 0 0 0 2 0 0 0 2 0 0 0 2
3 3 2 1 3 3 2 1 3 3 2 1 3 3 2
```

<PIL.Image.Image image mode=RGB size=960x320 at 0x716635B765D0>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

*   We have two grids: an input grid and an output grid.
*   Both grids have the same dimensions (5 rows x 15 columns).
*   The grids contain single-digit integers, representing colors.
*   The majority of the cells are '0' (white).
*   There are patterns of '2' (red), '1' (blue), and '3' (green).
*    The last row of the input is maintained and another instance of it is constructed in the output.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: 2D array
    dimensions: 5x15
    elements: integers (0-9)
  - name: output_grid
    type: 2D array
    dimensions: 5x15
    elements: integers (0-9)
  - name: red_blocks
    type: object
    color: 2 (red)
    shape: vertical bar (1x2)
  - name: blue_blocks
    type: object
    color: 1 (blue)
    shape: single cell
 - name: green_block
    type: object
    color: '3'
    shape: single cell

actions:
  - type: copy
    description: Certain elements from the input grid are copied to the output grid.
  - type: extend
    description: copy and extend the red blocks to the right

relationships:
  - input_output_same_dimensions: The input and output grids have the same dimensions.
  - row_preservation: The last row of the input grid is preserved in the output grid.
  - vertical_bar_duplication: every other column, starting at column 2, containing the
    red block has now been duplicated two columns to the right, starting from column 10.
```


**Natural Language Program:**

1.  **Copy the last row:** Copy the last row of the input grid directly to the last row of the output grid.
2.  **Copy red blocks:** Copy the vertical red blocks (color 2) in rows 3 and 4, columns 2 and 6 in the input grid to the same location in the output grid.
3.  **Extend:** For any red block detected in the third and fourth rows, mirror those red blocks two cells to their right.
4. **Fill empty cells** Every other cell will remain unchanged.


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
