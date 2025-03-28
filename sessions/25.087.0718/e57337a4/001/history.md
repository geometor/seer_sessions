
## train_1

**input:**
```
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 0 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9 9 9 9 9
```


**output:**
```
9 9 0
9 9 9
9 9 9
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 0 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 0 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
0 8 8
8 0 8
8 8 8
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 0 7 7 7 7 7 7 7 0 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 0 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
0 7 0
0 7 7
7 7 7
```

**Perception:**

1.  **Input Grid Structure:** The input grids are consistently 15x15. They feature a single dominant background color (maroon, azure, or orange in the examples) and one or more isolated white pixels (color 0).
2.  **Output Grid Structure:** The output grids are consistently 3x3. They use the same background color as their corresponding input grid. White pixels appear in the output grid.
3.  **Transformation:** The transformation appears to be a downscaling operation. The 15x15 input grid is mapped onto the 3x3 output grid. This suggests a scaling factor of 5 (15 / 3 = 5).
4.  **Rule:** The process seems to involve dividing the input grid into non-overlapping 5x5 blocks. Each 5x5 block in the input corresponds to a single pixel in the 3x3 output grid. If a 5x5 block in the input contains at least one white pixel, the corresponding pixel in the output grid becomes white. Otherwise, the output pixel takes the background color of the input grid.
5.  **Background Color Identification:** The background color is the color present in the input grid that is not white (0). This color is preserved in the output grid for cells corresponding to input blocks without any white pixels.

**YAML Facts:**


```yaml
Input Grid Properties:
  - Size: 15x15
  - Contains:
    - Background_Color: A single dominant color (non-white).
    - Foreground_Pixels: One or more pixels with color white (0).

Output Grid Properties:
  - Size: 3x3
  - Contains:
    - Background_Color: Same as the input grid's background color.
    - Foreground_Pixels: Pixels with color white (0).

Transformation:
  - Type: Downscaling
  - Scaling_Factor: 5 (Input dimension / Output dimension = 15 / 3 = 5)
  - Mapping: Each 5x5 block in the input maps to one pixel in the output.
  - Rule:
    - Identify the background color of the input grid (the non-white color).
    - Create a 3x3 output grid initialized with the background color.
    - Iterate through the input grid in 5x5 blocks (block indices [0,0], [0,1], [0,2], [1,0], ... [2,2]).
    - For each 5x5 block:
      - If any pixel within the block has the color white (0):
        - Set the corresponding pixel in the output grid (at the block index) to white (0).
      - Else:
        - Keep the corresponding pixel in the output grid as the background color.
```


**Natural Language Program:**

1.  Determine the dimensions of the input grid (always 15x15 in the examples) and the output grid (always 3x3). Calculate the scaling factor by dividing the input dimension by the output dimension (15 / 3 = 5).
2.  Identify the background color of the input grid by finding the color that is not white (0).
3.  Create a new 3x3 grid, initializing all its pixels with the identified background color.
4.  Iterate through the 3x3 output grid positions, using row index `out_r` from 0 to 2 and column index `out_c` from 0 to 2.
5.  For each output position (`out_r`, `out_c`), determine the corresponding 5x5 block in the input grid. The block spans rows from `out_r * 5` to `out_r * 5 + 4` and columns from `out_c * 5` to `out_c * 5 + 4`.
6.  Scan all pixels within this 5x5 input block.
7.  If any pixel within the 5x5 block has the color white (0), set the pixel at (`out_r`, `out_c`) in the output grid to white (0).
8.  If no white pixel is found within the 5x5 block, the pixel at (`out_r`, `out_c`) in the output grid retains the background color assigned in step 3.
9.  Return the completed 3x3 output grid.
