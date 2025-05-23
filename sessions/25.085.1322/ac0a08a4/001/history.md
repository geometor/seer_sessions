
## train_1

**input:**
```
0 4 0
0 0 8
6 0 0
```


**output:**
```
0 0 0 4 4 4 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 4 4 4 0 0 0
0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 8 8 8
6 6 6 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0
6 6 6 0 0 0 0 0 0
```


## train_2

**input:**
```
2 0 0
0 0 7
0 0 0
```


**output:**
```
2 2 0 0 0 0
2 2 0 0 0 0
0 0 0 0 7 7
0 0 0 0 7 7
0 0 0 0 0 0
0 0 0 0 0 0
```


## train_3

**input:**
```
0 6 9
3 0 2
0 7 0
```


**output:**
```
0 0 0 0 0 6 6 6 6 6 9 9 9 9 9
0 0 0 0 0 6 6 6 6 6 9 9 9 9 9
0 0 0 0 0 6 6 6 6 6 9 9 9 9 9
0 0 0 0 0 6 6 6 6 6 9 9 9 9 9
0 0 0 0 0 6 6 6 6 6 9 9 9 9 9
3 3 3 3 3 0 0 0 0 0 2 2 2 2 2
3 3 3 3 3 0 0 0 0 0 2 2 2 2 2
3 3 3 3 3 0 0 0 0 0 2 2 2 2 2
3 3 3 3 3 0 0 0 0 0 2 2 2 2 2
3 3 3 3 3 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 0 0 0 0 0
0 0 0 0 0 7 7 7 7 7 0 0 0 0 0
```

*   **Perception**: The task involves scaling up an input grid based on a factor derived from the input itself. Each non-white pixel in the input grid is transformed into a square block of the same color in the output grid. The size of this block, and consequently the overall scaling factor for the grid, is determined by the total count of non-white pixels present in the input grid. The output grid maintains the relative positions of these colored blocks corresponding to the positions of the original pixels in the input grid.

*   **YAML Facts**:
    
```yaml
    facts:
      - item: Input Grid
        properties:
          - Contains pixels with values 0-9 (colors).
          - Pixels with value 0 represent the background (white).
          - Pixels with values 1-9 are colored pixels.
          - Has dimensions H_in x W_in.
      - item: Output Grid
        properties:
          - Is a scaled-up version of the input grid.
          - Has dimensions H_out x W_out.
          - Contains square blocks of color corresponding to non-white input pixels.
          - Background is white (0).
      - item: Transformation Rule
        properties:
          - rule: Scaling and Block Replacement
          - parameter: Scale Factor (N)
            derivation: Count of non-white (non-zero) pixels in the input grid.
          - output_dimensions:
              H_out: H_in * N
              W_out: W_in * N
          - mapping: Each non-white pixel at `(r, c)` with color `V` in the input grid is replaced by an `N x N` block of color `V` in the output grid.
          - block_position: The top-left corner of the `N x N` block corresponding to input pixel `(r, c)` is located at `(r * N, c * N)` in the output grid.
          - background_mapping: White pixels (0) in the input correspond to `N x N` blocks of white (0) in the output grid.
    ```


*   **Natural Language Program**:
    1.  Determine the dimensions (height `H_in`, width `W_in`) of the input grid.
    2.  Count the total number of non-white (value > 0) pixels in the input grid. Let this count be `N`.
    3.  If `N` is 0, return the input grid unchanged (or an empty grid, clarification needed - based on examples, N > 0).
    4.  Calculate the dimensions of the output grid: height `H_out = H_in * N`, width `W_out = W_in * N`.
    5.  Create a new grid (the output grid) of size `H_out` x `W_out`, initializing all its pixels to white (0).
    6.  Iterate through each pixel of the input grid at row `r` (from 0 to `H_in - 1`) and column `c` (from 0 to `W_in - 1`).
    7.  Let the color (value) of the input pixel at `(r, c)` be `V`.
    8.  If `V` is not white (i.e., `V > 0`), then fill a square block of size `N`x`N` in the output grid with the color `V`. The top-left corner of this block should be at row `r * N` and column `c * N`. Specifically, for all `i` from 0 to `N-1` and `j` from 0 to `N-1`, set the output pixel at `(r * N + i, c * N + j)` to `V`.
    9.  Return the generated output grid.
