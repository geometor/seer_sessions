# 3de23699 • 002 • example_4 • investigate_coder

---

## train_1

**input:**
```
0 0 0 0 0 0 0
0 4 0 0 0 4 0
0 0 0 2 0 0 0
0 0 2 2 2 0 0
0 0 0 2 2 0 0
0 4 0 0 0 4 0
0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=448x448 at 0x7B4BFDB42850>

**output:**
```
0 4 0
4 4 4
0 4 4
```

<PIL.Image.Image image mode=RGB size=192x192 at 0x7B4BFDB42050>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 3 0
0 0 0 2 2 0 0 0 0
0 0 0 2 2 0 2 0 0
0 0 2 0 0 2 0 0 0
0 3 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=576x768 at 0x7B4BFDB42B50>

**output:**
```
0 3 3 0 0
0 3 3 0 3
3 0 0 3 0
```

<PIL.Image.Image image mode=RGB size=320x192 at 0x7B4BFDB42BD0>

## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=896x768 at 0x7B4BFDB426D0>

**output:**
```
0 6 0 0
0 6 0 0
6 6 6 0
0 6 6 0
```

<PIL.Image.Image image mode=RGB size=256x256 at 0x7B4BFDB425D0>

## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 4 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=1152x768 at 0x7B4BFDB421D0>

**output:**
```
0 0 0 8 8 0 0 0
0 0 8 8 0 0 0 0
0 0 0 0 0 0 8 0
0 0 0 0 8 0 8 0
```

<PIL.Image.Image image mode=RGB size=512x256 at 0x7B4BFDB42450>
<PIL.Image.Image image mode=RGB size=3232x1104 at 0x7B4BFE15DE50>Okay, let's analyze the provided input-output pairs to understand the transformation rule.

**Perception of Elements:**

The task involves 2D grids of different sizes containing single-digit integers (0-9), representing different colors. The transformation seems to focus on specific colors within each input grid, extracting and rearranging them to form the output grid. It appears the transformation is not about rotating or simply cropping a region. The output grid is always smaller than the input, and contains some selected, duplicated, and/or rearranged pixels. The selection seems related to identifying specific non-zero colored pixels and their relative positions. In particular there are two colors in each example. The output consists of just one of those colors and they are duplicated

**YAML Block (Facts):**


```yaml
facts:
  - observation: |
      Input grids are of varying dimensions, and always larger than their corresponding output grid.
  - observation: |
      Each cell in the grid contains a single-digit integer representing a color.
  - observation: |
     Each input grid usually features 2 distinct non-zero colors
  - observation: |
      The output grids contain only one of the non-zero colors from the input grid.
  - observation: |
     The pixels of the selected color in the output are duplicated.
  - observation: |
      Zero-valued pixels (white) appear to act as background and are not generally present in output, unless needed to achieve a shape/size
  - observation: |
    The relative position of the selected pixels in the output corresponds to the selected shape pixels in the input.

```


**Natural Language Program:**

1.  **Identify Target Colors:** For each input grid, identify the two non-zero colors that are present.
2.  **Select Output Color:** Determine which of these colors is the "target" color for the output. From the examples it looks like this is the first occurring non-zero pixel (reading left-to-right, top-to-bottom).
3. **Locate instances:** Find all instances of the target color
4.  **Duplicate:** For each pixel in the found target color locations, duplicate it in a 2x2 shape.
5. **construct a map:** using all the instances of the other color, construct a mask for the output grid that maps all the locations of that color to where the target pixels should appear in the output.
6.  **Create Output Grid:** Create a new grid, and place the 2x2 shapes based on the mask.


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
