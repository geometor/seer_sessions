# 941d9a10 • 010 • example_2 • investigate_coder

---

## train_2

**input:**
```
0 0 0 5 0 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 0
0 0 0 5 0 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B74CC50>

**output:**
```
1 1 1 5 0 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 2 2 2 2 5 0
0 0 0 5 2 2 2 2 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 0
5 5 5 5 5 5 5 5 5 5
0 0 0 5 0 0 0 0 5 3
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7F4C1B67DF50>
Okay, let's analyze this input-output pair to understand the transformation.

**Perception of Elements:**

*   **Input Grid:** A 10x10 grid with values primarily 0 (white) and 5 (gray). There's a repeating pattern of gray and white rows, and within those rows, a repeating pattern of gray and white pixels creating vertical stripes.
*   **Output Grid:** Also a 10x10 grid. It retains the gray (5) pixels from the input. However, some white (0) pixels are replaced:
    *   The top-left 3x1 block of white pixels becomes blue (1).
    *   A 4x2 central block of white pixels becomes red (2).
    *  A single, lower right white becomes green (3).

**YAML Facts:**


```yaml
facts:
  - object: input_grid
    type: grid
    size: 10x10
    elements:
      - color: white
        value: 0
      - color: gray
        value: 5
    pattern: alternating rows and columns of white and gray

  - object: output_grid
    type: grid
    size: 10x10
    elements:
      - color: white
        value: 0
      - color: gray
        value: 5
      - color: blue
        value: 1
      - color: red
        value: 2
      - color: green
        value: 3

  - action: replace_color
    input_color: white
    conditions:
        - location: top_left_corner, 3x1 block
          output_color: blue
        - location: two_center_rows, four_white_columns
          output_color: red
        - location: bottom_right_corner, one_white
          output_color: green
    default_output: no change
```


**Natural Language Program:**

1.  **Copy:** The gray (5) pixels from the input grid are directly copied to the output grid.
2. **Substitution at Top-Left Corner**: Detect if the current cell is part of a 3x1 block from the top-left corner within the input grid. If the current position contains white, replace it with blue (1) in the output.
3.  **Substitution in Center:** Detect if the current cell is part of rows 5 and 6. If so, find any group of four consecutive white pixels, and replace them with red pixels (2) in the output grid.
4.  **Substitution in Bottom Right**: Detect the bottom-right white. If it is white in the input, replace the white in the lower-right corner of the output grid with a green (3).
5. **Keep**: If a pixel does not meet the above conditions, maintain the original value from the input grid in the output grid.


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
