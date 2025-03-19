# 3aa6fb7a • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
0 0 0 0 0 0 0
0 8 0 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 0 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x786C6EBACB50>

**output:**
```
0 0 0 0 0 0 0
0 8 1 0 0 0 0
0 8 8 0 0 0 0
0 0 0 0 8 8 0
0 0 0 0 1 8 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x786C5497D8D0>
Okay, let's analyze this input-output example.

**Perception of Elements:**

The task involves a grid of pixels, most of which are white (0). There are some azure (8) pixels forming two distinct 2x2 squares, one in the top-left and another in the bottom-right. In the output, a single blue (1) pixel appears within each of the original azure squares. Specifically, the blue pixel replaces one of the azure pixels in the cluster.

**YAML Block (Facts):**


```yaml
facts:
  - observation: |
      The input grid contains two distinct clusters of azure (8) pixels.
  - object_1:
      type: cluster
      color: azure (8)
      shape: 2x2 square
      location: top-left
  - object_2:
      type: cluster
      color: azure (8)
      shape: 2x2 square
      location: bottom-right
  - transformation: |
      Within each azure cluster, one pixel is changed to blue (1).
  - location_change: |
        The pixel that changes within the top-left cluster is at relative position (1,0) of the object.
        The pixel that changes within the bottom-right cluster is at relative position (0,1) of the object.
  - environment:
    type: 2D grid
    background_color: white (0)
```


**Natural Language Program:**

1.  **Identify Clusters:** Find all contiguous clusters of azure (8) pixels.
2.  **Locate Target Pixels:** Within each identified cluster of azure pixels:
    * In the top-left cluster, find relative position (1, 0).
    * In the bottom-right cluster, find relative position (0,1)
3.  **Change Pixel Color:** Change the color of the pixel at the location specified to blue (1).
4. **Preserve other Pixels:** All other pixels retain their original color.

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
