# d22278a0 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 3
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
8 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7FC253D5CC50>

**output:**
```
0 3 0 3 0 3 0 3 0 3 0 3
8 0 0 3 0 3 0 3 0 3 0 0
0 0 0 3 0 3 0 3 0 3 3 3
8 8 8 0 0 3 0 3 0 0 0 0
0 0 0 0 0 3 0 3 3 3 3 3
8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 3 3 3 3 3
8 8 8 8 8 0 8 0 0 0 0 0
0 0 0 0 8 0 8 0 0 3 3 3
8 8 8 0 8 0 8 0 8 0 0 0
0 0 8 0 8 0 8 0 8 0 0 3
8 0 8 0 8 0 8 0 8 0 8 0
```

<PIL.Image.Image image mode=RGB size=768x768 at 0x7FC253D5C2D0>
Okay, let's analyze this input-output pair.

**Perception of Elements:**

*   The input is a 12x12 grid, mostly filled with 0s (white). There's a single 3 (green) in the top right corner and an 8 (azure) in the bottom left corner.
*   The output is a 12x12 grid with a more complex arrangement of 0s (white), 3s (green), and 8s (azure). There's a noticeable checkerboard-like pattern, and areas where the colors appear to have spread or filled in.

**YAML Block (Facts):**


```yaml
facts:
  - object: grid
    properties:
      - dimensions: 12x12
      - cell_values: [0, 3, 8]
  - object: cell
    properties:
      - color:
        - 0: white
        - 3: green
        - 8: azure
  - observation: input_grid
    details: single green cell at top right, single azure cell at bottom left, rest are white.
  - observation: output_grid
    details: checkerboard pattern with green and white, azure fills from bottom left, interacts with checkerboard.
  - action: fill
    details: Colors seem to expand from their starting positions.
  - relationship: interaction
      object1: azure fill
      object2: green/white checkerboard
      details: Azure appears to override or be blocked by the checkerboard pattern.
```


**Natural Language Program:**

1.  **Create a Checkerboard:** Generate a checkerboard pattern on the 12x12 grid, alternating between 3 (green) and 0 (white) cells, starting with 3 (green) in the top left corner. A cell contains a 3, if the sum of its row and col is even, else it is 0.

2.  **Flood Fill Azure (8):** Starting from the initial 8 (azure) cell in the bottom left corner of the input, flood fill outwards. The flood fill should only replace 0 (white) cells. It is blocked by and therefore does not replace, the 3 (green) cells of the checkerboard. The fill extends diagonally.

In essence, a green/white checkerboard is created, and then an azure color starts spreading from the bottom-left, but it's constrained by the green cells of the checkerboard.

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
