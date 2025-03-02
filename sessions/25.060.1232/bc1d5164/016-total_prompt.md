# bc1d5164 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
4 4 0 0 0 4 0
0 0 0 0 0 4 4
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x7CE41B97A350>

**output:**
```
4 4 0
0 4 4
4 0 4
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7CE41B8FFC50>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves a grid of numbers, representing colored pixels. The primary colors present are yellow (4) and white (0). The input grid is larger (7x5) than the output grid (3x3). The output grid seems to be a condensed or cropped version of the input, focusing only on the yellow pixels and some of the surrounding white pixels. The relative positions of the yellow pixels are maintained.

**YAML Block (Facts):**


```yaml
objects:
  - type: grid
    properties:
      dimensions:
        input: [5, 7]
        output: [3, 3]
      elements:
        type: pixel
        values: [0, 4]
        colors:
          0: white
          4: yellow
    
  - type: pixel_group
    properties:
    color: yellow
      locations:
        input: [[0,0], [0,1], [0,5], [1,5], [1,6], [4,0], [4,6]]
        output: [[0,0], [0,1], [1,1], [1,2], [2,0], [2,2]]

actions:
  - type: crop_or_condense
    description: "The input grid is reduced in size to form the output grid."

  - type:  filter_color_and_neighbors
    description: "keep only the target color (yellow) and empty (white) neighbors"

relationships:
  - type: spatial_preservation
    description: "The relative positions of the yellow pixels are maintained between the input and output grids."
```


**Natural Language Program:**

1.  **Identify Target Pixels:** Locate all pixels with the value 4 (yellow) in the input grid.

2.  **Determine Output Grid Size:** it will be the minimum size necessary
    to include all target (yellow) pixels, maintaining relative target pixel
    positions

3.  **Extract Subgrid:** Extract the minimum size including all non-zero value
    pixels

4.  Create output grid, keep only the minimum positions of the original grid with target values

In essence, the transformation extracts a subgrid containing only the yellow
pixels and their immediate white neighbors, discarding the rest. The minimal
subgrid containing the target values and immediate neighbor is the output.

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
