# 928ad970 • 018 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 4 0 0 4 0 0 0 0 5 0
0 0 0 0 4 0 0 4 0 0 0 0 0 0
0 5 0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=896x960 at 0x7F4C1A58BED0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 4 0 0 0 0 0 0 0 0 4 0 0
0 0 4 0 4 4 4 4 0 0 0 4 0 0
0 0 4 0 4 0 0 4 0 0 0 4 5 0
0 0 4 0 4 0 0 4 0 0 0 4 0 0
0 5 4 0 4 4 4 4 0 0 0 4 0 0
0 0 4 0 0 0 0 0 0 0 0 4 0 0
0 0 4 0 0 0 0 0 0 0 0 4 0 0
0 0 4 0 0 0 0 0 0 0 0 4 0 0
0 0 4 4 4 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=896x960 at 0x7F4C1A58B050>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The primary colors involved seem to be gray (5), yellow (4), and white (0).  The transformation appears to involve expanding or "inflating" the yellow (4) region outwards, while maintaining the positions of isolated gray (5) pixels. The expansion respects a certain set of rules.

**YAML Block (Facts):**


```yaml
facts:
  - object: yellow_region
    type: contiguous_block
    color: 4
    initial_state: enclosed_shape
    action: expand_outward
    constraints:
      - maintain_connectivity
      - expand_to_max

  - object: gray_pixels
    type: single_pixels
    color: 5
    initial_state: isolated
    action: maintain_position
    constraints: []

  - object: white_pixels
    type: background
    color: 0
    initial_state: fills_space
    action: recede_as_yellow_expands
    constraints: []
```


**Natural Language Program:**

1.  **Identify Objects:** Locate all contiguous regions of yellow (4) pixels and isolated gray (5) pixels within the input grid.

2.  **Preserve Gray Pixels:** The positions of the isolated gray (5) pixels remain unchanged in the output grid.

3.  **Expand Yellow Region:** The yellow (4) region expands outwards in all directions (up, down, left, and right).

4. **Expansion Rules:**
    *   The yellow pixels expand one layer at time.
    *   The expansion happens until the yellow region takes the maximum possible area.
    *   The yellow region expands around any white space (0) but does not go over other colors.

5.  **Output:** The resulting grid after performing the expansion and preserving gray pixel locations represents the transformation.

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
