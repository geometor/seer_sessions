
## train_1

**input:**
```
6 3 6 3 6 3 6 1
3 6 3 6 3 6 3 1
6 3 6 3 6 3 6 1
3 6 3 6 3 6 3 1
6 3 6 3 6 3 6 1
3 6 3 6 3 6 3 1
6 3 6 3 6 3 6 1
1 1 1 1 1 1 1 1
```


**output:**
```
3 6 3 6 3 6 3 6
6 3 6 3 6 3 6 3
3 6 3 6 3 6 3 6
6 3 6 3 6 3 6 3
3 6 3 6 3 6 3 6
6 3 6 3 6 3 6 3
3 6 3 6 3 6 3 6
6 3 6 3 6 3 6 3
```


## train_2

**input:**
```
6 7 6 7 6 7 6 3 3 3 3
7 6 7 6 7 6 7 3 3 3 3
6 7 6 7 6 7 6 3 3 3 3
7 6 7 6 7 6 7 3 3 3 3
6 7 6 7 6 7 6 3 3 3 3
7 6 7 6 7 6 7 3 3 3 3
6 7 6 7 6 7 6 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3
```


**output:**
```
7 6 7 6 7 6 7 6 7 6 7
6 7 6 7 6 7 6 7 6 7 6
7 6 7 6 7 6 7 6 7 6 7
6 7 6 7 6 7 6 7 6 7 6
7 6 7 6 7 6 7 6 7 6 7
6 7 6 7 6 7 6 7 6 7 6
7 6 7 6 7 6 7 6 7 6 7
6 7 6 7 6 7 6 7 6 7 6
7 6 7 6 7 6 7 6 7 6 7
6 7 6 7 6 7 6 7 6 7 6
7 6 7 6 7 6 7 6 7 6 7
```


## train_3

**input:**
```
5 4 5 4 5 6
4 5 4 5 4 6
5 4 5 4 5 6
4 5 4 5 4 6
5 4 5 4 5 6
6 6 6 6 6 6
```


**output:**
```
4 5 4 5 4 5
5 4 5 4 5 4
4 5 4 5 4 5
5 4 5 4 5 4
4 5 4 5 4 5
5 4 5 4 5 4
```

*   **Perception**:
    *   Each input grid consists of a main rectangular region in the top-left corner displaying a checkerboard pattern formed by two distinct colors (Color A and Color B).
    *   The remaining area of the input grid, typically the last row(s) and/or last column(s), is filled with a third distinct color (Color C), acting as a border or padding.
    *   The output grid has the same dimensions as the input grid.
    *   The output grid is entirely filled with a checkerboard pattern using the same two colors (Color A and Color B) found in the input's main region.
    *   The key transformation is that the positions of Color A and Color B are swapped in the output checkerboard pattern compared to the input's main region pattern. The color at position (0,0) in the output is different from the color at (0,0) in the input.
    *   The border color (Color C) from the input is completely absent in the output. The swapped checkerboard pattern extends over the entire area of the output grid.

*   **YAML:**
    
```yaml
    facts:
      - description: Identify the dimensions (Height H, Width W) of the input grid.
      - description: Identify the two colors forming the checkerboard pattern in the top-left region.
        label: color_A
        value: input[0][0] # The color at the top-left corner
      - description: Identify the second color in the checkerboard pattern.
        label: color_B
        value: input[0][1] or input[1][0] # The color adjacent to the top-left corner
        condition: Needs verification that it's different from color_A and not the border color.
      - description: Identify the border color (present in the last row/column, distinct from color_A and color_B).
        label: color_C
      - description: The output grid has the same dimensions (H, W) as the input grid.
      - description: The output grid is filled entirely with a checkerboard pattern using color_A and color_B.
      - description: The checkerboard pattern in the output is the inverse of the input's main pattern.
        details: If input[0][0] is color_A, then output[0][0] is color_B. If input[0][0] is color_B, then output[0][0] is color_A.
      - relationship: For any cell (row, col) in the output grid:
          - if (row + col) % 2 == 0, the color is the swapped color corresponding to input[0][0].
          - if (row + col) % 2 != 0, the color is the swapped color corresponding to input[0][1] (or input[1][0]).
      - action: The border color (color_C) is discarded and does not appear in the output.
    ```


*   **Natural Language Program**:
    1.  Determine the height (H) and width (W) of the input grid.
    2.  Identify the color at the top-left corner (0,0) of the input grid; call this `color_1`.
    3.  Identify the color adjacent to the top-left corner (e.g., at (0,1) or (1,0)) that is different from `color_1` and is part of the main checkerboard pattern (i.e., not the border color); call this `color_2`.
    4.  Create a new output grid with the same dimensions (H x W).
    5.  For each cell in the output grid at position (row, col), where row ranges from 0 to H-1 and col ranges from 0 to W-1:
        a.  Calculate the sum `row + col`.
        b.  If `(row + col)` is even (divisible by 2), set the output cell color to `color_2`.
        c.  If `(row + col)` is odd, set the output cell color to `color_1`.
    6.  Return the completed output grid.
