
## train_1

**input:**
```
5 0 0
0 5 0
0 0 5
```


**output:**
```
1 2 0 0 0 0
2 1 0 0 0 0
0 0 1 2 0 0
0 0 2 1 0 0
0 0 0 0 1 2
0 0 0 0 2 1
```


## train_2

**input:**
```
0 5 0
5 5 5
0 5 0
```


**output:**
```
0 0 1 2 0 0
0 0 2 1 0 0
1 2 1 2 1 2
2 1 2 1 2 1
0 0 1 2 0 0
0 0 2 1 0 0
```


## train_3

**input:**
```
0 5 0
0 5 5
5 5 0
```


**output:**
```
0 0 1 2 0 0
0 0 2 1 0 0
0 0 1 2 1 2
0 0 2 1 2 1
1 2 1 2 0 0
2 1 2 1 0 0
```

Okay, let's analyze the provided examples.

**Perception of Task Elements:**

1.  **Grid Transformation:** The core task involves transforming an input grid into a larger output grid.
2.  **Scaling:** The output grid dimensions are consistently double the input grid dimensions (e.g., 3x3 input becomes 6x6 output). This suggests a scaling factor of 2.
3.  **Pixel Mapping:** Each pixel in the input grid appears to map onto a 2x2 block of pixels in the output grid.
4.  **Color Transformation Rules:**
    *   Input pixels with the color white (0) are transformed into a 2x2 block of all white (0) pixels in the output.
    *   Input pixels with the color gray (5) are transformed into a specific 2x2 pattern in the output:
        
```
        1 2  (blue, red)
        2 1  (red,  blue)
        ```

5.  **Positional Correspondence:** The position of the 2x2 block in the output grid corresponds directly to the position of the source pixel in the input grid, scaled by the factor of 2. For an input pixel at `(row, col)`, the corresponding 2x2 block occupies the output grid area from `(row*2, col*2)` to `(row*2 + 1, col*2 + 1)`.

**Facts:**


```yaml
task_type: grid_transformation
input_properties:
  - grid:
      colors: [0, 5] # white, gray
      description: Smaller grid representing the initial state.
output_properties:
  - grid:
      colors: [0, 1, 2] # white, blue, red
      size_relation_to_input: height doubles, width doubles
      description: Larger grid resulting from the transformation.
transformation:
  type: pixel_to_block_mapping
  scaling_factor: 2
  rules:
    - input_pixel_color: 0 # white
      output_block: [[0, 0], [0, 0]] # 2x2 white block
    - input_pixel_color: 5 # gray
      output_block: [[1, 2], [2, 1]] # 2x2 blue/red pattern block
  mapping_logic: Each pixel at (r, c) in the input maps to the 2x2 block starting at (r*2, c*2) in the output.
```


**Natural Language Program:**

1.  Determine the dimensions (height `H`, width `W`) of the input grid.
2.  Create a new output grid with dimensions (`H` * 2, `W` * 2), initially filled with a default color (e.g., white/0).
3.  Iterate through each pixel of the input grid using its row index `r` (from 0 to `H`-1) and column index `c` (from 0 to `W`-1).
4.  For the current input pixel at `(r, c)`:
    a.  If the pixel's color is white (0), place a 2x2 block of white (0) pixels into the output grid starting at position (`r` * 2, `c` * 2). The block will occupy `(r*2, c*2)`, `(r*2, c*2 + 1)`, `(r*2 + 1, c*2)`, and `(r*2 + 1, c*2 + 1)`.
    b.  If the pixel's color is gray (5), place the specific 2x2 pattern `[[blue, red], [red, blue]]` (which corresponds to `[[1, 2], [2, 1]]`) into the output grid starting at position (`r` * 2, `c` * 2). Specifically:
        i.  Set output pixel `(r*2, c*2)` to blue (1).
        ii. Set output pixel `(r*2, c*2 + 1)` to red (2).
        iii. Set output pixel `(r*2 + 1, c*2)` to red (2).
        iv. Set output pixel `(r*2 + 1, c*2 + 1)` to blue (1).
5.  Return the completed output grid.
