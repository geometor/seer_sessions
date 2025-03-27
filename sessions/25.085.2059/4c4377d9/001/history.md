
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

*   **Perception:**
    *   The input is a grid of pixels with varying colors (maroon, yellow, blue, green, gray).
    *   The output grid is always twice the height of the input grid, while maintaining the same width.
    *   The output grid appears to be constructed by stacking two versions of the input grid vertically.
    *   The top half of the output grid corresponds to the input grid flipped vertically (rows are in reverse order).
    *   The bottom half of the output grid is an exact copy of the input grid.

*   **Facts:**
    
```yaml
    task: construct_output_grid
    
    elements:
      - type: grid
        name: input_grid
        properties:
          height: H
          width: W
          pixels: colored_values
    
      - type: grid
        name: output_grid
        properties:
          height: 2 * H
          width: W
          pixels: colored_values
    
    relationships:
      - type: composition
        description: The output grid is formed by stacking two grids vertically.
        source: input_grid
        target: output_grid
    
      - type: transformation
        name: vertical_flip
        input: input_grid
        output: top_half_of_output
        details: The rows of the input grid are reversed in order to form the top half of the output grid.
          - output_row[i] = input_row[H - 1 - i] for 0 <= i < H
    
      - type: copy
        name: identity
        input: input_grid
        output: bottom_half_of_output
        details: The bottom half of the output grid is an identical copy of the input grid.
          - output_row[H + i] = input_row[i] for 0 <= i < H
    ```


*   **Natural Language Program:**
    1.  Identify the input grid.
    2.  Determine the height (H) and width (W) of the input grid.
    3.  Create a new grid, the output grid, with height 2\*H and width W.
    4.  Create a vertically flipped version of the input grid. This means arranging the rows of the input grid in reverse order (the last row becomes the first, the second-to-last becomes the second, and so on).
    5.  Place this vertically flipped version into the top half of the output grid (rows 0 to H-1).
    6.  Copy the original input grid directly into the bottom half of the output grid (rows H to 2\*H-1).
