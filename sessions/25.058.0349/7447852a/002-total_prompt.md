# 7447852a • 002 • example_1 • investigate_coder

---

## Example 1

**input:**
```
2 0 0 0 2 0 0 0 2 0
0 2 0 2 0 2 0 2 0 2
0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x76911E9725D0>

**output:**
```
2 0 0 0 2 4 4 4 2 0
4 2 0 2 0 2 4 2 0 2
4 4 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x192 at 0x76911EB263F0>
Okay, here's my analysis of the provided example, formatted as a report:

**Perception of Elements:**

The task involves transforming a grid of colored pixels (represented by numbers) into another grid of the same dimensions. The colors involved are primarily white (0) and red (2), with the introduction of yellow (4) in the output. The spatial arrangement of the red pixels seems to influence the placement of yellow pixels. Specifically, it appears that solid, contiguous blocks of red trigger changes, while interspersed reds may not, and yellow fills the same shape, like a flood-fill constrained to a region.

**YAML Block - Facts:**


```yaml
objects:
  - type: grid
    properties:
      - dimensions: 3x10 (rows x columns)
      - cells:
          values: [0, 2, 4]  # white, red, yellow
          mapping:
            0: white
            2: red
            4: yellow

  - type: region
    properties:
      - color: red
      - shape: variable
      - connectivity: contiguous # adjacent pixels of the same color

actions:
  - name: fill
    properties:
      - target: region
      - color: yellow
      - trigger: "red region of size >=3"
      - constraint: "within original region boundary"

relationships:
  - type: spatial
    description: "Yellow regions replace spatially equivalent red regions."
  - type: conditional
    description: "Red regions trigger yellow fill if continuous region size >=3."
```


**Natural Language Program:**

1.  **Identify Red Regions:** Scan the input grid and identify all contiguous regions of red (2) pixels. A region is defined as a group of horizontally or vertically adjacent pixels of the same color.
2.  **Filter large regions:** Keep regions of red pixels that contains 3 or more pixels.
3.  **Fill with Yellow:** For each region identified above, change the color of those pixels to yellow (4) in the output grid.
4.  **Preserve Other Pixels:** All other pixels in the input grid that are not part of a large red region retain their original color in the output grid.

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
