
## train_1

**input:**
```
0 2 2
0 0 2
0 0 0
```


**output:**
```
0 0 0
0 2 2
0 0 2
```


## train_2

**input:**
```
0 0 0
1 1 1
0 0 0
```


**output:**
```
0 0 0
0 0 0
1 1 1
```


## train_3

**input:**
```
0 1 0
1 1 0
0 0 0
```


**output:**
```
0 0 0
0 1 0
1 1 0
```


## train_4

**input:**
```
1 1 1
0 0 0
0 0 0
```


**output:**
```
0 0 0
1 1 1
0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of Task Elements:**

*   The input and output grids are always the same size (3x3 in these examples).
*   The grids contain a background color (white, value 0) and one or more objects composed of non-white pixels.
*   In each example, the non-white pixels form a single contiguous object (or multiple objects treated as one unit).
*   The transformation consistently involves moving the non-white object(s) downwards.
*   The distance of the downward movement appears to be exactly one row.
*   The original position occupied by the moved object becomes white in the output.
*   The shape and color of the object(s) are preserved during the movement.

**YAML Facts:**


```yaml
task_description: Move all non-white pixels down by one row.
grid_properties:
  - size_relation: input and output grids have the same dimensions.
  - background_color: white (0) is the default background.
objects:
  - definition: Contiguous block(s) of non-white pixels.
  - properties:
      - color: Preserved during transformation.
      - shape: Preserved during transformation.
      - location: Changes during transformation.
actions:
  - name: translate
  - direction: down
  - distance: 1 row
  - target: all non-white pixels
  - effect:
      - original positions of non-white pixels become white (0) in the output.
      - new positions (row + 1, col) receive the original color of the non-white pixels.
relationships:
  - type: spatial_mapping
  - rule: Input pixel at (row, col) maps to output pixel at (row + 1, col) if the input pixel is not white. Otherwise, the output pixel defaults to white.
constraints:
  - Assumes movement does not cause pixels to go outside the grid boundaries (implied by the examples, but should be verified with more complex cases if available).
```


**Natural Language Program:**

1.  Create a new output grid with the same dimensions as the input grid, initially filled entirely with the background color (white, 0).
2.  Iterate through each cell of the input grid, examining its row index (`r`), column index (`c`), and color value (`color`).
3.  If the `color` of the input cell at `(r, c)` is not white (0):
    *   Calculate the target row index for the output grid as `r + 1`.
    *   Check if the target row index `r + 1` is within the bounds of the grid height.
    *   If the target row is valid, set the color of the cell at `(r + 1, c)` in the output grid to the `color` from the input cell.
4.  Return the completed output grid.
