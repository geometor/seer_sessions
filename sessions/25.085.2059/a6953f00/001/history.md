
## train_1

**input:**
```
7 5 8 2
8 0 4 7
1 6 4 7
8 9 6 9
```


**output:**
```
8 2
4 7
```


## train_2

**input:**
```
0 7 9
5 6 5
3 7 9
```


**output:**
```
0 7
5 6
```


## train_3

**input:**
```
5 8 8 9 2
8 0 5 6 5
7 7 2 2 9
5 5 1 7 4
3 3 8 7 7
```


**output:**
```
5 8
8 0
```

*   **Perception:**
    *   The task involves transforming an input grid into a smaller output grid.
    *   All output grids in the examples are 2x2.
    *   The output grid appears to be a subgrid extracted from the input grid.
    *   Comparing the input and output grids reveals that the output is always a 2x2 section taken from the top two rows of the input.
    *   The horizontal position of this 2x2 section seems to depend on the width of the input grid.
    *   In Example 1, the input grid has a width of 4 (even), and the output is the top-right 2x2 section.
    *   In Examples 2 and 3, the input grids have widths of 3 and 5 respectively (odd), and the outputs are the top-left 2x2 sections.
    *   This suggests a rule based on the parity (even or odd) of the input grid's width.

*   **Facts:**
    
```yaml
    task_type: extraction
    input_grid:
      description: A 2D grid of pixels with varying dimensions (height H, width W).
      properties:
        - height: H (ranges from 3 to 5 in examples)
        - width: W (ranges from 3 to 5 in examples)
    output_grid:
      description: A 2D grid of pixels, always 2x2.
      properties:
        - height: 2
        - width: 2
    transformation:
      type: subgrid_extraction
      parameters:
        - size: 2x2
        - location: determined by input width parity
      logic:
        - if input width W is even: extract the top-right 2x2 subgrid (rows 0-1, columns W-2 to W-1).
        - if input width W is odd: extract the top-left 2x2 subgrid (rows 0-1, columns 0-1).
    ```


*   **Natural Language Program:**
    1.  Determine the width (W) of the input grid.
    2.  Check if the width W is even or odd.
    3.  If W is even, extract the 2x2 subgrid located at the top-right corner of the input grid (rows 0 and 1, columns W-2 and W-1).
    4.  If W is odd, extract the 2x2 subgrid located at the top-left corner of the input grid (rows 0 and 1, columns 0 and 1).
    5.  The extracted 2x2 subgrid is the output grid.
