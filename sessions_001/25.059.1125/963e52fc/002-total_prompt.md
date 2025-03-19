# 963e52fc • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0
2 8 2 8 2 8
2 8 2 8 2 8
0 0 0 0 0 0
0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=384x320 at 0x7F4C1B703550>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 8 2 8 2 8 2 8 2 8 2 8
2 8 2 8 2 8 2 8 2 8 2 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=768x320 at 0x7F4C1B700250>

## train_2

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
2 3 3 2 3 3 2
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x320 at 0x7F4C1B701E50>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 3 3 2 3 3 2 3 3 2 3 3 2 3
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=896x320 at 0x7F4C1A58B150>

## train_3

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
1 2 2 1 2 2 1 2
2 1 2 2 1 2 2 1
0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=512x320 at 0x7F4C1A5893D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 2 2 1 2 2 1 2 2 1 2 2 1 2 2 1
2 1 2 2 1 2 2 1 2 2 1 2 2 1 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x320 at 0x7F4C1A58AC50>
<PIL.Image.Image image mode=RGB size=2816x720 at 0x7F4C1B75DC50>Okay, here's my analysis of the provided input-output examples, focusing on perception, object identification, and the transformation rule.

**Perception of Elements:**

The core elements are grids containing single-digit integers (0-9), representing different colors. The most prominent feature is a horizontal band of non-zero values within each input grid. This band appears to be the primary focus of the transformation. The output grids have a width that always seems to be double +2, the length of the colored band in the input.

**YAML Fact Documentation:**


```yaml
facts:
  - object: input_grid
    properties:
      - type: 2D array
      - values: integers (0-9)
      - feature: horizontal_band
        description: A contiguous sequence of non-zero values in a single row.
        properties:
          - start_column: index of the first non-zero value
          - end_column: index of the last non-zero value
          - length: number of non-zero value pixels (end_column - start_column + 1)
          - row_index: the row containing the band
  - object: output_grid
    properties:
      - type: 2D array
      - values: integers (0-9)
      - width: 2 * input_band_length + 2
      - feature: mirrored horizontal band.
        description: The input band sequence of colors is duplicated.
  - transformation:
      - description: The input grid's horizontal band is extended by doubling it's width and adding a padding of 0 at the beginning and at the end.
```


**Natural Language Program:**

1.  **Identify the Horizontal Band:** Locate the single row within the input grid that contains a contiguous sequence of non-zero values. Determine the starting column index, ending column index, and the length of this band.
2.  **Calculate new width:** double the length of the horizontal band, adding 2.
3.  **Create the extended output band:** Create a sequence of pixel matching the input band doubled in size.
4.  **Populate the output grid:** use the output sequence as the central band from the input grid, using the same row index. All other values on the grid are 0.


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
