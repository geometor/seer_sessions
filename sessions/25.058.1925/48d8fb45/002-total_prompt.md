# 48d8fb45 • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1
0 0 0 5 0 0 0 1 1 0
0 0 0 1 0 0 0 0 1 0
0 0 1 1 1 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 1 1 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F264D050>

**output:**
```
0 1 0
1 1 1
0 1 1
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x78E5F21D3BD0>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 4 4 0 0
0 0 4 0 0 0 0 0 4 0
0 4 0 4 0 0 0 4 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F21D3CD0>

**output:**
```
4 4 0
0 0 4
0 4 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x78E5F21D3C50>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 5 0 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x78E5F21D01D0>

**output:**
```
0 2 2
2 2 0
0 2 0
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x78E5F21D39D0>
<PIL.Image.Image image mode=RGB size=2000x882 at 0x78E5F2070FD0>Okay, let's analyze the provided examples to understand the transformation.

**Perception of the Elements:**

The task involves transforming a larger grid (input) into a smaller grid (output). The input grids contain various colored pixels (represented by numbers 0-9), with white (0) being the most prevalent, acting likely as a background. The output grids seem to be a condensed representation, focusing on specific colored objects within the input, while ignoring the white background and the grey (5) pixels. It appears that a non-white, non-grey object is extracted. It seems like only one colored shape/object besides 0 and 5 is extracted. There may be more than one distinct object of the same color.

**YAML Block Documenting Facts:**


```yaml
facts:
  - observation: Input grids are larger than output grids.
  - observation: Input grids contain pixels of various colors (0-9).
  - observation: Output grids are smaller and contain a subset of colors from the input, excluding 0 (white) and 5 (grey).
  - observation: Output grids seem to represent a single colored "object" extracted from the input.
  - observation: An "object" is defined by a group of contiguous pixels of the same color, excluding 0 and 5.
  - object: Input Grid
    properties:
      - size: variable, 10x10 in examples
      - colors: 0-9
  - object: Output Grid
    properties:
      - size: variable, 3x3 in examples
      - colors: subset of input grid colors, excluding 0 and 5
  - action: Extraction
    description: A specific non-white, non-grey object is extracted from the input grid.
  - relationship: Input grid is transformed into output grid by object extraction.
```


**Natural Language Program:**

1.  **Identify Objects:** Scan the input grid to identify contiguous blocks of pixels of the same color, excluding color 0 (white) and color 5 (grey).
2.  **Select Target Object:** Choose the object that is not white(0) or grey(5).
3. **Extract Bounding Box:** Determine the minimum bounding box for the target shape, encompassing all pixels of that object's color, while maintaining the input spatial arrangement.
4.  **Generate Output:** Create a new grid containing only the selected object's pixels within the bounding box area. All other pixels outside this region or pixels which are 0 or 5, should be color 0. The arrangement and positions of colors extracted in the bounding box should be same as in input grid.


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
