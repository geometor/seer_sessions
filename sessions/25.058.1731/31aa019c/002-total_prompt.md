# 31aa019c • 002 • example_3 • investigate_coder

---

## train_1

**input:**
```
0 0 0 1 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 1
0 0 1 0 0 0 0 0 0 5
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 5 1 0 1 0 0 0 0 0
0 8 1 0 0 0 1 0 3 0
0 0 0 0 0 0 0 3 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360398B4D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
2 4 2 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360398AAD0>

## train_2

**input:**
```
2 7 7 1 0 3 0 0 0 3
0 0 0 9 0 0 0 0 3 7
0 0 0 1 0 0 0 6 0 9
0 0 0 0 0 0 0 1 0 0
9 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 3 0
0 5 0 7 3 0 0 0 1 0
4 4 0 0 0 1 0 0 0 5
0 0 0 0 0 0 0 5 3 0
0 0 0 0 4 5 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C3603989BD0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 2 6 2 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C360398B450>

## train_3

**input:**
```
6 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 2 8
0 7 0 0 2 0 5 0 2 0
0 9 0 1 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 1
0 0 0 0 0 6 0 0 0 0
0 1 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 5 0 0 0 0 0 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36039887D0>

**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 3 2 0 0
0 0 0 0 0 2 2 2 0 0
```

<PIL.Image.Image image mode=RGB size=640x640 at 0x7C36039888D0>
<PIL.Image.Image image mode=RGB size=2000x1330 at 0x7C3603989650>Okay, let's analyze the provided input-output examples to understand the transformation.

**Perception of Elements:**

The task involves colored grids. The input grids have various single-pixel colors scattered across the grid. The output grids seem to be mostly empty (white, color 0), except for a concentrated area of red (color 2) pixels, sometimes containing a single different colored pixel inside. The location and size of this red area seems related to the distribution of colors in the input.  It looks like the output isolates and transforms a specific region of the input grid based on color. The key seems to be identifying a non-white color cluster, replacing all but one pixel in the cluster with red(2), keeping one of the original colored pixels, and clearing all other pixels.

**YAML Block (Facts):**


```yaml
objects:
  - name: input_grid
    type: grid
    properties:
      - width: 10
      - height: 10
      - cells: integers (0-9, representing colors)
  - name: output_grid
    type: grid
    properties:
      - width: 10
      - height: 10
      - cells: integers (0-9, representing colors)
  - name: colored_pixels
    type: pixel_cluster
    properties:
       - colors: List[integer]
       - locations: List[tuple(row,col)]

actions:
  - name: identify_cluster
    input: input_grid
    output: colored_pixels
    description: Finds the largest contiguous cluster of non-white pixels.
  - name: transform_cluster
    input: colored_pixels
    output: output_grid
    description:  Creates a new grid, replaces the clustered pixels with red (2) except one and clears all others.
  - name: select_center_pixel
    input: colored_pixels
    output: tuple(row,col)
    description: finds a pixel, usually colored, inside the cluster

relationships:
  - type: spatial
    relation: adjacency (pixels in the cluster are adjacent)
  - type: transformation
    relation: input_grid is transformed to output_grid by isolating and recoloring a color cluster.
```


**Natural Language Program:**

1. **Find the largest contiguous cluster:** Scan the input grid and find the largest group of connected non-white pixels.  Pixels are considered connected if they are adjacent horizontally, vertically, or diagonally.

2. **Create output grid initialized to all white:**. The output grid dimensions match the input.

3.  **Locate "center":** Find the approximate "center" of the cluster. If multiple non-zero pixels of same kind are presented, keep only one.

4. **Recolor the Cluster:** In the identified cluster in the input grid:
   - Change all pixels in the output grid corresponding to this cluster to red (value 2).
   - Keep single pixel found in step 3 to the original color in the input.

5. **Clear Remaining Pixels:** All pixels in the output grid that are not part of the transformed cluster remain white (value 0).

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
