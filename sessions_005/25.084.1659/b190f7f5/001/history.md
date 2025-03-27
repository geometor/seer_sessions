
## train_1

**input:**
```
0 0 8 0 4 0
8 0 0 1 2 4
8 8 0 0 1 0
```


**output:**
```
0 0 0 0 0 4 0 0 0
0 0 0 4 0 0 0 0 0
0 0 0 4 4 0 0 0 0
0 0 1 0 0 2 0 0 4
1 0 0 2 0 0 4 0 0
1 1 0 2 2 0 4 4 0
0 0 0 0 0 1 0 0 0
0 0 0 1 0 0 0 0 0
0 0 0 1 1 0 0 0 0
```


## train_2

**input:**
```
2 0 4 0 8 0
0 3 0 8 8 8
0 0 0 0 8 0
```


**output:**
```
0 2 0 0 0 0 0 4 0
2 2 2 0 0 0 4 4 4
0 2 0 0 0 0 0 4 0
0 0 0 0 3 0 0 0 0
0 0 0 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
2 0 0 4 0 0 8 0
0 2 4 0 8 8 8 8
0 4 2 0 0 0 8 0
4 0 0 2 0 0 8 0
```


**output:**
```
0 0 2 0 0 0 0 0 0 0 0 0 0 0 4 0
2 2 2 2 0 0 0 0 0 0 0 0 4 4 4 4
0 0 2 0 0 0 0 0 0 0 0 0 0 0 4 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 4 0
0 0 0 0 0 0 2 0 0 0 4 0 0 0 0 0
0 0 0 0 2 2 2 2 4 4 4 4 0 0 0 0
0 0 0 0 0 0 2 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 0 0 4 4 4 4 2 2 2 2 0 0 0 0
0 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 2 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
4 4 4 4 0 0 0 0 0 0 0 0 2 2 2 2
0 0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 2 0
```

**Perception:**

1.  **Input/Output Size:** The output grid dimensions are exactly 3 times the input grid dimensions (height and width).
2.  **Pixel Mapping:** Each pixel in the input grid seems to correspond to a 3x3 area in the output grid.
3.  **Background:** The background color in both input and output is white (0).
4.  **Transformation Pattern:** Non-white pixels in the input are transformed into a specific 3x3 pattern in the output, centered within the corresponding 3x3 area. White pixels in the input map to a 3x3 block of white pixels in the output.
5.  **Pattern Details:** For a non-white input pixel of color `C` at position `(r, c)`, the corresponding 3x3 block in the output, starting at `(3*r, 3*c)`, follows this pattern:
    
```
    0 C 0
    C C C
    0 C 0
    ```

    This pattern looks like a plus sign (+) made of the color `C`.

**Facts:**


```yaml
task_context:
  description: Scale each non-white pixel in the input grid into a 3x3 pattern in the output grid.
  grid_size_relation: Output grid dimensions are 3 times the input grid dimensions.
  background_color: white (0) remains the background.

transformation:
  type: pixel-wise scaling with pattern replacement
  scale_factor: 3x3
  operations:
    - description: Iterate through each pixel (r, c) in the input grid.
    - input_pixel: pixel at (r, c) with color C
    - output_block: 3x3 area in the output grid starting at (3*r, 3*c)
    - conditions:
      - if C is white (0):
          action: Fill the corresponding output_block with white (0).
      - if C is non-white:
          action: Fill the corresponding output_block with a specific pattern based on color C.
          pattern: |
            [[0, C, 0],
             [C, C, C],
             [0, C, 0]]
```


**Natural Language Program:**

1.  Determine the dimensions (height `H`, width `W`) of the input grid.
2.  Create a new output grid with dimensions `(3 * H, 3 * W)`, initialized entirely with white pixels (0).
3.  For each row `r` from 0 to `H-1` and each column `c` from 0 to `W-1` in the input grid:
    a.  Get the color `C` of the pixel at `input[r, c]`.
    b.  If the color `C` is not white (i.e., `C != 0`):
        i.  Calculate the top-left coordinates `(R, Col)` for the 3x3 block in the output grid: `R = 3 * r`, `Col = 3 * c`.
        ii. Set the pixels in the output grid according to the plus sign pattern:
            - `output[R, Col + 1] = C`
            - `output[R + 1, Col] = C`
            - `output[R + 1, Col + 1] = C`
            - `output[R + 1, Col + 2] = C`
            - `output[R + 2, Col + 1] = C`
4.  Return the generated output grid.
