# be94b721 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 7 7 0
0 0 8 0 0 0 2 0 0 7 0
0 8 8 0 0 2 2 0 0 7 0
0 8 8 0 0 0 2 0 0 7 0
0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=704x384 at 0x7FC253D5CD50>

**output:**
```
8 8 8
0 8 0
8 8 0
8 8 0
```

<PIL.Image.Image image mode=RGB size=192x256 at 0x7FC253D5DDD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grid contains multiple colored objects (contiguous blocks of pixels with the same color), including azure (8), orange (7), and red (2). The output grid seems to be a subset of the input, focusing on a specific object and its surrounding context. The output grid contains the azure and white.

**YAML Block - Facts:**


```yaml
objects:
  - id: azure_object
    color: azure (8)
    shape: irregular, appears to be the primary focus
    position:
      input: spans rows 2-5 and columns 2-4
      output: spans all rows and columns 1-3

  - id: orange_object
    color: orange (7)
    shape: vertical line of length 3
    position:
      input: spans rows 2-4 and column 10
      output: not present

  - id: red_object
    color: red (2)
    shape: 2x2 square
    position:
      input: spans rows 3-4, and columns 6-7
      output: Not present
  - id: background
    color: white(0)
    shape: background, empty cells

actions:
  - type: selection
    description: Select the azure (8) object in the top-left.
  - type: crop/extraction
    description: Extract a subgrid containing only the selected object

relationships:
  - type: contains
    description: The input grid contains multiple objects of different colors.
  - type: focus
    description: The transformation focuses on the azure object.
  - type: adjacency
    description: The white is surrounding to the azure object, and maintained in the output.
```


**Natural Language Program:**

1.  **Identify the Target Object:** Locate the azure (8) colored object in the input grid.
2.  **Determine object boundary:** Get the x and y coordinates of the bounding box of the azure object.
3.  **Extract Subgrid:** Extract the subgrid containing the boundary of the azure object, including any adjacent white (0) pixels.
4. **Return Subgrid.** Return a subgrid of only the target and its surrounding.


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
