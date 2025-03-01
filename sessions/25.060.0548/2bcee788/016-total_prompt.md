# 2bcee788 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 2 7 0 0 0 0 0
0 0 0 2 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B4BFE15CED0>

**output:**
```
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 7 7 3 3 3 3 3
3 3 7 7 7 7 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7B4C05B577D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves transforming a grid of numerical values (representing colors) into another grid of numerical values. The input grid contains a small cluster of non-zero values (2 and 7, representing red and orange) surrounded by zeros (white). The output grid replaces most of the zeros with 3s (green) and expands the cluster of 7s while eliminating the 2s.

**YAML Block - Facts:**


```yaml
objects:
  - name: background
    type: grid
    properties:
      initial_color: 0  # white
      final_color: 3    # green
  - name: cluster_1
    type: object
    properties:
      initial_colors: [2, 7] # red, orange
      final_color: 7   # orange
      shape: irregular, contiguous
      action: expand, replace
```


**Natural Language Program:**

1.  **Background Transformation:** Change all background pixels (value 0) in the input grid to the value 3 (green) in the output grid.

2.  **Object Identification and Expansion:** Identify the contiguous non-zero object (cluster of 2s and 7s) in the input.

3. **Color Replacement and Expansion:**
    *   Replace all pixels of value 2 (red) with 7.
    *   Expand every 7 one step right and up.

4.  **Final Output:** The output grid consists of the transformed background (all 3s) and the expanded/modified object (all 7s).

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
