# 7e0986d6 • 002 • example_2 • investigate_coder

---

## train_1

**input:**
```
8 0 0 0 8 0 3 3 3 3 3 8 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 8 3 8 0 0 0
0 0 3 3 3 0 3 3 3 3 3 0 0 0
0 0 3 3 3 0 3 8 3 3 3 0 0 0
0 0 3 3 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 8 0 3 3 3 8 3 0 3 3 3 8 3
0 0 0 3 8 3 3 3 0 3 3 3 3 3
0 0 0 3 3 3 3 3 0 3 3 3 3 3
3 3 3 3 8 3 3 3 8 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0 0 0 0
3 8 3 0 8 0 0 0 0 0 0 0 0 8
```

<PIL.Image.Image image mode=RGB size=896x832 at 0x741F72B1A670>

**output:**
```
0 0 0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 3 3 3 3 3 0 0 0
0 0 3 3 3 0 3 3 3 3 3 0 0 0
0 0 3 3 3 0 3 3 3 3 3 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3
0 0 0 3 3 3 3 3 0 3 3 3 3 3
0 0 0 3 3 3 3 3 0 3 3 3 3 3
0 0 0 3 3 3 3 3 0 3 3 3 3 3
3 3 3 3 3 3 3 3 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0 0 0 0
3 3 3 0 0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=896x832 at 0x741F72B1A850>

## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 1 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 2 1 2 2 2 2 2
0 2 2 1 2 0 0 0 0 2 2 2 2 2 2 2
0 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2
0 2 2 2 2 1 0 0 0 2 2 2 2 2 1 2
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0
0 1 0 2 2 2 2 2 2 1 2 2 2 0 0 0
0 0 0 1 2 2 2 2 2 2 2 2 2 0 0 1
0 0 0 2 2 2 2 2 2 1 2 2 1 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x832 at 0x741F72B1A8F0>

**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2
0 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2
0 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2
0 2 2 2 2 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 0 0 0
```

<PIL.Image.Image image mode=RGB size=1024x832 at 0x741F72B1B750>
<PIL.Image.Image image mode=RGB size=1980x1714 at 0x741F72B8FBB0>Okay, here's a breakdown of my observations, documented facts, and a natural language program describing the transformation:

**Perception of Elements:**

The primary elements appear to be colored pixels within a grid. The transformation seems to involve selectively removing certain colors based on their surroundings or overall pattern. The key seems to be identifying and removing specific colors, while leaving others untouched. The transformation is not a simple global color swap, but is context-dependent. In particular non-zero colors that do not touch any zero values, are removed.

**YAML Fact Documentation:**


```yaml
facts:
  - type: grid
    description: Input and output are grids of colored pixels.
  - type: colors
    values: [0, 1, 2, 3, 8] # white, blue, red, green, azure
    description: Pixels have colors represented by integer values.
  - type: transformation_type
    description: Selective color removal.
  - type: preservation_rule
    description: Colors touching at least one 0 (white) are preserved; otherwise removed.
  - type: removal_rule
    description: Colors not directly adjacent to 0 (white), are changed to 0.
  - type: adjacency
    description: Orthogonal (up, down, left, right). Diagonal adjacency doesn't affect the rule.
```


**Natural Language Program:**

1.  **Iterate** through each pixel in the input grid.
2.  **Check** the color of the current pixel.
3.  **If** the pixel's color is 0 (white) move on to the next pixel.
4.  **If** the pixel's color is not 0, examine the colors of its four immediate neighbors (up, down, left, and right). Do not check for diagonal neighbors.
5. **If** any of the neighbors are colour 0, do not change it.
6. **Else If** none of the neighbors are colors 0, then change the pixel value/color to 0 in the output grid.
7.  **Repeat** for all pixels in the grid.

In simpler terms, we keep the pixels of colors that *touch* white, while removing colors that do not touch the white background somewhere on their edge.

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
