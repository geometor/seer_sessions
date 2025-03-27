
## train_1

**input:**
```
0 7 0 7 0 7 0 7
7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
7 0 0 0 0 0 0 0
```


**output:**
```
0 7 0 7 0 7 0 7
7 0 0 0 0 0 0 0
0 6 0 6 0 6 0 6
```


## train_2

**input:**
```
2 1 2 1 2 2 1 2 1 1
7 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
7 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
7 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
7 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2
7 2 2 2 2 2 2 2 2 2
```


**output:**
```
2 1 2 1 2 2 1 2 1 1
7 2 2 2 2 2 2 2 2 2
2 6 2 6 2 2 6 2 6 6
```


## train_3

**input:**
```
1 1 1 4 1 1 1 4 4 1 4 4 1
6 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4
6 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4
6 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4
6 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4
6 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4
6 4 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
1 1 1 4 1 1 1 4 4 1 4 4 1
6 4 4 4 4 4 4 4 4 4 4 4 4
6 6 6 4 6 6 6 4 4 6 4 4 6
```


## train_4

**input:**
```
4 9 4 9 9 4 4 9 9 9 4
7 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9
7 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9
7 9 9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9 9 9
7 9 9 9 9 9 9 9 9 9 9
```


**output:**
```
4 9 4 9 9 4 4 9 9 9 4
7 9 9 9 9 9 9 9 9 9 9
6 9 6 9 9 6 6 9 9 9 6
```

*   **Perception**:
    *   The input grids vary in size, while the output grids consistently have a height of 3 rows and the same width as the corresponding input grid.
    *   The first two rows of the output grid are always identical copies of the first two rows of the input grid.
    *   The third row of the output grid is derived solely from the first row of the input grid through a color substitution rule.
    *   The input grids below the first row seem to follow a pattern (alternating rows starting with a specific color, followed by a background color, and rows filled entirely with that background color), but this pattern doesn't directly influence the output structure beyond establishing the context for the first two rows.
    *   The transformation rule for the third output row depends on identifying two distinct colors present in the first input row. One color acts as a "background" and remains unchanged, while the other "foreground" color is consistently replaced by magenta (6).
    *   The "background" color in the first input row appears to be the same as the dominant color found in the second input row (excluding the first column). The "foreground" color is the other color present in the first input row.

*   **Facts YAML**:
    
```yaml
    task_structure:
      input_grid_size: variable height and width
      output_grid_size: fixed height of 3, width matches input
    
    pertinent_input_elements:
      - row_index: 0
        role: source for output rows 0 and 2
      - row_index: 1
        role: source for output row 1, used to determine background color for row 2 transformation
    
    output_elements_derivation:
      - output_row_index: 0
        source: input row 0
        transformation: direct copy
      - output_row_index: 1
        source: input row 1
        transformation: direct copy
      - output_row_index: 2
        source: input row 0
        transformation: conditional color replacement
    
    row_2_transformation_details:
      target_color: magenta (6)
      rule:
        - description: Identify the background color (BG) from input row 1 (dominant color excluding first pixel).
        - description: Identify the foreground color (FG) from input row 0 (the color that is not BG).
        - description: Iterate through each pixel in input row 0.
        - condition: If pixel color is BG, keep the color BG in output row 2.
        - condition: If pixel color is FG, change the color to magenta (6) in output row 2.
    
    ignored_input_elements:
      - description: Input grid rows from index 2 onwards.
        reason: Do not affect the output grid generation based on observed patterns.
    
    ```


*   **Natural Language Program**:
    1.  Determine the width (`W`) of the input grid. Create a new output grid with 3 rows and `W` columns.
    2.  Copy the first row (row 0) of the input grid directly to the first row (row 0) of the output grid.
    3.  Copy the second row (row 1) of the input grid directly to the second row (row 1) of the output grid.
    4.  Identify the background color: Examine the second row (row 1) of the input grid. The color that appears in most cells (specifically, from the second cell onwards) is the background color.
    5.  Identify the foreground color: Examine the first row (row 0) of the input grid. The color present that is *not* the background color is the foreground color.
    6.  Generate the third row (row 2) of the output grid: Iterate through each pixel in the first row (row 0) of the input grid. For each pixel:
        *   If the pixel's color is the identified background color, place the background color in the corresponding position in the output grid's third row.
        *   If the pixel's color is the identified foreground color, place the color magenta (6) in the corresponding position in the output grid's third row.
