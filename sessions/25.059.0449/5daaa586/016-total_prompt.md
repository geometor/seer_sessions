# 5daaa586 • 016 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 4 3 0 0 0 4 0 0 0 4 0 0 0
0 0 0 3 0 4 0 0 0 0 0 4 0 0 0
0 0 0 3 0 0 4 0 0 0 0 4 0 0 0
0 0 0 3 0 4 0 0 0 0 0 4 0 0 0
0 0 0 3 0 0 0 0 0 0 4 4 4 0 4
2 2 2 3 2 2 2 2 2 2 2 4 2 2 2
4 0 0 3 4 4 0 4 0 0 0 4 0 0 0
0 0 0 3 0 0 0 0 0 0 0 4 0 0 0
4 0 0 3 0 0 0 0 4 0 4 4 0 0 0
4 0 0 3 0 0 4 0 0 0 4 4 0 0 0
8 8 8 3 8 8 8 8 8 8 8 4 8 8 8
0 0 0 3 0 0 0 0 0 0 4 4 0 0 4
0 0 0 3 4 0 0 4 0 0 0 4 0 0 0
0 0 4 3 0 0 0 0 0 4 0 4 0 0 0
```

<PIL.Image.Image image mode=RGB size=960x896 at 0x744068E60F50>

**output:**
```
3 2 2 2 2 2 2 2 4
3 4 4 4 4 4 4 4 4
3 0 0 0 0 0 0 0 4
3 0 0 0 0 4 4 4 4
3 0 0 4 4 4 4 4 4
3 8 8 8 8 8 8 8 4
```

<PIL.Image.Image image mode=RGB size=576x384 at 0x744068E47950>
Okay, let's analyze this input-output example.

**Perception of Elements:**

The input is a large, complex grid with various colors (represented by digits 0-9). The output is a smaller, simpler grid, also with colors. It seems like the output is a condensed or summarized version of the input. The vertical green line in the input (column of 3's) seems to be preserved as the leftmost column in the output. Horizontal lines of same-colored pixels crossing the green vertical line in the input, seem to be summarized in the output.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - colors: [0, 2, 3, 4, 8]
      - dimensions: [14, 15]
      - features:
          - vertical_line:
              color: 3
              position: column 4
          - horizontal_lines:
              - color: 2
                row: 6
              - color: 4
                row: 7
              - color: 8
                row: 11

  - name: output_grid
    type: grid
    properties:
      - colors: [2, 3, 4, 0, 8]
      - dimensions: [6, 9]

relationships:
  - type: summary
    from: input_grid
    to: output_grid
    details: "The output grid seems to represent a condensed version of the input, focusing on horizontal lines that cross a prominent vertical green line in the input."

actions:
    - action: select
      description: "Select row from input that crosses column with value equal 3"
    - action: evaluate
      description: "The selected rows from the input are simplified/reduced in the output."
```


**Natural Language Program:**

1.  **Identify Key Structure:** Find the vertical line of color 'green' (value 3) in the input grid. This is in column 4.
2.  **Select Rows:** Extract all the rows from the input grid that cross, contains pixels to the left and to the right, the veritical line of green.
3.  **Simplify Rows:** For each selected row, create a new, shorter row in the output.
4. **Preserve the first element:** The simplified row begins with the value 3, (the vertical green line), the first value of each simplified row.
5.  **Condense stretches:** All values to the right of the vertical line are condensed such
    that stretches of a single color are reduced to one pixel of that color
    in the order they appear.


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
