
## train_1

**input:**
```
0 1 0
1 0 1
0 1 0
1 0 1
0 1 0
1 0 1
```


**output:**
```
0 2 0
2 0 2
0 2 0
2 0 2
0 2 0
2 0 2
0 2 0
2 0 2
0 2 0
```


## train_2

**input:**
```
0 1 0
1 1 0
0 1 0
0 1 1
0 1 0
1 1 0
```


**output:**
```
0 2 0
2 2 0
0 2 0
0 2 2
0 2 0
2 2 0
0 2 0
0 2 2
0 2 0
```


## train_3

**input:**
```
0 1 0
1 1 0
0 1 0
0 1 0
1 1 0
0 1 0
```


**output:**
```
0 2 0
2 2 0
0 2 0
0 2 0
2 2 0
0 2 0
0 2 0
2 2 0
0 2 0
```

*   **Perception**
    *   The input grids consist of `white` (0) and `blue` (1) pixels.
    *   The output grids consist of `white` (0) and `red` (2) pixels.
    *   All examples show an input grid of size 6x3 and an output grid of size 9x3.
    *   The transformation involves changing the color of the non-white pixels from `blue` (1) to `red` (2).
    *   The output grid's height is 1.5 times the input grid's height. The width remains the same.
    *   The output grid appears to be constructed by first taking the entire input grid (with colors changed) and then appending the top half of that modified grid to its bottom. In the examples, the input height is 6, so the top half is the first 3 rows. These top 3 rows (after color change) are appended below the original 6 rows (after color change) to form the 9-row output.

*   **Facts**
    
```yaml
    task: color_change_and_vertical_append
    input_elements:
      - type: grid
        properties:
          height: H (e.g., 6)
          width: W (e.g., 3)
          pixels:
            - color: white (0)
            - color: blue (1)
    output_elements:
      - type: grid
        properties:
          height: 1.5 * H (e.g., 9)
          width: W (e.g., 3)
          pixels:
            - color: white (0)
            - color: red (2)
    transformation:
      - action: modify_pixels
        input: input_grid
        output: intermediate_grid
        rule: Change all blue (1) pixels to red (2). Keep white (0) pixels unchanged.
      - action: extract_subgrid
        input: intermediate_grid
        output: top_half_grid
        rule: Select the top H/2 rows of the intermediate_grid.
      - action: concatenate_vertically
        input_1: intermediate_grid
        input_2: top_half_grid
        output: output_grid
        rule: Append top_half_grid below intermediate_grid.
    relationships:
      - Output grid height is 1.5 times the input grid height.
      - Output grid width is the same as the input grid width.
      - The pattern in the output grid consists of the input pattern (with color changed) followed by a repetition of its top half.
    ```


*   **Natural Language Program**
    1.  Create a new grid (intermediate grid) by copying the input grid.
    2.  Iterate through each pixel of the intermediate grid. If a pixel's color is `blue` (1), change its color to `red` (2). Otherwise, leave it unchanged.
    3.  Determine the height `H` of the input grid.
    4.  Identify the top half of the intermediate grid, which consists of the first `H / 2` rows.
    5.  Construct the final output grid by vertically stacking the entire intermediate grid on top of its identified top half.
