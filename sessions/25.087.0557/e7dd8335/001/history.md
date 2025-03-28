
## train_1

**input:**
```
0 1 1 1 1 1 0
0 1 0 1 0 1 0
0 1 0 1 0 1 0
0 1 0 1 0 1 0
0 1 0 1 0 1 0
0 1 1 1 1 1 0
0 0 0 0 0 0 0
```


**output:**
```
0 1 1 1 1 1 0
0 1 0 1 0 1 0
0 1 0 1 0 1 0
0 2 0 2 0 2 0
0 2 0 2 0 2 0
0 2 2 2 2 2 0
0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0
0 1 0 0 1 0 0 0 0
0 1 0 0 1 0 0 0 0
0 1 0 0 1 0 0 0 0
0 1 0 0 1 0 0 0 0
0 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0
0 1 0 0 1 0 0 0 0
0 1 0 0 1 0 0 0 0
0 2 0 0 2 0 0 0 0
0 2 0 0 2 0 0 0 0
0 2 2 2 2 0 0 0 0
```


## train_3

**input:**
```
0 0 0 1 0 0 0 0 0
0 1 1 1 1 1 0 0 0
0 0 1 0 1 0 0 0 0
0 0 1 0 1 0 0 0 0
0 0 1 0 1 0 0 0 0
0 0 1 0 1 0 0 0 0
0 1 1 1 1 1 0 0 0
0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 0 0 0 0 0
0 1 1 1 1 1 0 0 0
0 0 1 0 1 0 0 0 0
0 0 1 0 1 0 0 0 0
0 0 2 0 2 0 0 0 0
0 0 2 0 2 0 0 0 0
0 2 2 2 2 2 0 0 0
0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    *   The input grids contain patterns of blue pixels (1) on a white background (0).
    *   These blue pixels often form hollow rectangular shapes, but can also include extensions or be more scattered as seen in train\_3.
    *   The output grids are largely identical to the input grids, with the key difference being that some of the blue pixels (1) have been changed to red pixels (2).
    *   The transformation seems selective, only affecting certain blue pixels based on their position.
    *   Comparing the input and output grids, the blue pixels that change to red appear to be located in the lower portion of the blue pattern's vertical extent.

*   **YAML Facts**:
    
```yaml
    elements:
      - object: background
        color: white (0)
        description: The grid background.
      - object: pattern_pixels
        color: blue (1)
        description: Pixels forming the primary pattern in the input.
      - object: modified_pixels
        color: red (2)
        description: Pixels in the output that were originally blue but changed color.

    relationships:
      - type: positional
        description: The transformation depends on the vertical position of blue pixels.
      - property: vertical_extent
        description: The set of all blue pixels occupies a range of rows.
        attributes:
          - min_row: The topmost row index containing a blue pixel.
          - max_row: The bottommost row index containing a blue pixel.
      - property: vertical_midpoint
        description: A conceptual horizontal line dividing the vertical extent of the blue pixels.

    actions:
      - action: identify_blue_pixels
        input: input_grid
        output: coordinates of all blue pixels
      - action: calculate_vertical_extent
        input: coordinates of blue pixels
        output: min_row, max_row
      - action: determine_change_threshold
        input: min_row, max_row
        # calculation: threshold_row = min_row + floor((max_row - min_row + 1) / 2)
        # Alternative simpler definition: threshold_row = floor((min_row + max_row) / 2) + 1 if considering rows >= threshold
        # Let's stick to the first calculation as it seems more robust for even/odd heights.
        # Example 1: min=0, max=5. height=6. threshold = 0 + floor(6/2) = 3. Rows >= 3 change.
        # Example 2: min=2, max=7. height=6. threshold = 2 + floor(6/2) = 5. Rows >= 5 change.
        # Example 3: min=0, max=7. height=8. threshold = 0 + floor(8/2) = 4. Rows >= 4 change.
        output: threshold_row_index
      - action: recolor_pixels
        input: input_grid, threshold_row_index
        description: Change the color of blue pixels (1) to red (2) if their row index is greater than or equal to the threshold_row_index.
        output: output_grid
    ```


*   **Natural Language Program**:
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Identify the coordinates (row, column) of all blue pixels (1) in the input grid.
    3.  If no blue pixels are found, return the copied input grid as is.
    4.  Determine the minimum (`min_row`) and maximum (`max_row`) row indices among all identified blue pixels.
    5.  Calculate the vertical midpoint threshold row: `threshold_row = min_row + floor((max_row - min_row + 1) / 2)`.
    6.  Iterate through all the identified blue pixel coordinates.
    7.  For each blue pixel, if its row index is greater than or equal to `threshold_row`, change the color of the corresponding pixel in the output grid to red (2).
    8.  Return the modified output grid.
