
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

*   **Perception:**
    *   The task operates on 3x3 grids.
    *   Input grids contain only white (0) and gray (5) pixels.
    *   Output grids contain only red (2), green (3), and yellow (4) pixels.
    *   The output grid has the same dimensions as the input grid.
    *   Each row in the input grid contains exactly one gray (5) pixel.
    *   The transformation appears to be row-dependent. The color of an entire output row is determined by the *column position* of the gray (5) pixel in the corresponding input row.
    *   A specific mapping exists: gray pixel in column 0 maps to a red row, column 1 maps to a yellow row, and column 2 maps to a green row.

*   **Facts:**
    
```yaml
    grid_properties:
      - input_dimensions: 3x3
      - output_dimensions: 3x3
      - input_colors: [white (0), gray (5)]
      - output_colors: [red (2), green (3), yellow (4)]

    objects:
      - type: pixel
        color: gray (5)
        role: indicator
        location: variable within each row of the input grid

    relationships:
      - type: positional_mapping
        description: The column index of the gray (5) pixel within a specific row of the input grid determines the color used for the entire corresponding row in the output grid.

    transformation:
      - type: row_coloring
        input_element: gray (5) pixel location within a row
        output_element: entire row of a single color
        rule: |
          If the gray pixel is in column 0, the output row is red (2).
          If the gray pixel is in column 1, the output row is yellow (4).
          If the gray pixel is in column 2, the output row is green (3).
    ```


*   **Natural Language Program:**
    1.  Create a new output grid with the same dimensions as the input grid.
    2.  For each row in the input grid:
        a.  Find the column index of the cell containing the gray (5) pixel.
        b.  Determine the output color based on this column index:
            *   If the index is 0, the color is red (2).
            *   If the index is 1, the color is yellow (4).
            *   If the index is 2, the color is green (3).
        c.  Fill all cells in the corresponding row of the output grid with the determined color.
    3.  Return the completed output grid.
