
## train_1

**input:**
```
0 0 0 8 0 6 0 8 0 0 6
0 0 0 8 0 0 0 8 0 6 0
0 6 0 8 0 6 0 8 0 0 0
8 8 8 8 8 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 6 0 8 0 0 0
6 0 0 8 0 0 0 8 0 6 0
8 8 8 8 8 8 8 8 8 8 8
0 0 0 8 0 0 0 8 6 0 0
0 6 0 8 0 0 0 8 0 0 6
0 0 0 8 6 0 0 8 0 0 0
```


**output:**
```
0 1 1
0 0 0
0 0 1
```


## train_2

**input:**
```
6 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 6 8 0 0 6
0 0 0 8 0 0 0 8 0 0 0
8 8 8 8 8 8 8 8 8 8 8
6 0 0 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 6 0
0 0 0 8 0 0 6 8 6 0 0
8 8 8 8 8 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0
6 0 0 8 0 0 0 8 0 0 0
0 6 0 8 0 6 0 8 0 0 6
```


**output:**
```
0 0 0
0 0 1
1 0 0
```


## train_3

**input:**
```
0 0 0 8 0 0 0 8 0 0 6
0 0 6 8 0 0 0 8 6 0 0
0 0 0 8 0 6 0 8 0 0 0
8 8 8 8 8 8 8 8 8 8 8
0 0 0 8 0 6 0 8 0 0 0
6 0 0 8 0 0 6 8 0 0 0
0 0 0 8 0 0 0 8 0 6 0
8 8 8 8 8 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0
0 0 6 8 0 0 0 8 6 0 0
0 0 0 8 0 6 0 8 0 0 0
```


**output:**
```
0 0 1
0 1 0
0 0 0
```


## train_4

**input:**
```
0 0 0 8 0 0 0 8 0 0 0
6 0 0 8 0 6 0 8 0 0 6
0 0 6 8 0 0 0 8 0 6 0
8 8 8 8 8 8 8 8 8 8 8
0 6 0 8 0 0 6 8 0 0 0
0 0 0 8 0 0 0 8 0 0 0
0 6 0 8 0 0 0 8 6 0 0
8 8 8 8 8 8 8 8 8 8 8
0 0 6 8 0 0 0 8 0 0 0
0 0 0 8 0 0 0 8 0 6 0
0 0 0 8 6 0 0 8 0 0 0
```


**output:**
```
1 0 1
1 0 0
0 0 0
```

*   **Perception**:
    *   The input grids are always 11x11.
    *   The input grids contain consistent structural elements: two horizontal lines and two vertical lines of Azure (8) pixels. These lines are always at rows 3 and 7, and columns 3 and 7 (0-indexed).
    *   These Azure lines divide the input grid into nine 3x3 subgrids.
    *   The pixels within these 3x3 subgrids are either White (0) or Magenta (6). The Azure lines act as separators.
    *   The output grids are always 3x3.
    *   The output grids contain only White (0) and Blue (1) pixels.
    *   There appears to be a positional correspondence between the nine 3x3 subgrids in the input and the nine cells in the 3x3 output grid. For example, the top-left 3x3 subgrid in the input maps to the top-left cell in the output.
    *   The transformation rule seems to depend on the content of each 3x3 input subgrid. Specifically, it relates to the count of Magenta (6) pixels within each subgrid.
    *   Observing the examples, an output cell is Blue (1) if and only if the corresponding input 3x3 subgrid contains exactly two Magenta (6) pixels. Otherwise, the output cell is White (0).

*   **Facts**:
    
```yaml
    task_type: grid_transformation
    input_grid:
      properties:
        size: 11x11
        structure: partitioned by Azure (8) lines at rows 3, 7 and columns 3, 7
        partitions: nine 3x3 subgrids
        colors_in_partitions: [White (0), Magenta (6)]
    output_grid:
      properties:
        size: 3x3
        colors: [White (0), Blue (1)]
      relationship_to_input:
        spatial_mapping: each output cell (r, c) corresponds to the input subgrid at grid indices [(r*4):(r*4+3), (c*4):(c*4+3)]
        transformation_rule: based on the content of the corresponding input subgrid
    rule_details:
      condition: count of Magenta (6) pixels within a 3x3 input subgrid
      mapping:
        - if count == 2: output pixel is Blue (1)
        - if count != 2: output pixel is White (0)
    ```


*   **Natural Language Program**:
    1.  Initialize an empty 3x3 output grid with all White (0) pixels.
    2.  Iterate through the nine 3x3 subgrids defined by the Azure (8) partition lines in the input grid. The subgrids are located at the top-left corners: (0,0), (0,4), (0,8), (4,0), (4,4), (4,8), (8,0), (8,4), (8,8).
    3.  For each 3x3 input subgrid:
        a.  Count the number of pixels with the color Magenta (6).
        b.  Determine the corresponding position (row `r`, column `c`) in the 3x3 output grid based on the subgrid's position (e.g., input subgrid at (0,0) maps to output (0,0), input subgrid at (4,8) maps to output (1,2), etc.). The mapping can be calculated as `r = input_subgrid_row // 4` and `c = input_subgrid_col // 4`.
        c.  If the count of Magenta pixels in the subgrid is exactly 2, set the corresponding pixel in the output grid at position (`r`, `c`) to Blue (1).
    4.  Return the final 3x3 output grid.
