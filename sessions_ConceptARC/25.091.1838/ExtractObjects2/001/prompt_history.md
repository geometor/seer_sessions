
## train_1

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 3 1 1 1 1 1 3 1 1 1 1 1
0 0 0 3 0 0 0 3 0 0 0 0 0 0
1 1 1 1 3 1 3 1 1 1 1 1 1 1
0 0 0 0 0 3 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 3 0 0 0
0 0 3 0 3 0 0
0 3 0 0 0 3 0
3 0 0 0 0 0 3
0 3 0 0 0 3 0
0 0 3 0 3 0 0
0 0 0 3 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 2 0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0 2 0 2
0 0 0 9 9 9 9 9 0 0 0 0 0 0 0 0
4 0 4 9 4 0 4 9 4 0 4 0 4 0 4 0
0 4 0 9 0 4 0 9 0 4 0 4 0 4 0 4
0 0 0 9 0 0 0 9 0 0 0 0 0 0 0 0
6 0 6 9 9 9 9 9 6 0 6 0 6 0 6 0
0 6 0 6 0 6 0 6 0 6 0 6 0 6 0 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 0 8 0 8 0 8 0 8 0 8 0 8 0 8 0
0 8 0 8 0 8 0 8 0 8 0 8 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
5 0 5 0 5 0 5 0 5 0 5 0 5 0 5 0
0 5 0 5 0 5 0 5 0 5 0 5 0 5 0 5
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 9 9 9 9
9 0 0 0 9
9 0 0 0 9
9 0 0 0 9
9 9 9 9 9
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
4 0 0 0 4 0 0 0 4 0 0
0 4 0 4 0 4 0 4 0 4 0
0 0 4 0 0 0 4 0 0 0 4
4 0 0 6 6 6 0 0 4 0 0
0 4 0 4 0 6 0 4 0 4 0
0 0 4 0 0 6 4 0 0 0 4
4 0 0 6 6 6 0 0 0 0 0
0 4 0 4 0 4 0 0 0 4 0
0 0 4 0 0 0 4 0 4 0 4
0 0 0 0 0 0 0 4 0 0 0
```


**output:**
```
6 6 6
0 0 6
0 0 6
6 6 6
```

*   **Perception**:
    *   Each input grid contains multiple colors, typically including white (0) as a background or separator.
    *   There appears to be one specific color in each input grid that forms a distinct, often central, shape or object (green=3 in train\_1, maroon=9 in train\_2, magenta=6 in train\_3).
    *   Other colors might form background patterns (like the blue lines in train\_1) or scattered elements (like the various colors in train\_2, yellow in train\_3).
    *   The output grid is always smaller than the input grid.
    *   The output grid's dimensions seem determined by the spatial extent (bounding box) of the single distinct object identified in the input.
    *   The output grid contains only the color of the distinct object and white (0).
    *   The transformation involves isolating the distinct object within its bounding box and removing any other non-white colors from that box, replacing them with white (0). The structure of the distinct object and the relative positions of the white pixels within the box are preserved.
    *   The key steps seem to be: identifying the unique "foreground" object's color, determining its bounding box, extracting that region, and then filtering out any "noise" colors within that region, keeping only the foreground color and white.

*   **Facts**:
    
```yaml
    task_type: extraction_and_filtering
    
    components:
      - role: input_grid
        attributes: [ M x N dimensions, multiple colors ]
      - role: output_grid
        attributes: [ m x n dimensions (m <= M, n <= N), two colors (target_color, white=0) ]
      - role: target_object
        identified_by: color that forms a single contiguous non-white object in the input grid
        attributes: [ target_color (e.g., green=3, maroon=9, magenta=6), spatial_extent ]
      - role: background_pixels
        identified_by: color white=0
      - role: noise_pixels
        identified_by: non-white colors other than the target_color
        location: potentially anywhere, including within the target_object's bounding box
    
    actions:
      - name: identify_target_color
        inputs: [ input_grid ]
        outputs: [ target_color ]
        description: Find the non-white color that forms exactly one contiguous object.
      - name: find_bounding_box
        inputs: [ input_grid, target_color ]
        outputs: [ top_row, bottom_row, left_col, right_col ]
        description: Determine the minimum and maximum row and column indices containing the target_color.
      - name: extract_subgrid
        inputs: [ input_grid, bounding_box ]
        outputs: [ extracted_grid ]
        description: Copy the portion of the input_grid defined by the bounding_box.
      - name: filter_subgrid
        inputs: [ extracted_grid, target_color ]
        outputs: [ output_grid ]
        description: Create the final output grid by replacing any pixel in the extracted_grid that is not the target_color and not white (0) with white (0).
    
    relationships:
      - The output_grid dimensions match the dimensions of the target_object's bounding_box.
      - The pixels in the output_grid correspond to the pixels within the target_object's bounding_box in the input_grid, after filtering.
    ```


*   **Natural Language Program**:
    1.  Analyze the input grid to identify all unique non-white colors present.
    2.  For each unique non-white color, determine the number of distinct contiguous objects formed by pixels of that color.
    3.  Identify the 'target color' as the color that forms exactly one contiguous object.
    4.  Find the minimum bounding box (smallest rectangle containing all pixels) of the target color within the input grid. Note its top row, bottom row, left column, and right column.
    5.  Determine the height and width of the output grid based on the dimensions of the bounding box calculated in the previous step (height = bottom\_row - top\_row + 1, width = right\_col - left\_col + 1).
    6.  Create a new grid (the output grid) with these dimensions.
    7.  Iterate through each cell within the calculated bounding box in the input grid (from top\_row to bottom\_row, and left\_col to right\_col).
    8.  For each cell (r, c) in the input grid's bounding box, get its color.
    9.  Determine the corresponding cell location (r - top\_row, c - left\_col) in the output grid.
    10. If the color from the input cell is the 'target color' or white (0), place that color in the corresponding output grid cell.
    11. If the color from the input cell is neither the 'target color' nor white (0), place white (0) in the corresponding output grid cell.
    12. The resulting grid is the final output.
