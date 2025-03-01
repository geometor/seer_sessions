# f15e1fac • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x716635C5CBD0>

**output:**
```
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 8 8 8 8 0 0 0 0
8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x716635BE9DD0>
Okay, let's analyze this example.

**Perception of Elements:**

*   The input and output are grids of the same dimensions (12x12).
*   The input grid contains a few non-zero pixels: azure (8) and red (2).
*   The azure pixels appear to be grouped in vertical lines.
*   The red pixels are on the bottom row.
*   The output grid seems to "extrude" or "reflect" the azure pixels horizontally. The number of times is decided by location.
* The red pixels remain unchanged.

**YAML Block (Facts):**


```yaml
objects:
  - type: pixel
    properties:
      color:
        - azure (8)
        - red (2)
        - white (0)
      position: (row, column)
  - type: grid
    properties:
      dimensions: 12x12

actions:
 - name: reflect_horizontally
   agent: azure_pixel_group
   condition: "location of the group"

relationships:
  - type: spatial
    description: Azure pixels are grouped vertically.
  - type: spatial
    description: Red pixels are located on the bottom row.
```


**Natural Language Program:**

1.  **Identify Azure Pixel Groups:** Find all groups of vertically contiguous azure (8) pixels in the input grid.
2.  **Horizontal Reflection:** For each distinct vertical group of azure pixels:
    *   If group in columns 0-3, extend to four 8s on the right.
    *   If group in columns 4-7, extend to four 8s on the left.
    *   If group in columns 8-11, extend to four 8s on the left.
3.  **Preserve Red Pixels:** Keep all red (2) pixels in their original positions in the output grid.
4. **Background:** All other cells will remain white (0)

Essentially, sections of the vertical azure lines are getting reflected.

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
