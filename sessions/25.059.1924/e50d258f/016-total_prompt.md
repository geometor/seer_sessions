# e50d258f • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
2 8 8 8 0 0 0 0 0 0
8 8 1 8 0 0 0 0 0 0
1 8 8 8 0 0 0 0 0 0
8 8 8 2 0 0 1 8 8 2
8 2 8 1 0 0 8 8 1 8
8 1 8 8 0 0 8 2 8 8
0 0 0 0 0 0 8 8 8 1
0 0 0 0 0 0 1 8 8 8
0 0 0 0 0 0 8 8 1 8
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x71663D535BD0>

**output:**
```
2 8 8 8
8 8 1 8
1 8 8 8
8 8 8 2
8 2 8 1
8 1 8 8
```

<PIL.Image.Image image mode=RGB size=256x384 at 0x716635B76450>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid is larger than the output grid. The colors present in the example are red (2), azure (8), blue (1), and white (0). The output grid seems to be a cropped portion of the input grid, specifically the top-left corner, but only includes the colored pixels, excluding the white ones.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      - name: input_grid
        dimensions: 10x10
        colors: [red, azure, blue, white]
      - name: output_grid
        dimensions: 6x4
        colors: [red, azure, blue]
relationships:
  - type: spatial
    description: The output grid appears to be a cropped section of the input grid.
  - type: color_filtering
    description: White pixels in input are not in output
actions:
  - type: cropping
    description: A section of the input grid is selected.
  - type: filtering
    description: White pixels are removed.

```


**Natural Language Program:**

1.  **Identify the Sub-grid:** Locate the smallest rectangular sub-grid within the input grid that contains all non-white pixels. In this instance it would seem that starting search in upper left corner of input.
2.  **Crop:** Extract this sub-grid.
3. **Filter**: Remove all white pixels


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
