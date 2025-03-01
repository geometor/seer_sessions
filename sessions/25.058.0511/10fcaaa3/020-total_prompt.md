# 10fcaaa3 • 020 • example_4 • investigate_coder

---

## Example 4

**input:**
```
0 0 0 0
0 2 0 0
0 0 0 0
0 0 0 0
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7B1DDE487A50>

**output:**
```
8 0 8 0 8 0 8 0
0 2 0 0 0 2 0 0
8 0 8 0 8 0 8 0
0 0 0 0 0 0 0 0
8 0 8 0 8 0 8 0
0 2 0 0 0 2 0 0
8 0 8 0 8 0 8 0
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x512 at 0x7B1DDE486150>
Okay, here's a breakdown of my observations, documented facts, and a natural language program describing the transformation:

**Perception:**

The core transformation seems to involve replicating the single red (value 2) object within the input grid and adding a new azure (value 8) border/alternating frame around each replica of the object. The input grid is 4x4, while the output grid expands to 8x8. It seems the object is replicated downwards, and then the replications are all surrounded by the azure, creating alternating rows.

**YAML Fact Documentation:**


```yaml
facts:
  - observation: |
      The input grid contains a single object of interest: a red pixel (value 2).
  - object: red_pixel
    value: 2
    initial_position: (1, 1) # (row, col) - zero-indexed
    properties:
      - color: red
  - object: background
    value: 0
    properties:
      - color: white
  - object: frame_pixel
    value: 8
    properties:
      - color: azure
  - action: replication
    description: The red pixel is replicated.
  - action: framing
    description: Azure pixels are added in alternating fashion to create horizontal dividers.
  - input_grid_size:
    rows: 4
    cols: 4
  - output_grid_size:
    rows: 8
    cols: 8
  - relationship: |
      The output grid is double the dimensions of the input grid.
  - relationship: frame rows have alternating azure and white
```


**Natural Language Program:**

1.  **Identify the object of interest:** Locate the single red pixel (value 2) within the input grid.
2.  **Replicate Vertically:** create a copy of the row containing the red pixel. The number of final replicated rows containing the red pixel should be equal to the heigh of the input.
3.  **Create frame rows:** for every replicated row, add a row above, with alternating azure and white pixels
4. **Assemble Output Grid:** Combine the replicated object, with frame rows, and empty rows to create output with twice the input grid dimensions. Ensure that replicated rows and empty rows alternate, starting from the top. Ensure there is a frame row between each set of replications.


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
