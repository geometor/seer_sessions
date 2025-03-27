
## train_1

**input:**
```
0 8 0
0 6 6
9 8 0
```


**output:**
```
0 0 0 8 8 8 0 0 0
0 0 0 8 8 8 0 0 0
0 0 0 8 8 8 0 0 0
0 0 0 6 6 6 6 6 6
0 0 0 6 6 6 6 6 6
0 0 0 6 6 6 6 6 6
9 9 9 8 8 8 0 0 0
9 9 9 8 8 8 0 0 0
9 9 9 8 8 8 0 0 0
```


## train_2

**input:**
```
1 0 4
0 4 0
0 1 0
```


**output:**
```
1 1 0 0 4 4
1 1 0 0 4 4
0 0 4 4 0 0
0 0 4 4 0 0
0 0 1 1 0 0
0 0 1 1 0 0
```


## train_3

**input:**
```
3 2 0
0 7 3
0 0 0
```


**output:**
```
3 3 3 2 2 2 0 0 0
3 3 3 2 2 2 0 0 0
3 3 3 2 2 2 0 0 0
0 0 0 7 7 7 3 3 3
0 0 0 7 7 7 3 3 3
0 0 0 7 7 7 3 3 3
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
4 0 3
2 2 0
0 0 8
```


**output:**
```
4 4 4 4 0 0 0 0 3 3 3 3
4 4 4 4 0 0 0 0 3 3 3 3
4 4 4 4 0 0 0 0 3 3 3 3
4 4 4 4 0 0 0 0 3 3 3 3
2 2 2 2 2 2 2 2 0 0 0 0
2 2 2 2 2 2 2 2 0 0 0 0
2 2 2 2 2 2 2 2 0 0 0 0
2 2 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 0 0 8 8 8 8
```


## train_5

**input:**
```
6 7 0
0 6 6
0 0 0
```


**output:**
```
6 6 7 7 0 0
6 6 7 7 0 0
0 0 6 6 6 6
0 0 6 6 6 6
0 0 0 0 0 0
0 0 0 0 0 0
```

*   **Perception:** The task involves scaling up the input grid. Each pixel in the input grid is transformed into a square block of the same color in the output grid. The size of this square block (the scaling factor) varies between examples and appears to depend on the content of the input grid. Specifically, the scaling factor seems to be equal to the number of unique non-white colors present in the input grid.

*   **YAML Facts:**
    
```yaml
    task_type: upsampling
    input_object:
      type: grid
      description: A small grid of colored pixels.
    output_object:
      type: grid
      description: A larger grid, scaled up from the input.
    transformation:
      name: pixel_block_scaling
      steps:
        - step: 1
          action: analyze_input
          input: input_grid
          details: Identify all unique non-white (non-zero) colors present.
          output: unique_colors_set
        - step: 2
          action: calculate_scaling_factor
          input: unique_colors_set
          details: Count the number of colors in the set.
          output: scaling_factor_N
        - step: 3
          action: determine_output_dimensions
          input: input_grid_dimensions, scaling_factor_N
          details: Multiply input height and width by scaling_factor_N.
          output: output_grid_dimensions
        - step: 4
          action: create_output_grid
          input: output_grid_dimensions
          details: Initialize an empty grid with the calculated dimensions, filled with a default color (e.g., white/0).
          output: output_grid
        - step: 5
          action: map_pixels_to_blocks
          input: input_grid, scaling_factor_N, output_grid
          details: For each pixel at (row, col) with color C in the input grid, fill an N x N block in the output grid starting at (row * N, col * N) with color C.
          output: final_output_grid
    parameters:
      scaling_factor_N:
        description: The side length of the square block each input pixel expands into.
        determination: Count of unique non-white colors in the input grid.
    relationships:
      - input_pixel_color determines the color of the corresponding output block.
      - input_pixel_position determines the top-left position of the corresponding output block (scaled by N).
      - The number of unique non-white colors in the input determines the scaling factor N.
    ```


*   **Natural Language Program:**
    1.  Count the number of distinct non-white (color values 1 through 9) pixels present in the input grid. Let this count be `N`.
    2.  Determine the dimensions of the input grid (height `H_in`, width `W_in`).
    3.  Calculate the dimensions of the output grid: height `H_out = H_in * N`, width `W_out = W_in * N`.
    4.  Create the output grid with dimensions `H_out` x `W_out`.
    5.  Iterate through each pixel of the input grid from `row = 0` to `H_in - 1` and `col = 0` to `W_in - 1`.
    6.  Let the color of the input pixel at `(row, col)` be `C`.
    7.  In the output grid, fill the square block of size `N x N`, whose top-left corner is at `(row * N, col * N)`, entirely with the color `C`.
    8.  Return the completed output grid.
