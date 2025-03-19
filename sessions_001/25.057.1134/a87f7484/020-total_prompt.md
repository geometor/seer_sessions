# a87f7484 • 020 • example_4 • investigate_coder

---

## Example 4

**input:**
```
0 7 7
7 7 0
7 0 7
3 0 0
0 3 3
3 0 0
2 0 0
0 2 2
2 0 0
8 0 0
0 8 8
8 0 0
```

<PIL.Image.Image image mode=RGB size=192x768 at 0x74AF1CE007D0>

**output:**
```
0 7 7
7 7 0
7 0 7
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x74AF1C9C6AD0>
Okay, here's my analysis of the example input-output pair, structured as a report:

**Perception of Elements:**

The task involves a grid of colored pixels. The input grid appears to be larger and contains multiple distinct colored regions (objects). The output grid is smaller and seems to correspond to a specific section of the input grid. The transformation involves identifying a sub-grid within the input. The non-zero values are all along the perimeter of the output.

**YAML Fact Block:**


```yaml
facts:
  - object: input_grid
    type: 2D array
    properties:
      - height: 12
      - width: 3
      - values: [0, 2, 3, 7, 8]
  - object: output_grid
    type: 2D array
    properties:
      - height: 3
      - width: 3
      - values: [0, 7]
  - observation: output_grid is a subregion of input_grid
  - observation: output grid contains top left corner object.
  - observation: the output grid is the smallest possible square

```


**Natural Language Program:**

1.  **Identify the Target Object:** Locate the object formed by contiguous non-zero pixels in the top-left corner of the input grid.
2.  **Determine Sub-grid Boundaries:** find the smallest bounding box to contain this object.
3.  **Extract Sub-grid:** Extract the region defined by the bounding box.
4.  **Output:** The extracted sub-grid is the output.

In simpler terms, the program finds the smallest top-left object and extracts it.

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
