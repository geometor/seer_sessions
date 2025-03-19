# a740d043 • 008 • example_2 • investigate_coder

---

## Example 2

**input:**
```
1 1 1 1 1 1 1
1 1 3 1 2 1 1
1 1 3 1 2 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
1 1 1 1 1 1 1
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x74AF1CC7D8D0>

**output:**
```
3 0 2
3 0 2
```

<PIL.Image.Image image mode=RGB size=192x128 at 0x74AF1CC2F850>
Okay, here's my analysis of the example input-output pair:

**Perception of Elements:**

*   The input is a 7x7 grid. Most cells are blue (value 1). There are two green (value 3) cells and two red (value 2) cells in specific locations.
*   The output is a 2x3 grid. It contains only the green (3), white/background (0), and red (2) colors, arranged in the same relative positions as they appear within the clusters in the input.

**YAML Block (Facts):**


```yaml
facts:
  - input_grid_size: 7x7
  - output_grid_size: 2x3
  - input_colors:
      - blue: 1
      - green: 3
      - red: 2
  - output_colors:
      - green: 3
      - white: 0
      - red: 2
  - object_1:
      type: cluster
      color_1: green
      color_2: red
      relative_position: color_1 is left of color_2
      instance_count: 2
  - background_color:
    input: 1
    output: 0

```


**Natural Language Program:**

1.  Identify the two clusters of non-blue pixels. In this case Green(3) and Red(2), they are in a cluster together, sharing a border, and repeated twice
2.  Extract each cluster separately. These can be treated as two separate objects.
3.  Represent the object to a new output grid.
4. Change the background color from blue (1) to white(0).
5.  Preserve the relative positions of the colored pixels from input object to output object.


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
