# 31aa019c • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
6 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 2 8
0 7 0 0 2 0 5 0 2 0
0 9 0 1 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 1
0 0 0 0 0 6 0 0 0 0
0 1 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 5 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36045DF1D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 3 2 0 0
0 0 0 0 0 2 2 2 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C3604476250>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input is a 10x10 grid with single-digit integers (0-9) representing different colors.
*   The output is also a 10x10 grid, but most of the grid is filled with 0s. A 3x3 block of non-zero numbers exists at the bottom right of non-zero values from the input grid..
*   The non-zero values in output seems to be related to a cluster of values in the input.

**YAML Block (Facts):**


```yaml
facts:
  - type: grid
    description: Input grid
    dimensions: [10, 10]
    elements: integers (0-9)

  - type: grid
    description: Output grid
    dimensions: [10, 10]
    elements: integers (0-9)

  - type: object
    description: cluster of non-zero pixels in input
    properties:
        - colors: mixed (1,2,3,5,6,7,8,9)

  - type: object
    description: 3x3 block in output
    properties:
      - colors: [2,3]
      - shape: square
    location: bottom-right of area of interest
  - type: action
    description: locate area of interest
    details: find area with at least one non-zero pixels in any surrounding eight neighbor.

  - type: action
    description: transformation
    details: select a 3x3 subgrid from the bottom right of the located region, if found.

  - type: relationship
    description: Input cluster to output block
    details: The output 3x3 block replaces a part of the input; its positioning corresponds to the bottom-right part of the original area in the input.
```


**Natural Language Program:**

1.  **Identify the Area of Interest:** Scan the input grid. The area of interest are all pixels that are non-zero and have at least one neighbor (up, down, left, right, or diagonal) that is non-zero.
2.  **Locate Subgrid:** If an area of interest is found, identify the bottom-right-most pixel, and define the 3x3 region in the output grid at that bottom right corner of the area of interest.
3. **Fill Output:** If no region is found, the output is all zeros. If it exists:
    fill the region with color '2' except for the central pixel which is '3'.
4.  **Other Pixels:** All other pixels in the output grid are set to 0.


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
