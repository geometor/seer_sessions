# 760b3cac • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 8 0 8 0 0 0
0 0 0 0 8 8 0 0 0
0 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x384 at 0x7778514437F0>

**output:**
```
8 0 8 8 0 8 0 0 0
8 8 0 0 8 8 0 0 0
8 0 0 0 0 8 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 4 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x384 at 0x777851399B30>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The colors present are white (0), azure (8), and yellow (4). The input and output grids have the same dimensions (9x6). The yellow object remains unchanged. The azure object in the input is modified in the output. Some azure pixels are added.

**YAML Fact Block:**


```yaml
facts:
  - object_types:
    - color: yellow
      shape: irregular
      change: none
    - color: azure
      shape: irregular
      change: added pixels
  - grid_properties:
    - dimensions: 9x6
    - same_dimensions: true # Input and output grids have the same dimensions
  - spatial_relationships:
      - type: adjacency
        description: "Pixels of the same color adjacent to each other form objects."
  - transformations:
      - type: addition
        description: Azure pixels are added to the top of existing azure pixels
        constraints: only to azure pixels on the top edge of azure object

```


**Natural Language Program:**

1.  **Identify Objects:** Locate all contiguous blocks of pixels of the same color. These are the objects.
2.  **Preserve Yellow:** The yellow (4) object remains unchanged between the input and output.
3.  **Copy Azure:** The original azure objects are copied from the input.
4. **Extend the Azure objects** For each column that contains azure (8) pixels, add azure colored pixels above the original azure area, filling to the top edge of the grid.


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
