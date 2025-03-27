
## train_1

**input:**
```
3 2 1 4
5 5 5 5
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```


**output:**
```
3 2 1 4
5 5 5 5
3 3 3 3
2 2 2 2
1 1 1 1
4 4 4 4
3 3 3 3
2 2 2 2
1 1 1 1
4 4 4 4
```


## train_2

**input:**
```
2 1 4
5 5 5
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```


**output:**
```
2 1 4
5 5 5
2 2 2
1 1 1
4 4 4
2 2 2
1 1 1
4 4 4
```


## train_3

**input:**
```
8 3
5 5
0 0
0 0
0 0
0 0
```


**output:**
```
8 3
5 5
8 8
3 3
8 8
3 3
```

*   **Perception of Task Elements:**
    *   The input grids consist of three main parts:
        1.  A top row (row index 0) containing a sequence of different colors.
        2.  A second row (row index 1) composed entirely of gray pixels (color 5), acting as a separator.
        3.  The remaining rows below the separator, initially filled with white pixels (color 0).
    *   The output grids retain the first two rows from the input unchanged.
    *   The rows below the gray separator in the output are filled based on the color sequence found in the first row of the input.
    *   Each output row below the separator is filled entirely with a single color.
    *   The colors used to fill these rows cycle through the sequence defined in the first input row.

*   **Facts:**
    
```yaml
    task: fill_rows_cyclically
    elements:
      - type: grid
        properties:
          - contains_distinct_regions
          - top_row_is_color_sequence
          - second_row_is_separator
          - lower_region_is_initially_uniform
    objects:
      - id: color_sequence
        description: The sequence of colors in the first row (index 0) of the input grid.
        source: input_grid[0]
      - id: separator
        description: The row of gray pixels (color 5) at row index 1.
        source: input_grid[1]
      - id: fill_region
        description: The rows below the separator (index 2 onwards) in the input grid, initially white (color 0).
        source: input_grid[2:]
    actions:
      - action: copy
        source: input_grid[0:2] # First two rows
        target: output_grid[0:2]
        description: The color sequence row and the separator row are copied directly to the output.
      - action: fill_cyclically
        source: color_sequence
        target: output_grid[2:] # Rows below the separator in the output
        parameters:
          - grid_width: width of the input/output grid
          - sequence_length: length of the color_sequence
        description: >
          For each row in the output grid starting from index 2, determine the color
          to use by cycling through the color_sequence. The color index is calculated
          as `(row_index - 2) % sequence_length`. Fill the entire row with the selected color.
    relationships:
      - type: source_target
        source: color_sequence
        target: output_grid[2:]
        description: The color sequence from the input's first row dictates the colors used to fill the rows below the separator in the output.
      - type: reference
        source: input_grid.width
        target: fill_cyclically action
        description: The width of the grid determines how many times the selected color is repeated in each filled row.
    ```


*   **Natural Language Program:**
    1.  Identify the sequence of colors present in the first row (index 0) of the input grid. Let this sequence be `ColorSequence`.
    2.  Identify the gray separator row at index 1 of the input grid.
    3.  Create the output grid with the same dimensions as the input grid.
    4.  Copy the first row (containing `ColorSequence`) and the second row (the gray separator) from the input grid to the first two rows of the output grid.
    5.  Determine the number of colors in `ColorSequence`, let this be `N`.
    6.  Determine the width of the grid, let this be `W`.
    7.  For each subsequent row in the output grid, starting from row index 2 up to the last row:
        a.  Calculate the index `idx` for `ColorSequence` using the formula: `idx = (current_row_index - 2) % N`.
        b.  Select the color at `ColorSequence[idx]`.
        c.  Fill the entire current row of the output grid (all `W` columns) with the selected color.
