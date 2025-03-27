
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 5 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 1 1 1
0 0 0 1 1 1 1 1 1
0 0 0 1 1 1 1 1 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0
1 1 1 0 0 0 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 1 1 1
```

*   **Perception:**
    *   The input grids contain a white background (0) and several isolated gray pixels (5).
    *   The output grids have the same dimensions as the input grids.
    *   The output grids also have a white background (0) but contain shapes made of blue pixels (1) instead of gray pixels.
    *   Each gray pixel in the input corresponds to a 3x3 square block of blue pixels in the output.
    *   The center of each blue 3x3 square in the output coincides with the position of a gray pixel in the input.
    *   In Example 1, two gray pixels are close enough that their corresponding 3x3 blue squares overlap in the output. The overlapping region remains blue.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_size_relation: same input and output dimensions
      background_color: 0 (white)
      input_elements:
        - object: gray_pixel
          color: 5
          properties: point-like (1x1)
          count: variable (3 or 4 in examples)
      output_elements:
        - object: blue_square
          color: 1
          properties: 3x3 shape
          count: equal to the count of input gray_pixels
      transformation:
        type: replacement_and_expansion
        mapping: each input gray_pixel maps to one output blue_square
        positional_rule: output blue_square is centered at the location of the corresponding input gray_pixel
        overlap_handling: overlapping blue_squares merge into a single blue region
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with white pixels (0).
    2.  Iterate through each cell of the input grid.
    3.  If a cell contains a gray pixel (5) at coordinates (row, column):
        a.  Define the 3x3 region centered at (row, column) in the output grid. This region includes cells from (row-1, column-1) to (row+1, column+1).
        b.  For every cell within this 3x3 region, if the cell coordinates are valid (within the grid boundaries), change its color to blue (1) in the output grid.
    4.  Return the final output grid.
