# 445eab21 • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 7 7 7 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B1DDE6E04D0>

**output:**
```
8 8
8 8
```

<PIL.Image.Image image mode=RGB size=128x128 at 0x7B1DDE6A1850>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Task Elements:**

The task involves transforming a grid of colored pixels (represented by numbers 0-9) into a smaller grid. The input grid contains two distinct shapes, one orange (7) and one azure (8). The output grid consists only of azure (8) pixels, arranged in a 2x2 square. The orange shape and all white (0) pixels are absent from the output. It appears that the transformation is selecting a specific object based on color and possibly shape, and extracting a sub-grid.

**YAML Fact Block:**


```yaml
facts:
  - observation: Input grid is 10x10, output grid is 2x2.
  - object: OrangeShape
    color: orange (7)
    location: Top-left quadrant of input grid.
    shape: Irregular, resembling a reversed 'L'.
  - object: AzureShape
    color: azure (8)
    location: Center-bottom region of input grid.
    shape: Irregular, resembling an 'L'.
  - object: OutputShape
    color: azure (8)
    location: Output grid.
    shape: 2x2 square.
  - relationship: OutputShape is a sub-component of InputShape Azure.
  - action: extraction
    target: AzureShape
    result: OutputShape
```


**Natural Language Program:**

1.  **Identify Objects:** Locate all distinct contiguous regions of pixels with the same color within the input grid. Consider these regions as separate objects.
2.  **Filter by Color:** Disregard all objects that are *not* colored azure (8).
3.  **Select Sub-grid:** find, and extract the smallest 2x2 square sub-grid in azure. If no such subgrid exist output nothing.
4. output the sub-grid.


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
