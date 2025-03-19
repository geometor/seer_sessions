# 91714a58 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
3 0 0 0 0 0 6 2 0 0 0 5 0 0 0 3
0 7 0 0 0 0 9 0 0 0 0 0 0 0 5 0
0 0 0 0 0 8 8 0 7 7 7 0 0 0 0 4
0 2 0 0 0 0 0 0 7 7 7 0 2 0 5 0
0 8 0 0 9 6 1 7 7 7 7 0 0 0 0 0
5 0 0 0 0 3 6 0 6 0 0 3 3 0 0 0
0 4 0 2 0 0 0 0 0 0 0 0 0 0 4 0
9 0 0 0 0 0 0 0 0 3 0 8 0 0 0 0
0 0 3 0 0 0 0 6 0 9 0 0 0 0 0 0
9 0 0 0 1 0 0 3 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 3 3 0 0 7 0
0 0 0 0 0 0 0 4 0 0 0 0 0 5 0 0
4 0 0 1 7 0 3 0 0 7 5 0 0 0 0 0
0 0 0 0 0 1 7 2 0 0 5 0 0 1 0 4
0 0 0 0 0 0 0 3 0 0 2 0 0 0 0 0
0 2 0 0 0 7 9 0 0 0 5 0 2 0 3 0
```

<PIL.Image.Image image mode=RGB size=1024x1024 at 0x7F2DF795C7D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x1024 at 0x7F2DF67FDA50>
Okay, I'm ready to analyze this input-output pair and determine the transformation rule. Here's my breakdown:

**Perception of Elements:**

*   The input is a grid with various single-digit numbers (0-9), representing different colors.
*   The output is a grid of the same dimensions, but it appears to be mostly empty (filled with 0s) except for a concentrated area of 7s.
*   The 7s in the output seem to correspond to a cluster of 7s in the input, although other instances of '7' are in the input and do not appear in the output. It appears the largest cluster of '7' is preserved.

**YAML Block (Facts):**


```yaml
objects:
  - id: input_grid
    type: grid
    description: Contains various colors represented by digits 0-9.
  - id: output_grid
    type: grid
    description: Contains mostly 0s, with a single cluster of 7s.
  - id: color_7_cluster
    type: object
    description: A contiguous block of 7s in the input grid.
    properties:
      - color: orange (represented by 7)
      - shape: irregular

actions:
  - name: identify_largest_cluster
    agent: SEER
    input: input_grid
    parameters:
      target_color: 7
    description: Find the largest contiguous cluster of the target color.
  - name: clear_grid
    agent: SEER
    input: input_grid
    output: output_grid
    description: Set all cells in the grid to 0.
  - name: reconstruct_cluster
    agent: SEER
    input: output_grid, color_7_cluster
    description: Recreate the largest identified cluster in the cleared output grid.

relationships:
  - subject: output_grid
    predicate: contains
    object: color_7_cluster
  - subject: color_7_cluster
    predicate: derived_from
    object: input_grid
```


**Natural Language Program:**

1.  **Initialization:** Start with the given input grid.
2.  **Identify Target:** The target color is orange (represented by the digit 7).
3.  **Find Largest Cluster:** Scan the input grid to identify the largest contiguous cluster of pixels with the value 7. Contiguous means pixels are adjacent horizontally or vertically. Diagonal adjacency doesn't seem to contribute.
4.  **Clear Output:** Create an output grid of the same dimensions as the input grid, initialized with all cells set to 0 (white).
5.  **Reconstruct:** Copy the largest cluster of 7s found in step 3 to the output grid, maintaining its original shape and relative position.
6. **Ignore other 7s**: All other 7s which are not part of the largest cluster are ignored (replaced with 0).
7. **Final Output:** All other colored pixels in the input grid are set to 0 in the output grid, the identified cluster will be the only non zero area.

Essentially, the transformation finds the largest connected "island" of 7s in the input and reproduces *only* that island in the output, setting everything else to 0.

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
