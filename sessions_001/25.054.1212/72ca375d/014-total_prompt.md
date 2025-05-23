# 72ca375d • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 3 0 0 5 0 0 5 0
0 0 3 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
8 8 8 8 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7BFC47579600>

**output:**
```
5 0 0 5
5 5 5 5
```

<PIL.Image.Image image mode=RGB size=256x128 at 0x7BFC4757B670>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a larger, more complex grid (input) into a smaller, simpler grid (output). The input grid contains various colored pixels (represented by digits 0-9), while the output grid seems to focus on a specific color (in this case, 5, representing gray) and its arrangement. The output grid's dimensions are significantly smaller than the input. It appears the transformation involves extracting, simplifying, or summarizing specific features from the input grid.

**YAML Fact Block:**


```yaml
facts:
  - object: input_grid
    type: 2D array
    elements: integers (0-9) representing colors
    properties:
      - width: 10
      - height: 10
  - object: output_grid
    type: 2D array
    elements: integers (0-9) representing colors
    properties:
      - width: 4
      - height: 2
  - observation: color_focus
    value: 5 (gray)
    description: The output grid only contains pixels of color 5 and 0.
  - observation: spatial_relationship
    description: The arrangement of the '5' pixels in the output grid corresponds to the arrangement of a subset of '5' pixels within the input grid. The shape of the gray object is maintained.
  - observation: dimension_change
    description: output grid dimensions are not directly related by a simple scaling factor to the input grid.
```


**Natural Language Program:**

1.  **Identify Target Color:** The target color for extraction is gray (5).

2.  **Locate Target Objects:** Scan the input grid to find all connected components (objects) of the target color (gray).

3. **Select largest target object:** From the set of object, choose the one that has the most pixels.

4.  **Extract Bounding Box:** Determine the smallest rectangular region (bounding box) that fully encompasses the largest target object.

5.  **Create Output:** Create the output grid using on the selected object bounding box, using value '5' when the pixel exists, or value '0' if it does not exist in the source grid.

The core logic seems to be focused on identifying, isolating, and possibly simplifying a particular colored object (or multiple objects of the same color) from the input grid. The transformation maintains relative position, and object shape.

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
