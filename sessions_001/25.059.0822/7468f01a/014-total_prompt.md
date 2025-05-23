# 7468f01a • 014 • example_3 • investigate_coder

---

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 3 6 6 0 0 0 0 0 0 0 0 0
0 0 6 3 3 3 6 6 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 3 6 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 3 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1088x960 at 0x70A2EC7D4350>

**output:**
```
6 6 3 6 6 6
6 6 3 3 3 6
6 3 6 6 6 6
6 3 6 6 6 6
```

<PIL.Image.Image image mode=RGB size=384x256 at 0x70A2EC74E6D0>
Okay, here's my analysis of the provided input-output example:

**Perception of Elements:**

The task involves extracting a specific colored region from a larger grid. The input grid is mostly empty (filled with 0s, representing white). There's a noticeable rectangular block composed of magenta (6) and green (3) pixels. The output grid appears to be a cropped version of the input, containing *only* that colored rectangle, with the whitespace removed. The rectangle in the input is not a solid color. The spatial arrangement of the colors within the rectangle in the input is preserved in the output.

**YAML Block (Facts):**


```yaml
task_description:
  task_type: object_extraction
  objects:
    - name: background
      color: white (0)
      role: filler
    - name: rectangle
      properties:
        - shape: rectangle
        - colors: [magenta (6), green (3)]
      actions:
        - extracted
  relationships:
    - type: spatial
      description: The 'rectangle' is embedded within the 'background'.
    - type: transformation
      description: The output is a cropped version of the input, containing only the 'rectangle'.
      details: "whitespace is removed"

```


**Natural Language Program:**

1.  **Identify the colored region:** Locate the smallest rectangular area within the input grid that encompasses all non-white (non-zero) pixels.
2.  **Extract the region:** Create a new grid containing only the pixels within the identified rectangular area.
3.  **Preserve internal structure**: Make sure the relative positions of different colors inside are kept identical.

In essence, the transformation rule is to "crop the input grid to the bounding box of the non-white pixels, retaining the internal colored structure".

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
