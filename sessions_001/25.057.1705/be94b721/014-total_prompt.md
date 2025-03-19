# be94b721 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 7 7 0
0 0 8 0 0 0 2 0 0 7 0
0 8 8 0 0 2 2 0 0 7 0
0 8 8 0 0 0 2 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x384 at 0x7778518FB070>

**output:**
```
8 8 8
0 8 0
8 8 0
8 8 0
```

<PIL.Image.Image image mode=RGB size=192x256 at 0x777869E5D450>
Okay, here's my analysis of the example input-output pair:

**Perception of Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grid contains multiple colored regions (represented by different numbers/colors). The output grid seems to be a cropped or extracted portion of the input grid. The colors in output correspond to portions of an object of the input.

**YAML Block (Facts):**


```yaml
facts:
  - object: input_grid
    type: grid
    properties:
      - dimensions: 6 x 11
      - colors: [0, 8, 2, 7]
    description: The initial grid containing colored regions.
  - object: output_grid
    type: grid
    properties:
      - dimensions: 4 x 3
      - colors: [8, 0]
    description: The resulting grid, a sub-region of the input.
  - object: azure_region
    type: region
    properties:
      - color: 8
      - location: input_grid
    description: A contiguous block of azure pixels in the input.
  - object: red_region
      type: region
      properties:
        - color: 2
        - location: input_grid
        description: A contiguous block of red pixels in the input
  - object: orange_region
      type: region
      properties:
        -color: 7
        -location: input_grid
      description: A contiguous block of orange pixels in the input.
  - action: cropping
    agent: system
    input: input_grid
    output: output_grid
    description: Extracting a sub-region based on the azure (8) color.
```


**Natural Language Program:**

1.  **Identify the Target Object:** Locate the largest contiguous block of azure (8) colored pixels within the input grid.
2.  **Determine Bounding Box:** Find the bounding box coordinates (top-left and bottom-right) of that identified azure region.
3. **Extract the Subgrid:** Create the output grid by copying the input grid cell, from within the found bounding box.

In essence, the transformation isolates and extracts the largest azure object from the input grid.

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
