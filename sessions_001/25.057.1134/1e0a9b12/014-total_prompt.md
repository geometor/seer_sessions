# 1e0a9b12 • 014 • example_3 • investigate_coder

---

## Example 3

**input:**
```
0 0 0 1 0
0 3 0 0 0
0 3 0 1 2
6 0 0 0 0
0 3 0 0 0
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x74AF1C9C6FD0>

**output:**
```
0 0 0 0 0
0 0 0 0 0
0 3 0 0 0
0 3 0 1 0
6 3 0 1 2
```

<PIL.Image.Image image mode=RGB size=320x320 at 0x74AF1CB832D0>
Okay, here's my analysis of the provided example, focusing on perception, structured documentation, and a natural language program describing the transformation.

**Perception of Elements:**

The task involves a grid of colored pixels.  The colors change from input to output, and some colors are not present in both. The shape and size of the grid is consistent. There appears to be a relationship between spatially adjacent, non-zero pixels. The key seems to be the movement, addition, and modification of colored pixels.

**YAML Documentation of Facts:**


```yaml
facts:
  - type: grid
    description: 2D array of pixels
    properties:
      - width: 5
      - height: 5
  - object: pixels
    description: Individual cells within the grid
    properties:
      - color: integer value (0-9) representing a color
      - position: (row, column) coordinates
  - observation: color_change
    description: Some pixel colors change between input and output.
    details: >
      Pixels that are non-zero, and are adjacent to another non-zero pixel seem to be "shifted" or have their color combined with adjacent non-zero pixels
      in the order Blue, Red, Green, then Magenta, at the bottom of the grid.
  - observation: spatial_relationship
    description:  Non-zero pixels move down.
  - observation: color_priority
    description: There appears to be a priority between color when they combine in the output, Blue > Red > Green > Magenta.
```


**Natural Language Program:**

1.  **Identify Non-Zero Clusters:** Find all clusters of adjacent, non-zero pixels. A cluster is defined as one or more non-zero pixels that are directly adjacent (not diagonally) to each other in the input grid.
2. **Shift Down:** Move clusters of adjacent, non-zero, pixels down in the grid, 1 row at time.
3. **Consolidate:** Merge moved pixels to the end of the non-zero, adjacent pixels.
4. **Fill with Zeroes**: All other pixels in the grid are zero (white).


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
