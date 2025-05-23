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

<PIL.Image.Image image mode=RGB size=320x320 at 0x7BFC47FB9A80>

**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x7BFC48A63190>
Okay, here's my analysis of the provided example, focusing on perception, structured observations, and a natural language program describing the transformation.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (5x5 in this case).
*   The grids contain single-digit integers representing colors.
*   Most of the grid cells are '0' (white).
*   There are a few non-zero colored cells, including '8' (azure) and '3' (green).
*   The bottom row appears to remain unchanged.
*  The green '3' in the bottom row seems important

**YAML Block (Facts):**


```yaml
facts:
  grid_dimensions:
    width: 5
    height: 5
  input_objects:
    - color: 3  # Green
      positions: [[4, 2]] #row, col
    - color: 8  # Azure
      positions: [[3,2], [4,0], [4,1], [4,3], [4,4]]
    - color: 0 # White
      positions: "all other cells"
  output_objects:
    - color: 3
      positions: [[1,0], [1,4], [2,1], [2,3], [4,2]]
    - color: 8
      positions:  [[3,2], [4,0], [4,1], [4,3], [4,4]]
    - color: 0
      positions: "all other cells"

  actions:
    - name: copy_bottom_row
      description: The bottom row of the input grid is preserved in the output grid.
    - name: green_expansion
      description:  New green '3' pixels appear in the output grid.
    - name: azure_preservation
      description: the azure pixels are preserved.
  relationships:
    - type: spatial
      description: The new green pixels form a cross shape around existing green and azure pixels, and on their own.

```


**Natural Language Program:**

1.  **Preserve the Bottom Row**: Copy the entire bottom row of the input grid directly to the output grid.
2.  **Preserve other colors**: Copy all non-zero color values, except the green '3', to the output grid in the same locations
3.  **Green Expansion:**.
    - Find the green (3) pixel in the bottom row
    - Create additional green pixels up and to either side in a cross shape, from row 1 to row 2

This program explains all changes from input to output. The azure pixels are copied and the green 3 expands.

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
