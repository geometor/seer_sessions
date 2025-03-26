
## train_1

**input:**
```
8 0 3 0 0
8 6 5 6 0
3 6 3 0 0
0 0 0 5 9
5 0 9 0 0
```


**output:**
```
0 0 3 0 0
0 0 5 0 0
0 0 3 0 0
0 0 0 0 0
0 0 9 0 0
```


## train_2

**input:**
```
6 4 0
0 3 9
1 0 0
```


**output:**
```
0 4 0
0 3 0
0 0 0
```


## train_3

**input:**
```
3 0 4 0 0
3 0 4 7 0
0 6 0 0 7
0 0 8 0 0
0 8 0 2 2
```


**output:**
```
0 0 4 0 0
0 0 4 0 0
0 0 0 0 0
0 0 8 0 0
0 0 0 0 0
```

*   **Perception:**
    *   The task takes an input grid of colored pixels and produces an output grid of the same dimensions.
    *   The output grid appears significantly sparser than the input grid, containing mostly white pixels (0).
    *   The non-white pixels in the output grid are always located in a single vertical column.
    *   These non-white pixels in the output grid retain their original colors and vertical positions from the input grid.
    *   Comparing the input and output across all examples, the column that is preserved in the output corresponds to the central vertical column of the input grid. All pixels outside this central column in the input are replaced with white (0) in the output.
    *   The center column index seems to be calculated based on the grid's width (e.g., for width 5, the index is 2; for width 3, the index is 1). This corresponds to integer division of `(width - 1) / 2`.

*   **Facts:**
    
```yaml
    task_type: transformation
    input_object:
      type: grid
      description: A 2D grid of pixels with colors represented by integers 0-9.
    output_object:
      type: grid
      description: A 2D grid of pixels, same dimensions as the input grid.
    transformation:
      relationship: column_extraction
      properties:
        - input_grid_width: The number of columns in the input grid.
        - center_column_index: Calculated as floor((input_grid_width - 1) / 2).
        - preserved_elements: Pixels located in the center column of the input grid.
        - modified_elements: Pixels located outside the center column of the input grid.
      actions:
        - Initialize the output grid with the same dimensions as the input grid, filled entirely with white pixels (0).
        - Identify the center column index of the input grid.
        - Iterate through each row of the input grid.
        - For each row, copy the pixel value from the center column of the input grid to the corresponding position (same row, same center column index) in the output grid.
        - All other positions in the output grid remain white (0).
    ```


*   **Natural Language Program:**
    1.  Determine the dimensions (height and width) of the input grid.
    2.  Calculate the index of the central column using the formula: `center_column_index = floor((width - 1) / 2)`.
    3.  Create a new output grid with the same height and width as the input grid, and initialize all its pixels to white (0).
    4.  For each row `r` from 0 to `height - 1`:
        a.  Get the pixel value from the input grid at position (`r`, `center_column_index`).
        b.  Set the pixel value in the output grid at position (`r`, `center_column_index`) to the value obtained in step 4a.
    5.  The resulting grid is the final output.
