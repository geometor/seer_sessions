
## train_1

**input:**
```
3 0 0 0 2 0
0 0 0 0 0 0
8 0 0 0 8 0
0 0 0 0 0 0
0 0 1 0 0 0
0 0 0 0 0 0
```


**output:**
```
3 0 2
8 0 8
0 1 0
```


## train_2

**input:**
```
2 0 2 0 1 0
0 0 0 0 0 0
2 0 1 0 0 0
0 0 0 0 0 0
3 0 0 0 0 0
0 0 0 0 0 0
```


**output:**
```
2 2 1
2 1 0
3 0 0
```


## train_3

**input:**
```
1 0 0 0 0 0
0 0 0 0 0 0
0 0 2 0 0 0
0 0 0 0 0 0
6 0 0 0 6 0
0 0 0 0 0 0
```


**output:**
```
1 0 0
0 2 0
6 0 6
```

**Perception**

The input grids are consistently 6x6, and the output grids are consistently 3x3. This suggests a downscaling or subsampling operation where the output grid is half the size of the input grid in both dimensions.

Observing the placement of non-white pixels in the input grids, they appear only in rows 0, 2, and 4, and columns 0, 2, and 4. All other rows (1, 3, 5) and columns (1, 3, 5) consist entirely of white pixels (0).

Comparing the input and output grids pixel by pixel reveals a direct mapping:
- The pixel at output coordinate `(r_out, c_out)` corresponds to the pixel at input coordinate `(r_in, c_in)`.
- The relationship seems to be `r_in = r_out * 2` and `c_in = c_out * 2`.

This pattern holds across all provided examples. The transformation effectively extracts pixels from the input grid at even row and even column indices to form the smaller output grid.

**Facts**


```yaml
task_type: grid_transformation
input_grid:
  properties:
    height: 6
    width: 6
    pixels: integers 0-9
    structure: Contains non-white pixels primarily at even row and even column indices. Rows and columns with odd indices are typically white.
output_grid:
  properties:
    height: 3
    width: 3
    pixels: integers 0-9
transformation:
  type: subsampling
  description: >
    Selects pixels from the input grid to create the output grid.
  mapping:
    input_coords: (r_in, c_in)
    output_coords: (r_out, c_out)
    rule: output[r_out, c_out] = input[r_out * 2, c_out * 2]
    details: Takes every second pixel starting from the top-left corner (0,0) along both rows and columns.
```


**Natural Language Program**

1.  Initialize an output grid with a height equal to half the input grid's height and a width equal to half the input grid's width.
2.  Iterate through each row index `r_out` from 0 up to (output height - 1).
3.  Within each row iteration, iterate through each column index `c_out` from 0 up to (output width - 1).
4.  Determine the corresponding input grid coordinates: `r_in = r_out * 2` and `c_in = c_out * 2`.
5.  Copy the pixel value from the input grid at `(r_in, c_in)` to the output grid at `(r_out, c_out)`.
6.  After iterating through all output grid coordinates, return the completed output grid.
