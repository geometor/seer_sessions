
## train_1

**input:**
```
0 4 0
0 8 0
2 0 0
```


**output:**
```
0 4 0 0 0 0
0 8 4 0 0 0
2 0 8 4 0 0
0 2 0 8 4 0
0 0 2 0 8 4
0 0 0 2 0 8
```


## train_2

**input:**
```
6 1 0
3 0 0
0 0 0
```


**output:**
```
6 1 0 0 0 0
3 6 1 0 0 0
0 3 6 1 0 0
0 0 3 6 1 0
0 0 0 3 6 1
0 0 0 0 3 6
```


## train_3

**input:**
```
0 0 6
1 3 0
0 0 0
```


**output:**
```
0 0 6 0 0 0
1 3 0 6 0 0
0 1 3 0 6 0
0 0 1 3 0 6
0 0 0 1 3 0
0 0 0 0 1 3
```

*   **Perception**: The input is a small grid (3x3 in all examples) containing a few colored pixels against a white background. The output is a larger grid (6x6 in all examples). The colored pixels from the input appear to be "streaked" or copied diagonally downwards and to the right in the output grid. Each streak starts at the original position of the input pixel and continues until it hits the boundary of the output grid.

*   **YAML Facts**:
    
```yaml
    task_context:
      grid_size_relation:
        input_dimensions: [H, W] = [3, 3] (observed in examples)
        output_dimensions: [H', W'] = [6, 6] (observed in examples)
        hypothesis: H' = H + 3, W' = W + 3
      background_color: 0 (white)
      transformation_type: Pattern generation based on input pixels.
    
    objects:
      - type: pixel
        properties:
          - color: Integer (1-9) representing a specific color.
          - position: Coordinates (row, column) in the input grid.
        count: Variable, depends on the input grid.
    
    actions:
      - name: create_output_grid
        inputs: [input_grid_height, input_grid_width]
        outputs: output_grid
        details: Create a new grid with dimensions (input_height + 3, input_width + 3), initialized with the background color (0).
      - name: copy_and_streak_pixel
        inputs: [input_pixel_color, input_pixel_position(r, c), output_grid]
        outputs: modified_output_grid
        condition: input_pixel_color is not the background color (0).
        details: |
          For a non-background pixel at (r, c) in the input grid with color C:
          Iteratively set the color of pixels in the output grid starting at (r, c).
          In each step i (starting from i=0), set output_grid[r+i][c+i] = C.
          Continue this process as long as (r+i) is within the output grid's height and (c+i) is within the output grid's width.
    
    relationships:
      - type: mapping
        from: Each non-background input pixel.
        to: A diagonal line/streak of the same color in the output grid.
        details: The streak starts at the input pixel's coordinates and extends downwards and rightwards.
    
    ```


*   **Natural Language Program**:
    1.  Determine the dimensions of the input grid (Height `H`, Width `W`).
    2.  Calculate the dimensions of the output grid: Output Height `H'` = `H` + 3, Output Width `W'` = `W` + 3.
    3.  Create a new output grid of size `H'` x `W'`, initializing all its cells to the background color (white, 0).
    4.  Iterate through each cell of the input grid at position (row `r`, column `c`).
    5.  Let `C` be the color of the input cell `input[r][c]`.
    6.  If `C` is not the background color (0):
        a.  Initialize a current row `dr` = `r` and current column `dc` = `c`.
        b.  Start a loop that continues as long as `dr` is less than `H'` AND `dc` is less than `W'`.
        c.  Inside the loop, set the color of the output grid cell `output[dr][dc]` to `C`.
        d.  Increment `dr` by 1.
        e.  Increment `dc` by 1.
    7.  After iterating through all input cells, return the completed output grid.
