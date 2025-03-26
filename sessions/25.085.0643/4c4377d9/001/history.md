
## train_1

**input:**
```
9 4 9 4
9 9 4 4
4 4 4 4
```


**output:**
```
4 4 4 4
9 9 4 4
9 4 9 4
9 4 9 4
9 9 4 4
4 4 4 4
```


## train_2

**input:**
```
4 1 1 4
1 1 1 1
4 4 4 1
```


**output:**
```
4 4 4 1
1 1 1 1
4 1 1 4
4 1 1 4
1 1 1 1
4 4 4 1
```


## train_3

**input:**
```
3 3 5 5
3 5 5 3
5 5 3 3
```


**output:**
```
5 5 3 3
3 5 5 3
3 3 5 5
3 3 5 5
3 5 5 3
5 5 3 3
```


## train_4

**input:**
```
9 9 5 9
5 5 9 9
9 5 9 9
```


**output:**
```
9 5 9 9
5 5 9 9
9 9 5 9
9 9 5 9
5 5 9 9
9 5 9 9
```

*   **Perception**: The task involves taking an input grid and generating a larger output grid. Across all examples, the input grid is 3 rows high and 4 columns wide. The output grid is always 6 rows high and 4 columns wide, exactly double the height of the input while maintaining the same width. The content of the output grid appears to be derived directly from the input grid. Specifically, the top half of the output grid (the first 3 rows) is a vertically flipped version of the input grid. The bottom half of the output grid (the last 3 rows) is identical to the original input grid. The colors involved change between examples (maroon/yellow, yellow/blue, green/gray, maroon/gray), but the transformation pattern remains consistent.

*   **Facts**:
    
```yaml
    facts:
      - description: Input and Output Grid Dimensions
        input_grid_height: 3
        input_grid_width: 4
        output_grid_height: 6 # 2 * input_grid_height
        output_grid_width: 4  # same as input_grid_width

      - description: Transformation Actions
        action_1: Create a vertically flipped copy of the input grid.
          - Vertical flip means reversing the order of the rows.
          - The first row of the input becomes the last row of the flipped copy.
          - The last row of the input becomes the first row of the flipped copy.
        action_2: Concatenate the flipped copy and the original input grid vertically.
          - The flipped copy forms the top part of the output grid.
          - The original input grid forms the bottom part of the output grid.

      - description: Relationship between Input and Output Structure
        relationship: The output grid is composed of two vertically stacked components.
        component_1:
          position: Top half (rows 0 to input_grid_height - 1)
          content: Vertically flipped version of the input grid.
        component_2:
          position: Bottom half (rows input_grid_height to 2 * input_grid_height - 1)
          content: Original input grid.
    ```


*   **Natural Language Program**:
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Create a new grid (flipped\_grid) with the same dimensions (H x W).
    3.  Populate the `flipped_grid` by reversing the order of the rows from the input grid: the pixel at `input_grid[r][c]` is moved to `flipped_grid[H - 1 - r][c]` for all rows `r` and columns `c`.
    4.  Create the output grid with dimensions (2 * H) x W.
    5.  Copy the `flipped_grid` into the top H rows of the output grid (from row 0 to H-1).
    6.  Copy the original input grid into the bottom H rows of the output grid (from row H to 2*H - 1).
    7.  Return the output grid.
