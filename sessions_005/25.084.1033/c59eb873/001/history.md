
## train_1

**input:**
```
2 1
3 1
```


**output:**
```
2 2 1 1
2 2 1 1
3 3 1 1
3 3 1 1
```


## train_2

**input:**
```
0 5 1
5 5 5
2 5 0
```


**output:**
```
0 0 5 5 1 1
0 0 5 5 1 1
5 5 5 5 5 5
5 5 5 5 5 5
2 2 5 5 0 0
2 2 5 5 0 0
```


## train_3

**input:**
```
2 0 3 0
2 1 3 0
0 0 3 3
0 0 3 5
```


**output:**
```
2 2 0 0 3 3 0 0
2 2 0 0 3 3 0 0
2 2 1 1 3 3 0 0
2 2 1 1 3 3 0 0
0 0 0 0 3 3 3 3
0 0 0 0 3 3 3 3
0 0 0 0 3 3 5 5
0 0 0 0 3 3 5 5
```

## Perception

The input is a grid of colored pixels. The output is also a grid of colored pixels. Comparing the input and output grids across all examples reveals a consistent pattern: the output grid is a scaled-up version of the input grid. Specifically, the output grid's height and width are exactly double the input grid's height and width. Each pixel in the input grid is expanded into a 2x2 square of the same color in the output grid. The relative positions of these 2x2 blocks in the output correspond to the positions of the original pixels in the input.

## Facts


```yaml
- task_type: grid_transformation
- transformation: scaling
- input_properties:
    - type: grid
    - elements: pixels (colored cells)
    - dimensions: variable height (H) and width (W)
- output_properties:
    - type: grid
    - elements: pixels (colored cells)
    - dimensions: 2 * H (height), 2 * W (width)
- relationship:
    - each pixel at coordinate (r, c) in the input grid, with color C
    - corresponds to a 2x2 block of pixels in the output grid
    - the 2x2 block consists of pixels at coordinates (2r, 2c), (2r, 2c+1), (2r+1, 2c), and (2r+1, 2c+1)
    - all pixels within this 2x2 block have the same color C as the original input pixel
- scaling_factor: 2 (uniform in both dimensions)
```


## Natural Language Program

1.  Determine the height (H) and width (W) of the input grid.
2.  Create a new output grid with height 2\*H and width 2\*W.
3.  Iterate through each pixel in the input grid, identified by its row index `r` (from 0 to H-1) and column index `c` (from 0 to W-1).
4.  For each input pixel at `(r, c)`, get its color value `C`.
5.  In the output grid, fill a 2x2 block of pixels with the color `C`. The top-left corner of this block is at row `2*r` and column `2*c`. Specifically, set the color of the output pixels at coordinates `(2*r, 2*c)`, `(2*r, 2*c + 1)`, `(2*r + 1, 2*c)`, and `(2*r + 1, 2*c + 1)` to `C`.
6.  Repeat steps 3-5 for all pixels in the input grid.
7.  The resulting grid is the final output.
