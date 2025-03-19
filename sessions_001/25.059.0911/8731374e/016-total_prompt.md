# 8731374e • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 7 9 8 8 0 8 9 9 3 1 4 5 2 7 6
6 0 9 2 7 2 8 4 3 3 2 7 7 5 9 4 0
1 9 4 5 4 8 8 8 8 8 8 8 8 2 0 7 9
5 5 6 8 3 8 8 8 8 8 8 8 8 2 0 2 7
8 2 3 2 9 8 8 8 8 8 8 8 8 0 7 6 4
1 7 3 3 5 8 8 8 2 8 8 8 8 7 1 1 4
7 2 3 5 6 8 8 8 8 8 8 8 8 5 8 5 6
5 2 7 3 5 8 8 8 8 8 8 8 8 1 4 4 6
1 4 0 0 9 9 4 0 2 6 5 5 0 8 6 4 7
8 7 8 3 3 8 0 9 0 4 8 9 8 5 2 7 3
2 0 2 8 2 0 8 4 4 3 2 6 8 7 4 7 2
2 7 8 3 7 4 2 4 8 4 2 3 9 9 2 0 8
4 8 8 5 3 2 0 1 8 9 3 9 8 1 8 8 7
3 9 9 9 1 6 1 9 4 7 5 5 3 2 9 3 0
5 8 2 5 4 2 2 4 0 9 2 8 1 3 5 7 3
8 0 9 5 3 8 4 5 0 2 5 2 9 6 0 1 0
```

<PIL.Image.Image image mode=RGB size=1088x1024 at 0x7D67CBE7A0D0>

**output:**
```
8 8 8 2 8 8 8 8
8 8 8 2 8 8 8 8
8 8 8 2 8 8 8 8
2 2 2 2 2 2 2 2
8 8 8 2 8 8 8 8
8 8 8 2 8 8 8 8
```

<PIL.Image.Image image mode=RGB size=512x384 at 0x7D67CBE7A6D0>
Okay, here's my analysis of the provided input-output example pair.

**Perception of Elements:**

The input is a large, multi-colored grid. The output is a smaller grid composed of only two colors (azure and red) from the input grid. The output appears to extract a specific pattern, a cross shape, from the input. The dominant color in the large input grid is azure (8). The red (2) forms a plus sign (+) or cross in the output.

**YAML Block (Facts):**


```yaml
task_description: |
  Extract a cross-shaped subgrid from a larger input grid.
objects:
  - name: input_grid
    type: 2D array
    properties:
      - colors: Multiple (0-9)
      - size: Large (16x17)
  - name: output_grid
    type: 2D array
    properties:
      - colors: [azure, red] # 8, 2
      - size: Smaller (6x8)
      - shape: cross
  - name: cross_pattern
    type: shape
    properties:
       - color: red
       - structure: vertical and horizontal lines intersecting at the center
actions:
  - type: extraction
    description: Isolate the cross pattern and its surrounding azure background.
relationships:
  - type: spatial
    description: The output grid's cross is centered and derived from a similar, less defined shape existing at the center area of input_grid
```


**Natural Language Program:**

1.  **Identify the dominant color:** Find the most frequent color in the input grid. In this case, it's azure (8).
2.  **Locate the Cross:** Examine the input grid and search for a cross or plus-shaped structure of same color, not the dominant one. This different color must have continuous horizontal and vertical lines, with same number of this color pixels at both sides.
3.  **Determine Output Grid Size:** The output is smaller than the input. The size is defined by the horizontal and vertical extent of the non-dominant color forming cross, plus additional rows/columns of dominant color from input
4.  **Extract:** Create the output grid by copying the identified cross pattern and the surrounding dominant-color background based on determined output size.
5. The cross pattern has one azure(8) surrounding row in up and down, and has two azure(8) surrounding columns at left and right.


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
