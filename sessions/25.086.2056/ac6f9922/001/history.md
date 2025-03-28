
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 2 2 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 2 2 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 3 3 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 3 3 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 2
3 8
```


## train_2

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 2 2 4 1 4 4 4 1 4
4 1 1 4 2 2 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 4 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
2 4
4 4
```


## train_3

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 4 4 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 4 4 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
3 4 1
1 6 8
```

*   **Perception**:
    The task requires identifying specific objects within the input grid and representing their relative spatial arrangement in a smaller output grid. The input grids feature a prominent 1-pixel border of a certain color. Inside this border, there are often internal structures or lines using either the border color or another color. The key elements to identify are 2x2 squares composed of a single, uniform color that is *not* the same as the border color. The output grid captures the colors of these identified 2x2 squares, placing them in positions that reflect their relative row and column locations in the input grid. The dimensions of the output grid are determined by the number of unique rows and columns occupied by the top-left corners of these squares, but with a minimum size of 2x2. Any positions in the output grid that do not correspond to a found 2x2 square are filled with the border color identified from the input grid.

*   **Facts**:
    
```yaml
    task_elements:
      - input_grid: 2D array of pixels (colors 0-9).
      - output_grid: Smaller 2D array representing spatial layout of specific objects.
      - border: 1-pixel frame surrounding the input grid content.
        property: border_color (color of the frame pixels).
      - target_objects: Contiguous 2x2 blocks of pixels.
        properties:
          - uniform_color: All four pixels in the 2x2 block have the same color.
          - color_constraint: The uniform color must not be equal to the border_color.
        location: Defined by the top-left coordinate (row, column).
      - spatial_relationship: The relative row and column positions of the target_objects are important.

    transformation:
      - step_1_identify_border: Determine the border_color from the input grid's outer frame.
      - step_2_find_objects: Scan the input grid to find all 2x2 squares matching the properties (uniform_color, color_constraint).
      - step_3_record_objects: Store the color and top-left coordinate (r, c) for each found object.
      - step_4_determine_indices:
          - Collect all unique row coordinates (`r`) from recorded objects into a sorted list `unique_r`.
          - Collect all unique column coordinates (`c`) from recorded objects into a sorted list `unique_c`.
      - step_5_determine_output_size:
          - Output rows = `max(2, len(unique_r))`
          - Output columns = `max(2, len(unique_c))`
      - step_6_create_output: Initialize an output grid of the calculated size, filled with `border_color`.
      - step_7_map_objects:
          - For each recorded object (color `clr`, coordinate `(r, c)`):
            - Find the index `i` of `r` in `unique_r`.
            - Find the index `j` of `c` in `unique_c`.
            - Set `output_grid[i][j] = clr`.
      - step_8_finalize: The resulting grid is the final output.

    example_reasoning:
      - example_1: Border=8. Objects: Red(2) at (4,9), Green(3) at (11,4). unique_r=[4, 11], unique_c=[4, 9]. Output size=max(2,2)x max(2,2)=2x2. Output initialized with 8. Red maps to (0,1), Green maps to (1,0). Final: [[8, 2], [3, 8]].
      - example_2: Border=4. Object: Red(2) at (4,5). unique_r=[4], unique_c=[5]. Output size=max(2,1)x max(2,1)=2x2. Output initialized with 4. Red maps to (0,0). Final: [[2, 4], [4, 4]].
      - example_3: Border=1. Objects: Green(3)@(3,3), Yellow(4)@(3,7), Magenta(6)@(11,7), Azure(8)@(11,12). unique_r=[3, 11], unique_c=[3, 7, 12]. Output size=max(2,2)x max(2,3)=2x3. Output initialized with 1. Green->(0,0), Yellow->(0,1), Magenta->(1,1), Azure->(1,2). Final: [[3, 4, 1], [1, 6, 8]].
    ```


*   **Natural Language Program**:
    1.  Determine the `border_color` by inspecting the color of the pixels forming the 1-pixel thick outer frame of the input grid.
    2.  Search the input grid for all occurrences of 2x2 squares where all four pixels have the same color (`square_color`), and `square_color` is not equal to `border_color`.
    3.  For each such 2x2 square found, record its `square_color` and its top-left coordinate `(r, c)`.
    4.  Collect all unique row coordinates (`r`) from the recorded squares into a sorted list, `unique_rows`.
    5.  Collect all unique column coordinates (`c`) from the recorded squares into a sorted list, `unique_cols`.
    6.  Calculate the dimensions for the output grid: `num_rows = max(2, length of unique_rows)` and `num_cols = max(2, length of unique_cols)`.
    7.  Create a new grid (the output grid) with `num_rows` rows and `num_cols` columns, initially filling all its cells with the `border_color`.
    8.  Iterate through the recorded squares (each with `square_color`, `r`, `c`):
        a.  Find the index `i` corresponding to row `r` in the `unique_rows` list.
        b.  Find the index `j` corresponding to column `c` in the `unique_cols` list.
        c.  Set the cell at position `(i, j)` in the output grid to `square_color`.
    9.  The final state of the output grid is the result.
