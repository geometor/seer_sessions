
## train_1

**input:**
```
0 3 0
0 7 7
0 0 0
```


**output:**
```
0 0 3 3 0 0
0 0 3 3 0 0
0 0 7 7 7 7
0 0 7 7 7 7
0 0 0 0 0 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 8 0
0 8 5 5
0 0 0 5
0 0 0 0
```


**output:**
```
0 0 0 0 8 8 0 0
0 0 0 0 8 8 0 0
0 0 8 8 5 5 5 5
0 0 8 8 5 5 5 5
0 0 0 0 0 0 5 5
0 0 0 0 0 0 5 5
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves transforming a smaller input grid into a larger output grid. The output grid appears to be a scaled-up version of the input grid. Each pixel in the input grid seems to correspond to a 2x2 block of the same color in the output grid. The overall structure and relative positions of the colors are preserved, but magnified.

*   **Facts:**
    
```yaml
    task_type: scaling
    elements:
      - type: grid
        role: input
        properties:
          height: H_in
          width: W_in
      - type: grid
        role: output
        properties:
          height: H_out
          width: W_out
      - type: pixel
        properties:
          color: C (0-9)
          position: (row, col)
    relationships:
      - dimension_scaling:
          H_out = 2 * H_in
          W_out = 2 * W_in
      - pixel_mapping:
          input_pixel_at_(r, c)_with_color_C -> output_block_of_color_C
          output_block_top_left: (2*r, 2*c)
          output_block_size: 2x2
    ```


*   **Natural Language Program:**
    1.  Determine the dimensions (height `H_in`, width `W_in`) of the input grid.
    2.  Create a new output grid with dimensions `2 * H_in` height and `2 * W_in` width.
    3.  Iterate through each pixel at position (`r`, `c`) in the input grid.
    4.  Get the color `C` of the input pixel at (`r`, `c`).
    5.  In the output grid, fill a 2x2 block of pixels, starting at the top-left position (`2*r`, `2*c`), with the color `C`. Specifically, set the pixels at (`2*r`, `2*c`), (`2*r+1`, `2*c`), (`2*r`, `2*c+1`), and (`2*r+1`, `2*c+1`) to color `C`.
    6.  Return the completed output grid.
