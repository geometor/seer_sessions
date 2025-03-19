# 00d62c1b • 004 • example_1 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0
0 0 3 0 0 0
0 3 0 3 0 0
0 0 3 0 3 0
0 0 0 3 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7FC253D4F950>

**output:**
```
0 0 0 0 0 0
0 0 3 0 0 0
0 3 4 3 0 0
0 0 3 4 3 0
0 0 0 3 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x384 at 0x7FC253D4EFD0>
Okay, here's my analysis of the provided input-output example:

**Perception of Task Elements:**

The task involves a 2D grid (matrix) of single-digit integers, representing colors. The primary change observed is the introduction of the number '4' (yellow) within the existing pattern of '3' (green) pixels.  The '4's appear to be inserted between adjacent '3's, specifically in a horizontal or vertical direction (not diagonal). The surrounding '0' (white) pixels remain unchanged. The overall grid dimensions remain constant.

**YAML Fact Block:**


```yaml
facts:
  - object: grid
    type: 2D array
    elements: integers (0-9)
    size_consistency: input_size == output_size

  - object: pixel
    type: grid_cell
    values:
      0: white
      3: green
      4: yellow

  - observation: yellow_insertion
    description: "Yellow (4) pixels are inserted between adjacent green (3) pixels."
    adjacency_type: horizontal_or_vertical
    
  - relation: adjacency
    parameters:
        type: cell
        value: [3,3]
    result:
        type: cell
        value: 4

```


**Natural Language Program:**

1.  **Identify** all green (3) pixels within the input grid.
2.  **Check** for horizontal and vertical adjacency between green pixels.
3.  **Insert** a yellow (4) pixel in the output grid between any two adjacent green pixels.
4. **Copy** all white pixels as they are
5.  **Maintain** the original grid dimensions and all other pixel values unchanged.

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
