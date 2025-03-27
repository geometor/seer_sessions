
## train_1

**input:**
```
5 0 0
0 5 0
5 0 0
```


**output:**
```
2 2 2
4 4 4
2 2 2
```


## train_2

**input:**
```
0 0 5
0 0 5
0 0 5
```


**output:**
```
3 3 3
3 3 3
3 3 3
```


## train_3

**input:**
```
0 5 0
0 0 5
0 5 0
```


**output:**
```
4 4 4
3 3 3
4 4 4
```


## train_4

**input:**
```
0 0 5
0 5 0
5 0 0
```


**output:**
```
3 3 3
4 4 4
2 2 2
```

*   **Perception of the Elements:**
    *   The input grids are all 3x3 and contain only white (0) and gray (5) pixels.
    *   Each row in the input grid contains exactly one gray pixel.
    *   The output grids are also 3x3.
    *   Each row in the output grid consists of a single color, repeated across the row.
    *   The colors appearing in the output rows are red (2), green (3), and yellow (4).
    *   The transformation seems to operate independently on each row. The color used to fill an output row depends on the position (column index) of the gray pixel in the corresponding input row.

*   **Facts:**
    
```yaml
    task_context:
      grid_size:
        input: [3, 3]
        output: [3, 3]
      colors_present:
        input: [white, gray]
        output: [red, green, yellow] # Based on examples
    
    objects:
      - name: gray_pixel
        identified_by: color_value == 5
        properties:
          - location: (row_index, column_index)
          - count_per_row: 1 # Inferred from examples
    
    transformation:
      type: row-wise_mapping
      input_focus: gray_pixel
      output_structure: Each output row is filled with a single color.
      mapping_rule:
        - input_property: column_index_of_gray_pixel
        - output_property: color_of_entire_output_row
        - conditions:
            - if column_index == 0: output_color = red (2)
            - if column_index == 1: output_color = yellow (4)
            - if column_index == 2: output_color = green (3)
    
    relationships:
      - description: The color filling the Nth row of the output grid is determined by the column position of the gray pixel in the Nth row of the input grid.
    
    ignored_elements:
      - white_pixels (0) in the input grid do not directly influence the output color.
    
    assumptions:
      - The input grid will always have exactly one gray pixel per row.
      - The input grid size is consistent (though this might not hold for the test case).
      - The column index mapping (0->2, 1->4, 2->3) is fixed.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid.
    2.  Iterate through each row of the input grid, from top to bottom (let the current row index be `i`).
    3.  Within the current input row `i`, find the column index `j` where the pixel value is gray (5).
    4.  Determine the output color based on the found column index `j`:
        *   If `j` is 0, the output color is red (2).
        *   If `j` is 1, the output color is yellow (4).
        *   If `j` is 2, the output color is green (3).
    5.  Fill the entire corresponding row `i` of the output grid with the determined output color.
    6.  After processing all rows, return the completed output grid.
