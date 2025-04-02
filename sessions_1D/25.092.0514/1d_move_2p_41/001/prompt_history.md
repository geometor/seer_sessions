
## train_1

**input:**
```
0 2 2 2 2 2 2 2 2 2 0 0 0 0
```


**output:**
```
0 0 0 2 2 2 2 2 2 2 2 2 0 0
```


## train_2

**input:**
```
0 0 2 2 2 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 7 7 7 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 7 7 7 7 7 7 0 0
```

**Perception:**

The input and output are both 1-dimensional arrays (or grids of height 1) containing integer values representing colors. In each example pair, the input grid contains a single contiguous block of a non-white color (red or orange) surrounded by white pixels (0). The output grid shows this same block of color, identical in size and color, shifted two positions to the right compared to its position in the input grid. The rest of the grid remains filled with white pixels.

**YAML Facts:**


```yaml
task_type: transformation
grid_dimensionality: 1D (or 1xN)
background_color: white (0)
objects:
  - type: contiguous_block
    count: 1
    properties:
      - color: non-white (varies: red (2), orange (7))
      - size: variable (preserved during transformation)
      - location: variable (changes during transformation)
actions:
  - name: shift_object
    target: the non-white contiguous_block
    direction: right
    distance: 2 positions
relationships:
  - type: spatial
    description: The non-white block is surrounded by the background color.
constraints:
  - The size of the grid remains unchanged.
  - The color of the block remains unchanged.
  - The size (length) of the block remains unchanged.
  - There is always exactly one non-white block.
```


**Natural Language Program:**

1.  Identify the contiguous block of non-white pixels in the input grid.
2.  Determine the starting and ending indices of this block.
3.  Calculate the new starting index by adding 2 to the original starting index.
4.  Calculate the new ending index by adding 2 to the original ending index.
5.  Create a new grid of the same size as the input grid, filled entirely with the background color (white, 0).
6.  Place the original non-white block into the new grid starting at the calculated new starting index and ending at the calculated new ending index.
7.  The resulting grid is the output.
