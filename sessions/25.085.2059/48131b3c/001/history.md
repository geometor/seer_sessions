
## train_1

**input:**
```
7 0
0 7
```


**output:**
```
0 7 0 7
7 0 7 0
0 7 0 7
7 0 7 0
```


## train_2

**input:**
```
0 8 0
8 0 8
0 0 0
```


**output:**
```
8 0 8 8 0 8
0 8 0 0 8 0
8 8 8 8 8 8
8 0 8 8 0 8
0 8 0 0 8 0
8 8 8 8 8 8
```


## train_3

**input:**
```
4 0 0 0
0 4 4 4
0 0 4 0
0 4 0 0
```


**output:**
```
0 4 4 4 0 4 4 4
4 0 0 0 4 0 0 0
4 4 0 4 4 4 0 4
4 0 4 4 4 0 4 4
0 4 4 4 0 4 4 4
4 0 0 0 4 0 0 0
4 4 0 4 4 4 0 4
4 0 4 4 4 0 4 4
```

Okay, let's analyze the transformation rule based on the provided examples.

**Perception**

1.  **Grid Size:** The output grid is always twice the height and twice the width of the input grid.
2.  **Color Preservation/Change:** The primary non-white color from the input grid is preserved in the output. White pixels (color 0) are sometimes preserved and sometimes replaced by the primary non-white color.
3.  **Structure:** The output grid appears to be a 2x2 tiling of a transformed version of the input grid.
4.  **Transformation Details:**
    *   The transformation involves row manipulation.
    *   The first two rows of the input grid seem to be swapped in the intermediate (tile) grid.
    *   Rows from the third row onwards in the input are modified: all white pixels (0) in these rows are replaced by the single non-white color present in the input grid. Non-white pixels in these rows remain unchanged.
    *   This modified grid (let's call it the 'tile grid') has the same dimensions as the input grid.
    *   The final output is created by tiling this 'tile grid' two times horizontally and two times vertically.
5.  **Color Identification:** Each input grid contains only white (0) and one other color. This single non-white color is used for the replacement operation.

**Facts**


```yaml
task_description: "Transforms an input grid by creating a modified version and tiling it 2x2."
facts:
  - object: input_grid
    properties:
      - type: grid
      - colors: contains white (0) and exactly one other non-white color (C)
      - dimensions: H rows, W columns
  - object: intermediate_grid (tile_grid)
    properties:
      - type: grid
      - dimensions: H rows, W columns (same as input)
    derivation:
      - step: "Swap the first two rows of the input grid."
        - target: intermediate_grid row 0 receives input_grid row 1
        - target: intermediate_grid row 1 receives input_grid row 0
      - step: "Modify subsequent rows (from index 2 onwards)."
        - for_each: row `i` from 2 to H-1
          - source: input_grid row `i`
          - action: "Replace all white (0) pixels with the non-white color C."
          - action: "Keep all non-white pixels unchanged."
          - target: intermediate_grid row `i`
  - object: output_grid
    properties:
      - type: grid
      - dimensions: 2H rows, 2W columns
    derivation:
      - step: "Tile the intermediate_grid 2x2."
        - placement:
          - top-left quadrant: intermediate_grid
          - top-right quadrant: intermediate_grid
          - bottom-left quadrant: intermediate_grid
          - bottom-right quadrant: intermediate_grid
```


**Natural Language Program**

1.  Identify the dimensions (Height H, Width W) of the input grid.
2.  Identify the single non-white color (let's call it `C`) present in the input grid.
3.  Create a new intermediate grid (let's call it `tile_grid`) with the same dimensions (H x W) as the input grid.
4.  Copy the second row (index 1) of the input grid to the first row (index 0) of the `tile_grid`.
5.  Copy the first row (index 0) of the input grid to the second row (index 1) of the `tile_grid`.
6.  For each subsequent row `i` from index 2 up to H-1 in the input grid:
    a.  Take the corresponding row `i` from the input grid.
    b.  Create a new row by iterating through its pixels: if a pixel is white (0), replace it with color `C`; otherwise, keep the pixel's original color.
    c.  Place this modified row into row `i` of the `tile_grid`.
7.  Create the final output grid with dimensions 2H x 2W.
8.  Construct the output grid by tiling the `tile_grid` in a 2x2 pattern: place copies of the `tile_grid` in the top-left, top-right, bottom-left, and bottom-right quadrants of the output grid.
